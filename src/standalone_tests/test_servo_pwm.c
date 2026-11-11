/**
  ******************************************************************************
  * @file    test_servo_pwm.c
  * @brief   Aquatic Guardian - Standalone Bench Test for Member 3 (Gia)
  *          Subsystem: Motor Actuation & Dispenser Mechanism
  *          Target MCU: STM32F401RE / F411RE / F429ZI Nucleo
  *          Peripheral: TIM2_CH1 PWM on PA0 (SG90 Servo)
  *                      Optional: 28BYJ-48 Stepper on PB12-PB15
  * @author  Group 7 - MCP201 Capstone Project
  ******************************************************************************
  * @how_to_use
  * 1. Connect SG90 Servo PWM signal (Orange wire) to Nucleo pin PA0.
  * 2. Connect SG90 Servo VCC (Red wire) to EXTERNAL 5V power supply (+5V).
  * 3. Connect SG90 Servo GND (Brown wire) to EXTERNAL 5V GND AND Nucleo GND!
  *    CAUTION: Never power servo directly from Nucleo 5V/3.3V pin (brownout risk).
  * 4. Call Test_Servo_PWM_Run() in main() before osKernelInitialize() or in a
  *    simple bare-metal while(1) loop to verify servo movement in 5 minutes.
  ******************************************************************************
  */

#include "main.h"
#include <stdbool.h>
#include <stdint.h>

/* ========================================================================== */
/* Hardware Configuration & Constants                                         */
/* ========================================================================== */

/* APB1 Timer Clock = 84 MHz (STM32F401RE/F411RE default)                    */
/* PSC = 83  ==> f_cnt = 84 MHz / (83 + 1) = 1 MHz (1 tick = 1 microsecond)  */
/* ARR = 19999 ==> Period = (19999 + 1) * 1us = 20,000 us = 20ms (50 Hz)     */
#define SERVO_TIM_HANDLE            htim2
#define SERVO_TIM_CHANNEL           TIM_CHANNEL_1

#define SERVO_PULSE_0_DEG_TICKS     1000U   /* 1.0 ms pulse -> 0 degrees (Closed)  */
#define SERVO_PULSE_90_DEG_TICKS    1500U   /* 1.5 ms pulse -> 90 degrees (Dispense)*/
#define SERVO_PULSE_180_DEG_TICKS   2000U   /* 2.0 ms pulse -> 180 degrees (Max)   */

/* External timer handle configured by STM32CubeMX */
extern TIM_HandleTypeDef htim2;

/* ========================================================================== */
/* Helper Functions                                                           */
/* ========================================================================== */

/**
  * @brief  Set SG90 Servo pulse width in ticks (microseconds).
  * @param  pulse_ticks: 1000 (0 deg) to 2000 (180 deg).
  */
static void Servo_SetPulseTicks(uint32_t pulse_ticks)
{
    if (pulse_ticks < SERVO_PULSE_0_DEG_TICKS)   pulse_ticks = SERVO_PULSE_0_DEG_TICKS;
    if (pulse_ticks > SERVO_PULSE_180_DEG_TICKS) pulse_ticks = SERVO_PULSE_180_DEG_TICKS;

    __HAL_TIM_SET_COMPARE(&SERVO_TIM_HANDLE, SERVO_TIM_CHANNEL, pulse_ticks);
}

/**
  * @brief  Convert target angle (0 to 180 degrees) to PWM pulse width.
  * @param  angle_deg: Angle in degrees (0 - 180).
  */
static void Servo_SetAngle(uint8_t angle_deg)
{
    if (angle_deg > 180U) angle_deg = 180U;
    uint32_t pulse = SERVO_PULSE_0_DEG_TICKS + 
        ((uint32_t)angle_deg * (SERVO_PULSE_180_DEG_TICKS - SERVO_PULSE_0_DEG_TICKS)) / 180U;
    Servo_SetPulseTicks(pulse);
}

/* ========================================================================== */
/* Standalone Bench Test Runner                                               */
/* ========================================================================== */

/**
  * @brief  Standalone test routine for Member 3.
  *         Sweeps the SG90 servo between 0 deg (closed) and 90 deg (dispense).
  *         Blinks Green User LED (PA5) on each dispense cycle.
  */
void Test_Servo_PWM_Run(void)
{
    /* 1. Start PWM Generation on TIM2 Channel 1 */
    HAL_TIM_PWM_Start(&SERVO_TIM_HANDLE, SERVO_TIM_CHANNEL);

    /* 2. Initial state: Closed position (0 deg) */
    Servo_SetAngle(0);
    HAL_Delay(1000);

    while (1)
    {
        /* Step A: Open feeder slot to 90 degrees (Dispense food) */
        Servo_SetAngle(90);
        HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET); /* Green LED ON */
        HAL_Delay(800); /* Hold open for 800ms to allow food pellets to drop */

        /* Step B: Close feeder slot back to 0 degrees */
        Servo_SetAngle(0);
        HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_RESET); /* Green LED OFF */
        HAL_Delay(1200); /* Rest closed for 1.2s */

        /* Step C: Full sweep test (0 -> 45 -> 90 -> 135 -> 180 -> 0) */
        for (uint8_t deg = 0; deg <= 90; deg += 15)
        {
            Servo_SetAngle(deg);
            HAL_Delay(100);
        }
        HAL_Delay(500);

        for (int16_t deg = 90; deg >= 0; deg -= 15)
        {
            Servo_SetAngle((uint8_t)deg);
            HAL_Delay(100);
        }
        HAL_Delay(2000); /* Wait 2s before next test cycle */
    }
}

/* ========================================================================== */
/* Fallback: 28BYJ-48 Stepper Motor Driver on PB12 - PB15 (ULN2003)           */
/* Note: Completely avoids I2C1 pins PB8 / PB9!                               */
/* ========================================================================== */

#define STEPPER_IN1_PIN   GPIO_PIN_12  /* GPIOB */
#define STEPPER_IN2_PIN   GPIO_PIN_13  /* GPIOB */
#define STEPPER_IN3_PIN   GPIO_PIN_14  /* GPIOB */
#define STEPPER_IN4_PIN   GPIO_PIN_15  /* GPIOB */

static const uint8_t step_sequence[4][4] = {
    {1, 0, 0, 0},
    {0, 1, 0, 0},
    {0, 0, 1, 0},
    {0, 0, 0, 1}
};

void Test_Stepper_Step(uint8_t step_index)
{
    HAL_GPIO_WritePin(GPIOB, STEPPER_IN1_PIN, step_sequence[step_index][0] ? GPIO_PIN_SET : GPIO_PIN_RESET);
    HAL_GPIO_WritePin(GPIOB, STEPPER_IN2_PIN, step_sequence[step_index][1] ? GPIO_PIN_SET : GPIO_PIN_RESET);
    HAL_GPIO_WritePin(GPIOB, STEPPER_IN3_PIN, step_sequence[step_index][2] ? GPIO_PIN_SET : GPIO_PIN_RESET);
    HAL_GPIO_WritePin(GPIOB, STEPPER_IN4_PIN, step_sequence[step_index][3] ? GPIO_PIN_SET : GPIO_PIN_RESET);
}
