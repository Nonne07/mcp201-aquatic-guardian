/**
  ******************************************************************************
  * @file    aquatic_guardian_app.h
  * @brief   Aquatic Guardian - Smart Fish Tank Controller & Feeder
  *          Core FreeRTOS Application Architecture Header (v2.0 Conflict-Free)
  * @author  Nghiem Hoang Tung & Group 7 (MCP201)
  ******************************************************************************
  */

#ifndef AQUATIC_GUARDIAN_APP_H_
#define AQUATIC_GUARDIAN_APP_H_

#ifdef __cplusplus
extern "C" {
#endif

#include "main.h"
#include "cmsis_os2.h"
#include <stdint.h>
#include <stdbool.h>

/* ========================================================================== */
/* Configuration Constants & Thresholds                                       */
/* ========================================================================== */

#define TDS_SAFE_THRESHOLD_PPM       350.0f  /* Normal clean water ceiling    */
#define TDS_WARNING_THRESHOLD_PPM    450.0f  /* Water change recommended      */
#define TDS_DANGER_THRESHOLD_PPM     500.0f  /* Hazardous water pollution     */

#define TEMP_SAFE_MAX_CELSIUS        30.0f   /* Max safe fish temp            */
#define TEMP_DANGER_MAX_CELSIUS      32.0f   /* Overheat alert threshold      */

#define SERVO_FEED_ANGLE_OPEN        90      /* Degrees to dump food pellet   */
#define SERVO_FEED_ANGLE_CLOSED      0       /* Rest/closed position          */
#define SERVO_PWM_PERIOD_TICKS       20000   /* 20ms period at 1MHz timer clk */
#define SERVO_PULSE_MIN_TICKS        1000    /* 1.0ms pulse = 0 degrees       */
#define SERVO_PULSE_MAX_TICKS        2000    /* 2.0ms pulse = 180 degrees     */

#define TDS_FILTER_SAMPLE_COUNT      20      /* 20-sample Ring Buffer (Thesis)*/
#define SENSOR_MAILBOX_LENGTH        1       /* Length-1 non-destructive queue*/
#define TELEMETRY_BUFFER_SIZE        256

/* ========================================================================== */
/* Data Structures                                                            */
/* ========================================================================== */

typedef enum {
    WATER_STATUS_OPTIMAL = 0,
    WATER_STATUS_ACCEPTABLE,
    WATER_STATUS_WARNING,
    WATER_STATUS_CRITICAL
} WaterQualityStatus_t;

typedef enum {
    FEEDER_STATE_IDLE = 0,
    FEEDER_STATE_DISPENSING,
    FEEDER_STATE_JAMMED,
    FEEDER_STATE_MANUAL_TRIGGER
} FeederState_t;

/**
 * @brief Telemetry snapshot produced by Task_SensorAcquisition and consumed
 *        non-destructively by UI, Telemetry, and Safety Supervisor tasks.
 */
typedef struct {
    uint16_t              raw_tds_adc;
    float                 tds_voltage;
    float                 tds_ppm;
    uint16_t              raw_pot_adc;
    uint8_t               portion_grams;
    float                 water_temp_celsius;
    WaterQualityStatus_t  water_status;
    uint32_t              timestamp_sec;
} AquariumTelemetry_t;

/* ========================================================================== */
/* FreeRTOS Object Handles (Shared Externs)                                   */
/* ========================================================================== */

extern osThreadId_t         taskSensorHandle;
extern osThreadId_t         taskDispenserHandle;
extern osThreadId_t         taskDisplayHandle;
extern osThreadId_t         taskTelemetryHandle;
extern osThreadId_t         taskSafetyHandle;

extern osMutexId_t          i2cBusMutexHandle;
extern osMutexId_t          uartMutexHandle;
extern osSemaphoreId_t      feedTriggerSemHandle;
extern osMessageQueueId_t   telemetryQueueHandle;

/* ========================================================================== */
/* Exported Application Functions                                             */
/* ========================================================================== */

/**
 * @brief Initialize all RTOS objects (Tasks, Mutexes, Semaphores, Mailbox).
 *        Must be called from freertos.c or main.c prior to osKernelStart().
 */
void AquaticGuardian_Init(void);

/* FreeRTOS Task Entry Functions */
void Task_SensorAcquisition_Entry(void *argument);
void Task_DispenserControl_Entry(void *argument);
void Task_DisplayUI_Entry(void *argument);
void Task_Telemetry_Entry(void *argument);
void Task_SafetySupervisor_Entry(void *argument);

/* ISR Callbacks */
void AquaticGuardian_OnButtonPressed_ISR(uint16_t GPIO_Pin);

/* Hardware Driver Abstractions & I2C Peripherals */
uint16_t AquaticGuardian_ReadADCChannel(uint32_t channel);
float    AquaticGuardian_ReadWaterTemperature(void);
float    AquaticGuardian_CalculateTDS(uint16_t raw_adc, float temperature_c);
void     AquaticGuardian_SetServoAngle(uint8_t angle_deg);
void     AquaticGuardian_DispensePortion(uint8_t grams);
void     AquaticGuardian_SetAlarmState(bool active);
void     AquaticGuardian_SetRelayState(bool active);
bool     AquaticGuardian_LogFeedToEEPROM(uint32_t timestamp, uint8_t portion);

/* LCD2004 PCF8574 Backpack Driver */
void     AquaticGuardian_LCD_Init(void);
void     AquaticGuardian_LCD_SetCursor(uint8_t row, uint8_t col);
void     AquaticGuardian_LCD_Print(const char *str);

/* DS3231 RTC Driver */
bool     AquaticGuardian_DS3231_ReadTime(uint8_t *hrs, uint8_t *min, uint8_t *sec);

#ifdef __cplusplus
}
#endif

#endif /* AQUATIC_GUARDIAN_APP_H_ */
