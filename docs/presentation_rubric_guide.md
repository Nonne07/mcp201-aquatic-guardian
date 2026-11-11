# 🎤 Aquatic Guardian — Project Defense & Grading Rubric Guide
## MCP201 Final Capstone Presentation (30% Course Weight)

> **Team**: Group 7 | **Subject**: MCP201 Microcontroller Programming  
> **Platform**: STM32 Nucleo ARM Cortex-M4 · FreeRTOS

---

## 🏆 1. Mapping Aquatic Guardian to the Instructor Rubric

| Rubric Criteria | Weight | Aquatic Guardian Implementation | High-Score Talking Points |
| :--- | :---: | :--- | :--- |
| **System Architecture & Complexity** | 25% | 5 FreeRTOS Tasks with preemptive scheduling and priority hierarchy. Explicit byte stack sizing (**1024 bytes** core, **2048 bytes** Display/Telemetry). **Length-1 Non-Destructive Mailbox** (`xQueueOverwrite` + `xQueuePeek`) eliminating task starvation. | Explains priority ordering (`Safety > Dispenser > Sensor > Display > Telemetry`) and non-destructive mailbox peeking. |
| **Peripheral Integration (HAL)** | 25% | **ADC1** (PA1 TDS & PA4 Potentiometer), **TIM2_CH1 PWM** (PA0, PSC=83, ARR=19999 @ 84MHz APB1) / Stepper (**PB12–PB15**), **1-Wire DS18B20** (PA8 with 4.7kΩ pull-up), **Shared I2C1** (PB8/PB9: LCD2004 `0x27`, DS3231 `0x68`, AT24C32 `0x57`), **USART1** (PA9/PA10 ESP32 `~` framing), **USART2** (PA2/PA3 PC VCP), **EXTI13** (PC13 300ms debounce), **GPIO** (PB0 Buzzer, PA5 Green LED, PB1 Red LED, PB4 Relay). | All major STM32 peripherals from Chapters 5–9 are physically active, conflict-free, and integrated. |
| **RTOS Synchronization & Safety** | 25% | **`i2cBusMutex`** (Priority Inheritance between `Task_DispenserControl` AboveNormal logging EEPROM `0x57` and `Task_DisplayUI` BelowNormal), **`uartMutex`**, **`feedTriggerSem`** (Deferred Interrupt with 300ms software tick guard), Length-1 Mailbox. | Demonstrates understanding of race conditions, deadlocks, Priority Inheritance, and why `osDelay()` is required over `HAL_Delay()`. |
| **Live Demonstration & Q&A** | 25% | Live hardware demo showing: 1) Normal state on LCD2004 & telemetry, 2) Manual feed via button with EEPROM log, 3) TDS spike trigger alarm, 4) Portion potentiometer. | Crisp answers on Cortex-M4 NVIC, volatile flags, byte stack allocation, timer prescaler calculations, and cubic TDS DSP math. |

---

## 🎬 2. Live Hardware Demonstration Script (5-Minute Walkthrough)

### Step 1: Normal Operation (1 min)
* **Action**: Power on the Nucleo board with the external 5V rail connected.
* **Observation**:
  * Green Status LED (`PA5`) is ON.
  * LCD 2004 initializes and displays current water TDS (`TDS: 120ppm [O]`), water temperature from DS18B20 (`26.5C`), and portion setting.
  * Serial monitor on PC (`USART2` PA2/PA3) and Telegram Bot via ESP32 (`USART1` PA9/PA10) receive live JSON telemetry framed with `~` every 2 seconds.
  * Relay (`PB4`) is ON (water filter pump running).

### Step 2: Manual Feeder Trigger via EXTI (1.5 min)
* **Action**: Press the blue User Push-Button (`PC13`).
* **Observation**:
  * EXTI ISR instantly executes 300ms software tick debounce guard and signals `feedTriggerSem`.
  * `Task_DispenserControl` unblocks in thread context.
  * Servo motor smoothly turns 90° (CCR1 = 1500) to open the dispenser slot, waits 800ms, and returns to 0° (CCR1 = 1000).
  * `Task_DispenserControl` acquires `i2cBusMutex` and logs feed timestamp into AT24C32 EEPROM (`0x57`).
  * **Explain to Teacher**: *"Notice there is zero lag on the LCD or serial stream because the servo delay runs inside a dedicated worker task using `osDelay()`, never blocking the CPU or the ISR. Priority Inheritance prevents priority inversion on I2C1."*

### Step 3: Water Quality Hazard Simulation (1.5 min)
* **Action**: Submerge the TDS probe into a cup of salted water (TDS rises above 500 ppm), or turn the simulated potentiometer.
* **Observation**:
  * `Task_SafetySupervisor` detects `tds_ppm > 500`.
  * Buzzer (`PB0`) sounds an alarm, and the Red Hazard LED (`PB1`) flashes at 1Hz.
  * LCD 2004 updates status from `[O]` to `[!] HAZARD`.
  * Telemetry JSON status flag shifts to `3` (Critical), and ESP32 sends Telegram emergency alert.

