/**
  ******************************************************************************
  * @file    test_tds_filter.c
  * @brief   Aquatic Guardian - Standalone Bench Test for Member 2 (Manh)
  *          Subsystem: Sensing & Analog DSP Processing
  *          Target MCU: STM32F401RE / F411RE / F429ZI Nucleo
  *          Peripherals:
  *            - ADC1_IN1 on PA1 (Analog TDS Sensor V1.0)
  *            - ADC1_IN4 on PA4 (10k Potentiometer - Portion Dial)
  *            - 1-Wire GPIO on PA8 (Waterproof DS18B20 with 4.7k pull-up)
  * @author  Group 7 - MCP201 Capstone Project
  ******************************************************************************
  * @how_to_use
  * 1. Connect TDS Sensor Analog OUT to Nucleo PA1, VCC to 3.3V/5V, GND to GND.
  * 2. Connect 10k Potentiometer center wiper to PA4, outer legs to 3.3V and GND.
  * 3. (Optional) Connect DS18B20 Data to PA8 with 4.7k resistor pulled up to 3.3V.
  * 4. Call Test_TDS_Filter_Run() in main().
  * 5. Observe readings on Serial terminal (USART2 @ 115200 bps):
  *    - Cup A (Clean tap water): TDS ~ 80 - 150 ppm (Optimal).
  *    - Cup B (Water with pinch of salt): TDS > 500 ppm (Critical Hazard).
  ******************************************************************************
  */

#include "main.h"
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>

/* ========================================================================== */
/* Hardware & Algorithm Constants                                             */
/* ========================================================================== */

#define TDS_FILTER_SAMPLES      20U     /* 20-sample Ring Buffer (Thesis)    */
#define VREF_VOLTAGE            3.3f    /* STM32 ADC Reference Voltage       */
#define ADC_MAX_COUNT           4095.0f /* 12-bit ADC Max Value (2^12 - 1)   */

/* External HAL handles */
extern ADC_HandleTypeDef  hadc1;
extern UART_HandleTypeDef huart2; /* ST-LINK VCP (PA2/PA3) */

/* 20-Sample Circular Buffer Structures */
static uint16_t tds_ring_buffer[TDS_FILTER_SAMPLES] = {0};
static uint8_t  ring_head = 0;
static uint8_t  ring_count = 0;
static uint32_t running_sum = 0;

/* ========================================================================== */
/* Dynamic Channel Polling (Chống ghi đè ADC1->DR)                            */
/* ========================================================================== */

/**
  * @brief  Reads a single ADC1 channel on-demand to prevent DR register overwrite.
  * @param  channel: ADC_CHANNEL_1 (PA1) or ADC_CHANNEL_4 (PA4).
  * @retval 12-bit raw ADC reading (0 - 4095).
  */
static uint16_t ADC1_ReadChannel_Dynamic(uint32_t channel)
{
    ADC_ChannelConfTypeDef sConfig = {0};
    sConfig.Channel      = channel;
    sConfig.Rank         = 1;
    sConfig.SamplingTime = ADC_SAMPLETIME_84CYCLES;

    HAL_ADC_ConfigChannel(&hadc1, &sConfig);
    HAL_ADC_Start(&hadc1);

    uint16_t val = 0;
    if (HAL_ADC_PollForConversion(&hadc1, 10) == HAL_OK)
    {
        val = (uint16_t)HAL_ADC_GetValue(&hadc1);
    }
    HAL_ADC_Stop(&hadc1);

    return val;
}

/* ========================================================================== */
/* 20-Sample Circular Moving Average Filter (O(1) Running Sum)                */
/* ========================================================================== */

/**
  * @brief  Applies a 20-sample circular moving average filter in O(1) time.
  * @param  new_sample: Latest raw 12-bit ADC conversion.
  * @retval Filtered ADC average.
  */
static uint16_t TDS_ApplyFilter(uint16_t new_sample)
{
    if (ring_count < TDS_FILTER_SAMPLES)
    {
        /* Buffer warming up: accumulator adds new sample */
        running_sum += new_sample;
        tds_ring_buffer[ring_head] = new_sample;
        ring_head = (ring_head + 1) % TDS_FILTER_SAMPLES;
        ring_count++;
        return (uint16_t)(running_sum / ring_count);
    }
    else
    {
        /* O(1) Sliding update: subtract oldest sample, add new sample */
        running_sum = running_sum - tds_ring_buffer[ring_head] + new_sample;
        tds_ring_buffer[ring_head] = new_sample;
        ring_head = (ring_head + 1) % TDS_FILTER_SAMPLES;
        return (uint16_t)(running_sum / TDS_FILTER_SAMPLES);
    }
}

