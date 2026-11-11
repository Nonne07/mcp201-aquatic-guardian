# 👥 Aquatic Guardian — 5-Member Team Work Division
## Group 7 Engineering & Presentation Assignment Matrix (MCP201)

> **Course**: MCP201 — Microcontroller Programming (Semester 3)  
> **Team**: Group 7 (Class IC2005)  
> **Topic**: Aquatic Guardian (Smart Fish Tank Feeder & Water Purity Monitor)  
> **Project Weight**: 30% of Final Grade

---

## 🎖️ Member Roster & Assigned Roles

| Member | Student ID | Primary Engineering Domain | Presentation & Defense Role |
| :--- | :---: | :--- | :--- |
| **Nghiêm Hoàng Tùng (You)** | **SE211196** | **Team Leader & FreeRTOS Systems Architect** | System Architecture & RTOS Lead (Slides 1–4, Demo Lead) |
| **Hoàng Đức Mạnh** | **SE211191** | **Sensors & Analog Signal Processing Specialist** | Sensing Subsystem & Calibration (Slide 5, Probe Operator) |
| **Đỗ Khắc Lê Gia** | **SE211559** | **Actuation, Hardware & Power Engineering Lead** | Actuator, PWM & Power Design (Slide 6, Hardware Operator) |
| **Phạm Hồng Minh** | **SE211181** | **I2C Bus, RTC & Display UI Specialist** | Display HUD, I2C & Memory (Slide 7, LCD Presenter) |
| **Nguyễn Đức Anh** | **SE211485** | **IoT Telemetry, Telegram Bot & QA Lead** | IoT Telemetry, Testing & Conclusion (Slides 8–10, Video Lead) |

---

## 🛠️ SECTION 1: THE PROJECT (Engineering & Firmware Development)

### 1. Nghiêm Hoàng Tùng (You) — Team Lead & FreeRTOS Architect
* **Deliverables**:
  1. **STM32CubeMX Setup**: Generate base project (`.ioc`) on ST Nucleo-F401RE / F411RE / F429ZI with FreeRTOS CMSIS-RTOS v2 and move HAL Timebase to TIM5.
  2. **FreeRTOS Kernel Core**: Define the 5 tasks with explicit **byte stack sizes** (`1024 bytes` for Sensor/Dispenser/Safety, `2048 bytes` for Display/Telemetry to support `snprintf`), setting priorities (`Safety > Dispenser > Sensor > Display > Telemetry`).
  3. **Concurrency Primitives**: Implement `i2cBusMutex`, `uartMutex`, `feedTriggerSem` (Binary Semaphore), and the **Length-1 Non-Destructive Mailbox Queue** (`xQueueOverwrite` + `xQueuePeek`) to prevent consumer starvation.
  4. **Deferred Interrupt & Debounce**: Write `AquaticGuardian_OnButtonPressed_ISR(PC13)` with a **300ms software tick debounce guard** to prevent re-triggering during mechanical contact bounce.
  5. **Master Integration**: Merge all teammate modules into `main.c` / `aquatic_guardian_app.c` and manage Git repository.
* **Key Files**: `aquatic_guardian_app.c/.h`, `freertos.c`, `main.c`.

### 2. Hoàng Đức Mạnh — Sensors & Analog Signal Processing
* **Deliverables**:
  1. **ADC Dynamic Channel Polling**: Configure multi-channel ADC1 on `PA1` (TDS Sensor) and `PA4` (Potentiometer) using single-channel start/stop polling to prevent `ADC1->DR` register overwrite without DMA.
  2. **Water Temperature Driver**: Implement 1-Wire communication on `PA8` for the waterproof DS18B20 sensor (with DS3231 internal temperature register as backup).
  3. **20-Sample Ring Buffer Filter**: Implement the circular moving average filter from Quattrone's thesis to stabilize TDS readings against water surface ripples.
  4. **Exact TDS Math & Calibration**: Code the temperature-compensated cubic polynomial:  
     $$V_{\text{comp}} = \frac{V_{\text{adc}}}{1.0 + 0.02(T - 25.0)}, \quad \text{TDS} = \left(133.42V_{\text{comp}}^3 - 255.86V_{\text{comp}}^2 + 857.39V_{\text{comp}}\right) \times 0.5$$
  5. **Water Test Samples**: Prepare Cup A (Tap water $\sim 120\text{ ppm}$) and Cup B (Salted water $\sim 600\text{ ppm}$) for testing.
* **Key Files**: `tds_sensor.c/.h`, `ds18b20.c/.h`, `adc_dsp.c/.h`.

### 3. Đỗ Khắc Lê Gia — Actuation, Hardware & Power Engineering
* **Deliverables**:
  1. **Motor Actuation**: Configure TIM2_CH1 PWM on `PA0` (Prescaler `PSC=83`, Auto-reload `ARR=19999` for 84MHz APB1 timer clock) for 50Hz servo pulses (1ms = 0°, 1.5ms = 90°). Fallback: GPIO on `PB12–PB15` for 28BYJ-48 Stepper + ULN2003 (completely avoiding I2C pins `PB8`/`PB9`).
  2. **Mechanical Dispenser**: Build the bottle-cap mount (small plastic bottle with side slot glued to the motor horn/shaft).
  3. **Power Isolation Rail**: Build external 5V/12V rail with common ground to prevent MCU brownout resets when the motor turns.
  4. **Safety Circuits**: Wire Active 5V Buzzer (`PB0`), Red Hazard Alert LED (`PB1`), and Aquarium Filter Relay (`PB4`).
