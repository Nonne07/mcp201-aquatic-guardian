/**
  ******************************************************************************
  * @file    test_i2c_scanner.c
  * @brief   Aquatic Guardian - Standalone Bench Test for Member 4 (Minh)
  *          Subsystem: Shared I2C1 Bus Scanner & Peripheral Probe
  *          Target MCU: STM32F401RE / F411RE / F429ZI Nucleo
  *          Peripheral: I2C1 on PB8 (SCL) and PB9 (SDA)
  *          Target Slaves:
  *            - LCD2004 Backpack (PCF8574): 0x27 (or 0x3F)
  *            - DS3231 RTC Module:         0x68
  *            - AT24C32 EEPROM:             0x57
  * @author  Group 7 - MCP201 Capstone Project
  ******************************************************************************
  * @how_to_use
  * 1. Wire LCD backpack, DS3231 RTC, and AT24C32 EEPROM in parallel to:
  *    - SCL -> Nucleo pin PB8 (D15)
  *    - SDA -> Nucleo pin PB9 (D14)
  *    - VCC -> 5V (for LCD) and 3.3V (for RTC/EEPROM)
  *    - GND -> Nucleo GND
  *    Ensure 4.7k pull-up resistors to 3.3V/5V are present on SCL & SDA lines.
  * 2. Call Test_I2C_Scanner_Run() in main().
  * 3. Open Serial Terminal (USART2 @ 115200 bps) to inspect bus scan results.
  ******************************************************************************
  */

#include "main.h"
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>

/* ========================================================================== */
/* Target I2C 7-bit Addresses                                                 */
/* ========================================================================== */

#define I2C_ADDR_LCD_PRIMARY     0x27U   /* Standard PCF8574 backpack        */
#define I2C_ADDR_LCD_SECONDARY   0x3FU   /* PCF8574A backpack                */
#define I2C_ADDR_DS3231_RTC      0x68U   /* DS3231 Real-Time Clock           */
#define I2C_ADDR_AT24C32_EEPROM  0x57U   /* AT24C32 32-Kbit EEPROM           */

/* External HAL Handles */
extern I2C_HandleTypeDef  hi2c1;
extern UART_HandleTypeDef huart2;

/* ========================================================================== */
/* Utility Helpers                                                            */
/* ========================================================================== */

static void UART_Log(const char *str)
{
    HAL_UART_Transmit(&huart2, (uint8_t*)str, strlen(str), 100);
}

/**
  * @brief  Quick read of DS3231 RTC seconds/minutes to verify communication.
  */
static void Probe_DS3231_RTC(void)
{
    uint8_t rtc_data[3] = {0};
    /* DS3231 seconds register starts at address 0x00 */
    uint8_t reg = 0x00;

    if (HAL_I2C_Master_Transmit(&hi2c1, (I2C_ADDR_DS3231_RTC << 1), &reg, 1, 50) == HAL_OK &&
        HAL_I2C_Master_Receive(&hi2c1, (I2C_ADDR_DS3231_RTC << 1), rtc_data, 3, 50) == HAL_OK)
    {
        /* Convert BCD to decimal */
        uint8_t sec = ((rtc_data[0] >> 4) * 10) + (rtc_data[0] & 0x0F);
        uint8_t min = ((rtc_data[1] >> 4) * 10) + (rtc_data[1] & 0x0F);
        uint8_t hrs = ((rtc_data[2] & 0x1F) >> 4) * 10 + (rtc_data[2] & 0x0F);

        char buf[80];
        snprintf(buf, sizeof(buf), "   -> [DS3231 OK] Current Clock: %02u:%02u:%02u\r\n", hrs, min, sec);
        UART_Log(buf);
    }
    else
    {
        UART_Log("   -> [DS3231 ERR] Failed to read registers!\r\n");
    }
}

/**
  * @brief  Write & Read test for AT24C32 EEPROM at Page 0 (Address 0x0000).
  */
