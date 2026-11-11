# 🔌 Aquatic Guardian — Hardware Wiring & Conflict-Free Pin Mapping Guide

> Target MCU: **ST Nucleo-F401RE / Nucleo-F411RE / Nucleo-F429ZI** (STM32F4 series)

---

## 📌 1. Conflict-Free Pin Mapping Table

| Peripheral | Sensor / Module | Signal / Pin | Nucleo Header Pin | STM32 Alternate Function | Electrical Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ADC1_IN1** | Analog TDS Sensor | Signal (AOUT) | **`PA1`** (A1) | Analog In | 0 – 3.3V linear range; 0.1µF capacitor to GND for noise filtering |
| **ADC1_IN4** | Dosage Potentiometer | Wiper (Center) | **`PA4`** (A2) | Analog In | 10kΩ Potentiometer between 3.3V and GND |
| **GPIO / 1-Wire**| Waterproof DS18B20 | Data Signal | **`PA8`** (D7) | GPIO_Output_OD | 1-Wire protocol; requires 4.7kΩ pull-up resistor to 3.3V |
| **TIM2_CH1** | Servo Feeder (SG90) | Control Signal | **`PA0`** (A0) | AF1 (TIM2_CH1) | 50 Hz PWM (20ms period). Pulse: 1ms (0°) to 2ms (180°) |
| **GPIO Out** | Stepper 28BYJ-48 (Alt) | IN1 – IN4 | **`PB12–PB15`** | GPIO_Output | ULN2003 driver; completely avoids I2C pins `PB8`/`PB9` |
| **I2C1_SCL** | LCD2004 + DS3231 RTC | SCL | **`PB8`** (D15) | AF4 (I2C1_SCL) | Shared I2C Clock; Requires 4.7kΩ pull-up to 3.3V / 5V |
| **I2C1_SDA** | LCD2004 + DS3231 RTC | SDA | **`PB9`** (D14) | AF4 (I2C1_SDA) | Shared I2C Data; Requires 4.7kΩ pull-up to 3.3V / 5V |
| **USART1_TX** | ESP32 Wi-Fi Bridge | TX (to ESP RX) | **`PA9`** (D8) | AF7 (USART1_TX) | 115200 bps, 8N1; dedicated Wi-Fi serial communication |
| **USART1_RX** | ESP32 Wi-Fi Bridge | RX (from ESP TX)| **`PA10`** (D2) | AF7 (USART1_RX) | 115200 bps, 8N1; interrupts on idle frame |
| **USART2_TX** | ST-LINK USB VCP (PC) | TX (to PC) | **`PA2`** | AF7 (USART2_TX) | 115200 bps; ST-LINK Virtual COM Port on USB cable |
| **USART2_RX** | ST-LINK USB VCP (PC) | RX (from PC) | **`PA3`** | AF7 (USART2_RX) | 115200 bps; ST-LINK Virtual COM Port on USB cable |
| **EXTI13** | User Button (B1) | Push Button | **`PC13`** | GPIO Input | Active Low; debounced in software (300ms tick guard) |
| **GPIO Out** | Active Buzzer (3-Pin)| Control (I/O) | **`PB0`** (A3) | GPIO_Output | High = Buzzer ON; uses 3-pin module with onboard transistor (safe <1mA draw) |
| **GPIO Out** | Normal Status LED | Anode (+) | **`PA5`** (D13) | GPIO_Output | Nucleo Green User LED; High = Active Normal |
| **GPIO Out** | Warning Hazard LED | Anode (+) | **`PB1`** (D6) | GPIO_Output | Red LED with 330Ω current limiting resistor; High = Alert |
| **GPIO Out** | Pump / Aerator Relay | Relay IN | **`PB4`** (D5) | GPIO_Output | 5V Relay with H/L Jumper set to HIGH trigger (or Open-Drain mode) |

---

## ⚡ 2. Power Rail Distribution & Grounding Rules

> [!CAUTION]
> **Servo Motor & Relay Power Rule:**  
> Never power the SG90 Servo motor, 28BYJ-48 Stepper, or Relay coil directly from the STM32 3.3V or 5V regulator pin (VDD/E5V). Inductive kicks and motor surge currents will trigger MCU brown-out resets or damage the onboard LDO regulator.
> 
> **MB102 Dropout Warning:**  
> The MB102 breadboard power supply uses an AMS1117-5.0 regulator with a ~1.2V dropout. Always power the MB102 via a **9V–12V DC 5.5x2.1mm adapter** to guarantee clean 5.0V output for LCD and Servo!

### Wiring Topology:
1. **External 5V Power Supply (MB102 powered by 9V/12V DC):**
   * Supplies the **SG90 Servo Motor** (Red wire: +5V, Brown wire: GND).
   * Supplies the **Relay Coil** (VCC: +5V, GND: GND).
   * Supplies the **LCD 2004 / 1602 Backpack** (VCC: +5V for bright contrast & backlight).
   * Supplies the **3-Pin Buzzer Module** (VCC: +5V, GND: GND).
