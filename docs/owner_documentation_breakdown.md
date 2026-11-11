# 📘 Deep-Dive Analysis: Martin Quattrone's Final Project Thesis
## Insights, Lessons Learned, and Engineering Blueprint for Aquatic Guardian

> **Source Document**: `Memoria del Trabajo Final - Sistemas Embebidos - Martin Quattrone.docx` (Universidad de Buenos Aires, Dec 2023)  
> **Course**: Sistemas Embebidos (Led by Prof. Ariel Lutenberg, primary author of the ARM Cortex-M textbook used in MCP201)

---

## 🎯 1. Project Specifications & Requirements (SMART Analysis)

From Chapter 2 of the thesis, the project was evaluated against formal SMART requirements:

| Subsystem | Requirement ID | Requirement Specification | Original Status | MCP201 Strategy |
| :--- | :---: | :--- | :---: | :--- |
| **Sensors** | **1.1** | Measure water temperature ($0^\circ\text{C} - 85^\circ\text{C}$, $\pm 0.5^\circ\text{C}$) | ⚠️ Replaced | Potentiometer on `PA4` simulates analog temperature / portion. |
| **Sensors** | **1.2** | Measure Total Dissolved Solids ($0 - 999\text{ ppm}$, $\pm 1\text{ ppm}$) | ✅ Passed | Analog TDS sensor on `PA1` with 20-sample circular filter. |
| **Actuators** | **2.1** | Refillable food dispenser mechanism | ✅ Passed | Plastic bottle with dispenser slit attached to motor cap. |
| **Actuators** | **2.2** | Automatic scheduled dispensing | ✅ Passed | Driven by 28BYJ-48 Stepper or SG90 Servo (TIM2 PWM). |
| **LCD Display**| **3.1 – 3.4**| Display: 1) Clock, 2) Temp, 3) TDS ppm, 4) Next Feeding | ✅ Passed | 4-line LCD 2004 (or 1602 2-page) with PCF8574 I2C adapter. |
| **Connectivity**| **4.1 – 4.3**| ESP32 Wi-Fi + Access Point web config + Telegram Bot | ✅ Passed | ESP32 running `Esp32.ino` connected via USART2. |
| **Real-Time** | **5.1 – 5.2**| Internet NTP/TimeAPI sync + EEPROM persistent memory | ✅ Passed | DS3231 RTC + AT24C32 EEPROM for power-loss recovery. |

---

## ⚙️ 2. Hardware Design & Schematics

### 1. Mechanical Dispenser Innovation (Bottle-Cap Mount)
* **Design**: A small transparent cylindrical bottle with an opening/slit along the side.
* **Mounting**: The bottle cap is permanently glued to the motor shaft.
* **Operation**:
  * To refill: Simply unscrew the bottle from its cap, pour in fish pellets, and screw it back on.
  * To dispense: Stepper/Servo rotates 1 full turn ($360^\circ$ for stepper or $0^\circ \to 90^\circ \to 0^\circ$ for servo), causing pellets to drop into the tank when the slit faces downward.

```
       [ Stepper Motor Shaft / Servo Horn ]
                      |
             [ Glued Bottle Cap ]
                      |
             [ Screw-in Bottle ] ====> [ Feed Slit ] ---> 🐟 (Pellets drop)
```

### 2. Original Hardware Pinout vs. MCP201 Nucleo Pinout

| Peripheral | Thesis Original Pin (NUCLEO-F429ZI) | MCP201 Group 7 Pinout (F401RE / F411RE) | Electrical / Driver Notes |
| :--- | :--- | :--- | :--- |
| **TDS Sensor** | `A0` (PA3) | **`PA1`** (ADC1_IN1) | 0 – 3.3V analog input |
| **Potentiometer**| `A1` (PC0) | **`PA4`** (ADC1_IN4) | Analog simulated temperature / portion dial |
| **Stepper Motor**| `D9, D8, D7, D6` | **`PB8, PB9, PB14, PB15`** (or TIM2 `PA0` for Servo) | ULN2003 driver with external 5V/12V power |
| **RTC (DS1307/DS3231)**| `PB_10` (SCL), `PB_11` (SDA) | **`PB8`** (I2C1_SCL), **`PB9`** (I2C1_SDA) | I2C with 4.7kΩ pull-up resistors |
| **LCD Display**| 4-bit parallel GPIO (`D0–D5`) | **`PB8` / `PB9`** (Shared I2C via PCF8574) | Saves 6 GPIO pins by multiplexing on I2C bus |
| **ESP32 Wi-Fi** | `PE_7` (TX), `PE_8` (RX) | **`PA2`** (USART2_TX), **`PA3`** (USART2_RX) | 115200 bps, 8N1 serial protocol (`~` packet delimiter) |