* **Key Files**: `servo_feeder.c/.h` / `stepper_motor.c/.h`, `hardware_wiring.md`.

### 4. Phạm Hồng Minh — I2C Bus, RTC & Display UI
* **Deliverables**:
  1. **LCD Driver**: Implement PCF8574 4-bit I2C driver on `I2C1` (`PB8` SCL, `PB9` SDA) for LCD 2004 or LCD 1602.
  2. **DS3231 RTC Reader & Single-Shot Guard**: Implement I2C communication to read real-time hours, minutes, and seconds. Enforce single-shot execution so scheduled feeds trigger `feedTriggerSem` only once per minute.
  3. **AT24C32 EEPROM Persistence**: Implement functions to read/write feeding schedules (pages 0–4) and feed event logs (`0x57`) on I2C1.
  4. **Priority Inheritance Integration**: Ensure both `Task_DisplayUI` (`osPriorityBelowNormal`) and `Task_DispenserControl` (`osPriorityAboveNormal`) acquire `i2cBusMutex`, demonstrating the priority inheritance mechanism.
* **Key Files**: `lcd_pcf8574.c/.h`, `ds3231_rtc.c/.h`, `eeprom_at24c32.c/.h`.

### 5. Nguyễn Đức Anh — IoT Telemetry, Telegram Bot & QA
* **Deliverables**:
  1. **Dedicated Dual UART Architecture**:
     * Implement `USART1` on `PA9`/`PA10` (115200 bps) with idle frame interrupts (`HAL_UARTEx_ReceiveToIdle_IT`) and `~` delimiter framing for the ESP32 Wi-Fi bridge.
     * Implement `USART2` on `PA2`/`PA3` for PC ST-LINK Virtual COM Port debug streaming.
  2. **ESP32 Telegram Bot Bridge**: Flash `Esp32.ino` to the ESP32 module, verifying `/feed`, `/status`, and emergency alert push notifications.
  3. **PC Serial Dashboard**: Create a lightweight Python/Serial terminal script to test commands when Wi-Fi is unavailable.
  4. **Stress & Failsafe Testing**: Enable `configCHECK_FOR_STACK_OVERFLOW = 2` to verify stack stability under stress.
  5. **Backup Video Recording**: Film and edit a crisp 2-minute 4K demonstration video of the working system.
* **Key Files**: `telemetry_uart.c/.h`, `Esp32.ino`, `demo_backup_video.mp4`.

---

## 🎤 SECTION 2: THE PRESENTATION & DEFENSE (30% Evaluation)

### 1. Slide Deck Speaking Segments (10 Minutes)
* **Tùng (You) — Slides 1–4 (2 min)**: Introduction, Problem Statement, System Block Diagram, FreeRTOS Preemptive Multitasking & Priority Matrix.
* **Đức Mạnh — Slide 5 (1.5 min)**: Sensor Subsystem, ADC Sampling Cycles, 20-Sample Ring Buffer Filter & Temperature Compensation Math.
* **Lê Gia — Slide 6 (1.5 min)**: Actuation Subsystem, PWM Timer Calculations (`PSC`/`ARR`), Motor Mount & Power Isolation.
* **Hồng Minh — Slide 7 (1.5 min)**: Shared I2C Bus Architecture, LCD HUD Layout, DS3231 RTC Sync & AT24C32 EEPROM Memory Map.
* **Đức Anh — Slides 8–10 (1.5 min)**: Dual UART Architecture, ESP32 Telegram Bot Commands, Reliability Testing & Conclusion.

### 2. Live Demo Responsibilities (2 Minutes)
1. **Normal State**: **Tùng & Gia** power on the system $\to$ Green LED ON, LCD displays live time and clean TDS reading, PC/Telegram receives telemetry.
2. **Manual Feed**: **Tùng & Đức Anh** trigger feed via blue button (`PC13` debounced) or Telegram `/feed` $\to$ Motor rotates dispenser slot $\to$ Food drops $\to$ Zero lag on LCD.
3. **Hazard Event**: **Mạnh** dips TDS probe into salted water ($> 500\text{ ppm}$) $\to$ Buzzer alarms, Red LED flashes, LCD alerts `[!] HAZARD`, Telegram receives alert.
4. **Portion Dial**: **Gia & Minh** rotate the potentiometer on `PA4` $\to$ Portion updates dynamically from $2\text{g} \to 12\text{g}$, proving ADC linearity.

### 3. Teacher Technical Q&A Defense Assignment
* **Tùng (You)**: Defends FreeRTOS Kernel, Task States, Context Switching, Deadlock Prevention, and **Priority Inheritance on `i2cBusMutex`** (between `Task_DispenserControl` and `Task_DisplayUI`).
* **Mạnh**: Defends ADC Dynamic Polling (preventing single-register overwrite), 12-bit Resolution, 1-Wire DS18B20 timing, and 20-sample digital filtering.
* **Gia**: Defends Timer Prescaler/ARR math ($84\text{MHz} \to 1\text{MHz} \to 50\text{ Hz}$), inductive flyback diodes, and common ground isolation.
* **Minh**: Defends I2C Protocol (Start/Stop, ACK/NACK, 7-bit addresses `0x27`/`0x68`/`0x57`), single-shot minute guard, and EEPROM page writing.
* **Đức Anh**: Defends Dual UART routing, asynchronous idle frame RX (`HAL_UARTEx_ReceiveToIdle_IT`), and stack watermark monitoring (`configCHECK_FOR_STACK_OVERFLOW = 2`).