static void Probe_AT24C32_EEPROM(void)
{
    uint8_t test_write[4] = {0x00, 0x00, 0xBE, 0xEF}; /* Word address 0x0000 + 2 data bytes */
    uint8_t test_read[2]  = {0};
    uint8_t addr_ptr[2]   = {0x00, 0x00};

    /* Write 0xBEEF */
    if (HAL_I2C_Master_Transmit(&hi2c1, (I2C_ADDR_AT24C32_EEPROM << 1), test_write, 4, 50) == HAL_OK)
    {
        HAL_Delay(10); /* EEPROM write cycle delay (tWR = 5ms max) */

        /* Set read pointer to 0x0000 */
        HAL_I2C_Master_Transmit(&hi2c1, (I2C_ADDR_AT24C32_EEPROM << 1), addr_ptr, 2, 50);
        /* Read 2 bytes */
        if (HAL_I2C_Master_Receive(&hi2c1, (I2C_ADDR_AT24C32_EEPROM << 1), test_read, 2, 50) == HAL_OK)
        {
            char buf[80];
            snprintf(buf, sizeof(buf), "   -> [AT24C32 OK] Write: 0xBEEF | Read: 0x%02X%02X (%s)\r\n",
                     test_read[0], test_read[1],
                     (test_read[0] == 0xBE && test_read[1] == 0xEF) ? "MATCH SUCCESS" : "MISMATCH");
            UART_Log(buf);
            return;
        }
    }
    UART_Log("   -> [AT24C32 ERR] EEPROM read/write transaction failed!\r\n");
}

/* ========================================================================== */
/* Standalone Bench Test Runner                                               */
/* ========================================================================== */

/**
  * @brief  Standalone test routine for Member 4.
  *         Scans all 7-bit addresses on I2C1 (PB8/PB9), highlights detected
  *         devices, and tests RTC & EEPROM sanity.
  */
void Test_I2C_Scanner_Run(void)
{
    char buf[128];
    UART_Log("\r\n=======================================================\r\n");
    UART_Log("🔍 Aquatic Guardian: Shared I2C1 Bus Address Scanner\r\n");
    UART_Log("   Target Bus: I2C1 Master | SCL = PB8 | SDA = PB9\r\n");
    UART_Log("=======================================================\r\n");

    uint8_t devices_found = 0;
    bool lcd_found = false;
    bool rtc_found = false;
    bool eeprom_found = false;

    for (uint8_t addr = 1; addr < 128; addr++)
    {
        /* HAL expects address shifted by 1 */
        HAL_StatusTypeDef status = HAL_I2C_IsDeviceReady(&hi2c1, (uint16_t)(addr << 1), 2, 5);

        if (status == HAL_OK)
        {
            devices_found++;
            const char *label = "Unknown I2C Device";

            if (addr == I2C_ADDR_LCD_PRIMARY || addr == I2C_ADDR_LCD_SECONDARY) {
                label = "LCD2004 PCF8574 Backpack (UI Display)";
                lcd_found = true;
            } else if (addr == I2C_ADDR_DS3231_RTC) {
                label = "DS3231 Precision Real-Time Clock";
                rtc_found = true;
            } else if (addr == I2C_ADDR_AT24C32_EEPROM) {
                label = "AT24C32 32-Kbit EEPROM (Feed Log Storage)";
                eeprom_found = true;
            }

            snprintf(buf, sizeof(buf), "[+] Found Device at 7-bit: 0x%02X (8-bit: 0x%02X) -> %s\r\n",
                     addr, (addr << 1), label);
            UART_Log(buf);
        }
    }

    UART_Log("-------------------------------------------------------\r\n");
    snprintf(buf, sizeof(buf), "Scan Summary: %u device(s) detected on I2C1 bus.\r\n", devices_found);
    UART_Log(buf);

    if (lcd_found && rtc_found && eeprom_found) {
        UART_Log("🎉 [PERFECT] All 3 Target Devices Successfully Identified!\r\n");
        HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET); /* Green LED ON */
    } else {
        UART_Log("⚠️ [WARNING] Some devices are missing. Check wiring & pull-ups.\r\n");
        if (!lcd_found)    UART_Log("   - MISSING: LCD PCF8574 (0x27 / 0x3F)\r\n");
        if (!rtc_found)    UART_Log("   - MISSING: DS3231 RTC (0x68)\r\n");
        if (!eeprom_found) UART_Log("   - MISSING: AT24C32 EEPROM (0x57)\r\n");
    }

    /* Perform probe tests if devices detected */
    if (rtc_found)    Probe_DS3231_RTC();
    if (eeprom_found) Probe_AT24C32_EEPROM();

    UART_Log("=======================================================\r\n");
}
