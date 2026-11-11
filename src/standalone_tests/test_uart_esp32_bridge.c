/**
  ******************************************************************************
  * @file    test_uart_esp32_bridge.c
  * @brief   Aquatic Guardian - Standalone Bench Test for Member 5 (Duc Anh)
  *          Subsystem: Dual UART Architecture & ESP32 Wi-Fi Bridge
  *          Target MCU: STM32F401RE / F411RE / F429ZI Nucleo
  *          Peripherals:
  *            - USART1 on PA9 (TX) & PA10 (RX) @ 115200 bps -> ESP32 Co-Processor
  *            - USART2 on PA2 (TX) & PA3 (RX) @ 115200 bps -> PC ST-LINK VCP
  * @author  Group 7 - MCP201 Capstone Project
  ******************************************************************************
  * @how_to_use
  * 1. Connect STM32 to ESP32:
  *    - STM32 PA9  (USART1_TX) -> ESP32 RX (GPIO 16 or RX0)
  *    - STM32 PA10 (USART1_RX) -> ESP32 TX (GPIO 17 or TX0)
  *    - STM32 GND              -> ESP32 GND (Shared Common Ground!)
  *    (Loopback bench test: Connect PA9 directly to PA10 with a jumper wire).
  * 2. Connect Nucleo USB cable to PC (USART2 Virtual COM Port @ 115200 bps).
  * 3. Call Test_UART_ESP32_Bridge_Run() in main().
  * 4. Observe JSON telemetry packets framed by '~' and verify command parsing.
  ******************************************************************************
  */

#include "main.h"
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>

/* ========================================================================== */
/* Configuration & Protocol Constants                                         */
/* ========================================================================== */

#define UART_FRAME_DELIMITER    '~'
#define RX_BUFFER_SIZE          128U
#define TX_BUFFER_SIZE          256U

/* External HAL Handles */
extern UART_HandleTypeDef huart1; /* ESP32 Wi-Fi Bridge (PA9/PA10) */
extern UART_HandleTypeDef huart2; /* PC Debug Console (PA2/PA3)   */

/* RX State Machine Variables */
static char    rx_buffer[RX_BUFFER_SIZE];
static uint8_t rx_index = 0;
static bool    in_frame = false;
static bool    packet_ready = false;

/* ========================================================================== */
/* Helper Functions                                                           */
/* ========================================================================== */

static void PC_Log(const char *msg)
{
    HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), 100);
}

static void ESP32_SendFramedPacket(const char *json_payload)
{
    char frame[TX_BUFFER_SIZE];
    int len = snprintf(frame, sizeof(frame), "%c%s%c\r\n",
                       UART_FRAME_DELIMITER, json_payload, UART_FRAME_DELIMITER);
    if (len > 0)
    {
        HAL_UART_Transmit(&huart1, (uint8_t*)frame, (uint16_t)len, 100);
    }
}

/**
  * @brief  Processes incoming characters using '~' delimiter framing state machine.
  */
static void ProcessIncomingByte(char c)
{
    if (c == UART_FRAME_DELIMITER)
    {
        if (!in_frame)
        {
            /* Start of new frame */
            in_frame = true;
            rx_index = 0;
            rx_buffer[0] = '\0';
        }
        else
        {
            /* End of frame */
            in_frame = false;
            rx_buffer[rx_index] = '\0';
            packet_ready = true;
        }
    }
    else if (in_frame)
    {
        if (rx_index < (RX_BUFFER_SIZE - 1U))
        {
            rx_buffer[rx_index++] = c;
        }
        else
        {
            /* Buffer overflow prevention: discard frame */
            in_frame = false;
            rx_index = 0;
        }
    }
}

/* ========================================================================== */
/* Standalone Bench Test Runner                                               */
/* ========================================================================== */

/**
  * @brief  Standalone test routine for Member 5.
  *         Transmits simulated telemetry to ESP32 every 2 seconds,
  *         polls USART1 for incoming commands, and relays events to PC.
  */
void Test_UART_ESP32_Bridge_Run(void)
{
    char debug_msg[128];
    uint32_t last_tx_tick = 0;
    uint32_t packet_counter = 0;

    PC_Log("\r\n=======================================================\r\n");
    PC_Log("📡 Aquatic Guardian: Dual UART & ESP32 Bridge Test\r\n");
    PC_Log("   USART1 (PA9/PA10): ESP32 Wi-Fi Bridge @ 115200 bps\r\n");
    PC_Log("   USART2 (PA2/PA3):  PC ST-LINK Debug VCP @ 115200 bps\r\n");
    PC_Log("=======================================================\r\n");

    while (1)
    {
        uint32_t now = HAL_GetTick();

        /* 1. Periodic Telemetry Transmission (every 2000ms) */
        if (now - last_tx_tick >= 2000U)
        {
            last_tx_tick = now;
            packet_counter++;

            char json_telemetry[128];
            snprintf(json_telemetry, sizeof(json_telemetry),
                     "{\"id\":%lu,\"tds\":135.5,\"temp\":26.2,\"portion\":4,\"status\":0}",
                     (unsigned long)packet_counter);

            /* Send framed packet to ESP32 over USART1 */
            ESP32_SendFramedPacket(json_telemetry);

            snprintf(debug_msg, sizeof(debug_msg), "[TX -> ESP32] ~%s~\r\n", json_telemetry);
            PC_Log(debug_msg);
        }

        /* 2. Poll for incoming byte from ESP32 on USART1 */
        uint8_t rx_byte = 0;
        if (HAL_UART_Receive(&huart1, &rx_byte, 1, 10) == HAL_OK)
        {
            ProcessIncomingByte((char)rx_byte);
        }

        /* 3. Handle Completed Command Frame */
        if (packet_ready)
        {
            packet_ready = false;
            snprintf(debug_msg, sizeof(debug_msg), "[RX <- ESP32] Frame received: \"%s\"\r\n", rx_buffer);
            PC_Log(debug_msg);

            /* Parse Remote Commands */
            if (strstr(rx_buffer, "/feed") != NULL || strstr(rx_buffer, "FEED") != NULL)
            {
                PC_Log("   🎯 Command Recognized: [/feed] -> Triggering Feeder Dispenser!\r\n");
                HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET); /* Green LED Blink */
                HAL_Delay(100);
                HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_RESET);

                /* Send ACK back to ESP32 */
                ESP32_SendFramedPacket("{\"ack\":\"feed_ok\"}");
            }
            else if (strstr(rx_buffer, "/status") != NULL)
            {
                PC_Log("   📊 Command Recognized: [/status] -> Sending Immediate Status\r\n");
                ESP32_SendFramedPacket("{\"ack\":\"status\",\"tds\":135.5,\"pump\":1}");
            }
            else if (strstr(rx_buffer, "ping") != NULL)
            {
                PC_Log("   🏓 Command Recognized: [ping] -> Sending Pong ACK\r\n");
                ESP32_SendFramedPacket("{\"ack\":\"pong\"}");
            }
            else
            {
                PC_Log("   ❓ Unknown command payload received.\r\n");
            }
        }
    }
}