/* ========================================================================== */
/* Temperature-Compensated Exact Cubic TDS Formula                            */
/* ========================================================================== */

/**
  * @brief  Calculates TDS ppm using temperature compensation and exact cubic polynomial.
  *         Formula:
  *           Vcomp = Vadc / (1.0 + 0.02 * (T - 25.0))
  *           TDS   = (133.42 * Vcomp^3 - 255.86 * Vcomp^2 + 857.39 * Vcomp) * 0.5
  * @param  filtered_adc: 12-bit filtered ADC count.
  * @param  temp_celsius: Water temperature in degrees Celsius (from DS18B20).
  * @retval Calculated TDS value in ppm.
  */
static float TDS_CalculatePPM(uint16_t filtered_adc, float temp_celsius)
{
    /* 1. Convert raw ADC to voltage (0.0V - 3.3V) */
    float voltage = ((float)filtered_adc / ADC_MAX_COUNT) * VREF_VOLTAGE;

    /* 2. Temperature compensation factor (2% per deg C, normalized to 25 deg C) */
    float temp_coeff = 1.0f + 0.02f * (temp_celsius - 25.0f);
    if (temp_coeff < 0.1f) temp_coeff = 1.0f; /* Guard against divide by zero */

    float v_comp = voltage / temp_coeff;

    /* 3. Exact 3rd-order polynomial */
    float tds_ppm = (133.42f * v_comp * v_comp * v_comp
                   - 255.86f * v_comp * v_comp
                   + 857.39f * v_comp) * 0.5f;

    if (tds_ppm < 0.0f) tds_ppm = 0.0f;
    return tds_ppm;
}

/* ========================================================================== */
/* Standalone Bench Test Runner                                               */
/* ========================================================================== */

/**
  * @brief  Standalone test routine for Member 2.
  *         Continuously samples TDS & Potentiometer, filters readings,
  *         and logs formatted results over USART2 (115200 bps).
  */
void Test_TDS_Filter_Run(void)
{
    char msg[128];
    float simulated_water_temp = 25.5f; /* Replace with DS18B20 1-Wire read on PA8 */

    /* Reset filter buffer */
    memset(tds_ring_buffer, 0, sizeof(tds_ring_buffer));
    ring_head = 0;
    ring_count = 0;
    running_sum = 0;

    snprintf(msg, sizeof(msg), "\r\n=== Aquatic Guardian: TDS Sensor Bench Test ===\r\n");
    HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), 100);

    while (1)
    {
        /* 1. Dynamic channel reads */
        uint16_t raw_tds_adc = ADC1_ReadChannel_Dynamic(ADC_CHANNEL_1);
        uint16_t raw_pot_adc = ADC1_ReadChannel_Dynamic(ADC_CHANNEL_4);

        /* 2. Apply 20-sample Ring Buffer Filter */
        uint16_t filtered_adc = TDS_ApplyFilter(raw_tds_adc);

        /* 3. Compute compensated TDS ppm */
        float tds_ppm = TDS_CalculatePPM(filtered_adc, simulated_water_temp);
        float voltage = ((float)filtered_adc / ADC_MAX_COUNT) * VREF_VOLTAGE;

        /* 4. Convert Potentiometer to Portion grams (1g - 15g) */
        uint8_t portion_grams = (uint8_t)((raw_pot_adc * 15U) / 4095U) + 1U;

        /* 5. Classification */
        const char *status_str = "OPTIMAL";
        if (tds_ppm > 500.0f) {
            status_str = "CRITICAL HAZARD [!]";
            HAL_GPIO_WritePin(GPIOB, GPIO_PIN_1, GPIO_PIN_SET); /* Red LED ON */
        } else if (tds_ppm > 350.0f) {
            status_str = "WARNING ELEVATED";
            HAL_GPIO_WritePin(GPIOB, GPIO_PIN_1, GPIO_PIN_RESET);
        } else {
            status_str = "NORMAL OK";
            HAL_GPIO_WritePin(GPIOB, GPIO_PIN_1, GPIO_PIN_RESET);
        }

        /* 6. Print diagnostics to PC console */
        snprintf(msg, sizeof(msg),
                 "[TDS] Raw:%4u | Filt:%4u | Volt:%.3fV | TDS:%5.1f ppm | Temp:%.1fC | Pot:%2dg | %s\r\n",
                 raw_tds_adc, filtered_adc, voltage, tds_ppm, simulated_water_temp, portion_grams, status_str);
        HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), 100);

        HAL_Delay(200); /* 5 Hz sample rate: 20 samples converge in 4 seconds */
    }
}