---

## 💾 3. Non-Volatile EEPROM Memory Layout (AT24C32)

The Tiny RTC board includes an **AT24C32 EEPROM** organized in 32-byte pages. The author allocated persistent memory addresses to survive power outages:

| Page # | Memory Address | Configuration Data Stored | Size |
| :---: | :---: | :--- | :---: |
| **0 – 4** | `0x0000 – 0x0080` | **5 Scheduled Feeding Slots** (`HH:MM:SS` + Portion units) | $5 \times 32\text{ bytes}$ |
| **5** | `0x00A0` | **Temperature Safety Limits** (`MIN_TEMP` and `MAX_TEMP`) | 32 bytes |
| **6** | `0x00C0` | **TDS Safety Limits** (`MIN_PPM` and `MAX_PPM`) | 32 bytes |
| **7** | `0x00E0` | **Telegram Registered User ID** (Prevents unauthorized users) | 32 bytes |
| **8** | `0x0100` | **Wi-Fi SSID Name** | 32 bytes |
| **9** | `0x0120` | **Wi-Fi Password** | 32 bytes |
| **10** | `0x0140` | **RTC Time Zone String** (e.g. `GMT+7` / `Asia/Ho_Chi_Minh`) | 32 bytes |

---

## 🔄 4. UART Communication Protocol Between STM32 & ESP32

To avoid serial packet corruption, the thesis established a clean, custom ASCII framing protocol:
* **End-of-Frame Delimiter**: `~` (tilde) indicates the end of a transmission.
* **Parameter Delimiter**: `|` (vertical pipe) separates arguments.

### Supported Command Frames:
1. **Status Check**:
   * STM32 $\to$ ESP32: `status~`
   * ESP32 $\to$ STM32: `connected~` or `disconnected~`
2. **Wi-Fi Access Point Mode (Captive Portal)**:
   * If Wi-Fi fails, STM32 sends: `accesspoint~`
   * ESP32 hosts an AP named `FishTankGuardian` with a web portal for entering Wi-Fi credentials.
3. **HTTP GET / Time Sync**:
   * STM32 $\to$ ESP32: `get|https://www.timeapi.io/api/Time/current/zone?timeZone=Asia/Bangkok~`
   * ESP32 $\to$ STM32: JSON response with current time string.
4. **Telegram Commands Processed**:
   * `/start` $\to$ Registers user ID in EEPROM page 7.
   * `/feeder_feed <1..3>` $\to$ Dispenses 1 to 3 portions immediately.
   * `/feeder_set <slot 1..5> <HH:MM:SS> <units>` $\to$ Writes to EEPROM pages 0–4.
   * `/feeder_delete <slot>` $\to$ Clears feeding slot in EEPROM.
   * `/monitor_status` $\to$ Returns current Temp, TDS, and safety bounds.
   * `/monitor_set_tds_limits <min> <max>` $\to$ Updates TDS thresholds in EEPROM page 6.

---

## ⚠️ 5. Practical Pitfalls Encountered & How Our FreeRTOS Design Fixes Them

| Pitfall Encountered by Author (Thesis Section 4.1) | Author's Workaround in Mbed | Our Superior FreeRTOS Solution for MCP201 |
| :--- | :--- | :--- |
| **1. TDS Sensor Reading Jitter** | Water turbulence caused wild spikes ($\pm 50\text{ ppm}$). The author used an average of 20 samples. | Implement a **20-sample Ring Buffer Filter** inside `Task_SensorAcquisition`. Pushes clean data to `telemetryQueue`. |
| **2. Temperature Probe Breakdown** | Submersible DS18B20 failed and generated spurious high temps. Replaced by potentiometer. | Support both: ADC potentiometer as reliable calibration dial, plus conditional DS18B20 1-wire driver. |
| **3. Serial UART Collision** | RealTimeClock and TelegramBot both tried to send requests to ESP32 simultaneously, corrupting serial frames. | **`uartMutex`**: Wrap all UART transmissions in `osMutexAcquire(uartMutexHandle)` and `osMutexRelease()`. |
| **4. I2C Bus Contention** | LCD and Tiny RTC shared I2C pins, leading to lockups. | **`i2cBusMutex`**: Complete mutual exclusion prevents bus arbitration losses. |
| **5. CPU 100% Saturation** | While waiting for HTTP responses, the main polling loop burned clock cycles. | **`osDelay()` + Binary Semaphores**: Tasks block and release the CPU completely to the idle task or higher-priority threads. |