### Step 4: Portion Control Calibration (1 min)
* **Action**: Rotate the 10kΩ potentiometer on `PA4`.
* **Observation**:
  * ADC1 dynamically samples channel 4; portion on LCD changes smoothly from `2g` to `12g`.
  * Shows ADC linearity and calibration logic without channel data register overwrite.

---

## ❓ 3. Top 7 Teacher Defense Questions & Model Answers

### Q1: *"Why did you use a Mutex for the I2C bus instead of a Binary Semaphore? How is Priority Inheritance demonstrated in your tasks?"*
> **Answer**: *"A Mutex is specifically designed for mutual exclusion and resource ownership. It implements **Priority Inheritance** to prevent priority inversion. In our system, two tasks of different priorities legitimately share I2C1: `Task_DisplayUI` (`osPriorityBelowNormal`) which updates the LCD2004 and reads the DS3231 RTC, and `Task_DispenserControl` (`osPriorityAboveNormal`) which writes feed event timestamps into the AT24C32 EEPROM (`0x57`). If `Task_DisplayUI` holds the bus and `Task_DispenserControl` requests it, the kernel temporarily boosts `Task_DisplayUI`'s priority to `AboveNormal`, ensuring it finishes quickly without being preempted by intermediate tasks (`Task_SensorAcquisition`). A Binary Semaphore has no concept of ownership or priority inheritance and cannot prevent this."*

### Q2: *"What happens if you call `HAL_Delay(1000)` inside one of your FreeRTOS tasks?"*
> **Answer**: *" `HAL_Delay()` spins the CPU in a `while` loop waiting for the SysTick counter, wasting clock cycles and blocking all tasks of equal or lower priority. Instead, we call `osDelay(1000)`, which tells the FreeRTOS scheduler to transition the calling task into the **Blocked state**, immediately freeing the CPU to execute other Ready tasks."*

### Q3: *"Why is the User Button handled via EXTI + Semaphore rather than polling in a task?"*
> **Answer**: *"Polling wastes CPU bandwidth checking a pin state every few milliseconds. By configuring `PC13` as an External Interrupt (EXTI), the hardware NVIC detects the falling edge instantly. To filter mechanical bounce, the ISR checks a 300ms software tick guard (`HAL_GetTick() - last_tick > 300`). The ISR does not execute heavy logic; it simply executes `osSemaphoreRelease()` and exits in $< 1\mu\text{s}$ (Deferred Interrupt Processing), leaving the motor delay to the thread context."*

### Q4: *"How did you prevent the I2C bus from colliding between the RTC, EEPROM, and LCD?"*
> **Answer**: *"All three devices share the same physical pins (`PB8` SCL and `PB9` SDA). While their 7-bit addresses differ (`0x27` for LCD2004, `0x68` for DS3231 RTC, and `0x57` for AT24C32 EEPROM), STM32 I2C hardware is single-threaded. By encapsulating all I2C calls within `osMutexAcquire(i2cBusMutexHandle, timeout)` and `osMutexRelease()`, we guarantee atomic bus transactions."*

### Q5: *"How did you configure the Hardware Timer for the Servo PWM across different clock speeds?"*
> **Answer**: *"The SG90 servo requires a 50Hz PWM frequency (a 20ms period). We locked the APB1 timer clock to 84MHz. We set the Prescaler (PSC) to `83` so the timer ticks at exactly 1MHz (1µs per tick). Then we set the Auto-Reload Register (ARR) to `19999` (yielding a 20,000µs = 20ms period). We modulate the pulse by writing `1000` (1ms = 0°) to `2000` (2ms = 180°) into the Capture/Compare Register (CCR1). If running on an STM32F429ZI with a 90MHz APB1 timer clock, `PSC` is simply set to `89`."*

### Q6: *"How do you calculate TDS PPM and why is a 20-sample ring buffer required?"*
> **Answer**: *"Water surface ripples cause raw ADC voltage to swing by $\pm 50\text{ ppm}$. We use a 20-sample circular moving average buffer with $O(1)$ running sum maintenance to stabilize readings. We then apply temperature compensation and the exact cubic polynomial: $V_{\text{comp}} = V_{\text{adc}} / [1.0 + 0.02(T - 25.0)]$ and $\text{TDS} = (133.42V_{\text{comp}}^3 - 255.86V_{\text{comp}}^2 + 857.39V_{\text{comp}}) \times 0.5$, reading $T$ from the waterproof DS18B20 on PA8."*

### Q7: *"Why use two separate UART channels instead of multiplexing on one?"*
> **Answer**: *"Multiplexing PC ST-LINK debugging and ESP32 Wi-Fi communications on a single UART port causes frame corruption, bus collisions, and debug garbage on IoT packets. We dedicate `USART2` (`PA2`/`PA3`) hardwired to the ST-LINK USB Virtual COM Port for PC debugging, and `USART1` (`PA9`/`PA10`) with `~` delimiter framing for the ESP32 Wi-Fi bridge, both protected by `uartMutex`."*