2. **STM32 Nucleo 3.3V Output:**
   * Supplies the **TDS Sensor VCC** (3.3V).
   * Supplies the **DS18B20 Temperature Sensor VCC** (with 4.7kΩ pull-up to 3.3V).
   * Supplies the **DS3231 RTC Module VCC** (**CRITICAL**: Power with 3.3V to prevent destructive trickle charging of non-rechargeable CR2032 batteries!).
   * Supplies the **Potentiometer Top Leg** (3.3V reference).
3. **Common Ground (GND):**
   * **MANDATORY**: Connect the GND of the External 5V Power Supply / MB102 to the STM32 Nucleo GND pin and ESP32 GND pin. Without a shared ground reference, PWM pulses, UART bytes, and ADC readings will suffer severe floating noise.

---

## 📐 3. Shared I2C1 Bus Architecture (LCD + RTC + EEPROM)

All three I2C peripherals share the same physical lines (`PB8` SCL, `PB9` SDA):

| Device | Default 7-bit I2C Address | Address in 8-bit STM32 HAL format | Accessing Tasks |
| :--- | :---: | :---: | :--- |
| **LCD2004 (PCF8574)** | `0x27` (or `0x3F`) | `0x4E` (`(0x27 << 1)`) | `Task_DisplayUI` (`osPriorityBelowNormal`) |
| **DS3231 Real-Time Clock** | `0x68` | `0xD0` (`(0x68 << 1)`) | `Task_DisplayUI` (`osPriorityBelowNormal`) |
| **AT24C32 EEPROM** | `0x57` | `0xAE` (`(0x57 << 1)`) | `Task_DispenserControl` (`osPriorityAboveNormal`) |

> **Priority Inheritance Verification**:  
> Because `Task_DispenserControl` (`osPriorityAboveNormal`) and `Task_DisplayUI` (`osPriorityBelowNormal`) both acquire `i2cBusMutex`, the FreeRTOS kernel will dynamically raise `Task_DisplayUI`'s priority when `Task_DispenserControl` attempts to log a feed timestamp, proving the Priority Inheritance mechanism during defense!

---

## ⏱️ 4. Timer Clock Calculations (TIM2_CH1 PWM 50Hz)

* **Timer Clock Source**: APB1 Timer Clock locked to **`84 MHz`** (on STM32F401RE / F411RE).
* **Prescaler (PSC)**: `83` $\implies f_{\text{cnt}} = \frac{84\,\text{MHz}}{83 + 1} = 1\,\text{MHz}$ ($1\,\mu\text{s}$ per tick).
* **Auto-Reload Register (ARR)**: `19999` $\implies T = \frac{19999 + 1}{1\,\text{MHz}} = 20{,}000\,\mu\text{s} = 20\,\text{ms}$ ($50\,\text{Hz}$).
* **Pulse Modulation (CCR1)**:
  * $0^\circ$ (Closed position): $\text{CCR1} = 1000$ ($1.0\,\text{ms}$).
  * $90^\circ$ (Dispense position): $\text{CCR1} = 1500$ ($1.5\,\text{ms}$).
  * $180^\circ$ (Max position): $\text{CCR1} = 2000$ ($2.0\,\text{ms}$).

---

## 🧪 5. Analog TDS DSP Math & Water Temperature

* **Temperature Compensation**:  
  $$V_{\text{comp}} = \frac{V_{\text{adc}}}{1.0 + 0.02 \times (T - 25.0)}$$
  *(where $T$ is read from Waterproof DS18B20 on `PA8` with 4.7kΩ pull-up).*
* **Exact Cubic TDS Polynomial**:  
  $$\text{TDS} = \left(133.42 \times V_{\text{comp}}^3 - 255.86 \times V_{\text{comp}}^2 + 857.39 \times V_{\text{comp}}\right) \times 0.5$$
* **20-Sample Circular Ring Buffer Filter**: Maintains an $O(1)$ running sum across 20 samples to filter water ripples and transient electrode noise.

---

## 🚦 6. FreeRTOS Concurrency & Byte Stack Allocation

* **Length-1 Non-Destructive Mailbox**: Implemented with `xQueueOverwrite()` (Producer) and `xQueuePeek()` (Consumers) to eliminate consumer task starvation.
* **Byte Stack Sizing**: CMSIS-RTOS v2 allocates stack in **bytes**:
  * `Task_SafetySupervisor`: **1024 bytes**
  * `Task_DispenserControl`: **1024 bytes**
  * `Task_SensorAcquisition`: **1024 bytes**
  * `Task_DisplayUI`: **2048 bytes** (supports `snprintf` buffer formatting)
  * `Task_Telemetry`: **2048 bytes** (supports JSON framing & UART buffers)
* **EXTI13 Debounce**: 300ms software tick guard in `PC13` ISR callback.
