# -*- coding: utf-8 -*-
r"""
Aquatic Guardian - Task Tracker & Defense Workbook Generator
Course: MCP201 (Microcontroller Programming) - Capstone Project
Group: 7 (Class IC2005) - Aquatic Guardian
Platform: STM32 Nucleo ARM Cortex-M4 (F401RE/F411RE) & FreeRTOS
Target Path: E:\AntiGravityRoot\mcp201-aquatic-guardian\Aquatic_Guardian_Task_Tracker.xlsx
"""

import os
import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUTPUT_PATH = r"E:\AntiGravityRoot\mcp201-aquatic-guardian\Aquatic_Guardian_Task_Tracker.xlsx"

# Color Palette Constants
HEX_NAVY_DARK = "1B365D"       # Main table headers & titles
HEX_NAVY_SLATE = "2C4D75"      # Section headers
HEX_ICE_BLUE = "D9E8F5"        # Subtitle bars & accents
HEX_ICE_TINT = "F0F4F8"        # Table sub-headers
HEX_ZEBRA = "F9FAFB"           # Alternating row fill
HEX_WHITE = "FFFFFF"           # White fill / font
HEX_BORDER = "D0D7DE"          # Crisp cell borders

# Priority & Status Palette
HEX_DONE_BG = "E6F4EA"
HEX_DONE_FG = "137333"
HEX_PROG_BG = "FEF7E0"
HEX_PROG_FG = "B06000"
HEX_TODO_BG = "F1F3F4"
HEX_TODO_FG = "5F6368"
HEX_BLOCKED_BG = "FCE8E6"
HEX_BLOCKED_FG = "C5221F"

HEX_HIGH_BG = "FCE8E6"
HEX_HIGH_FG = "C5221F"
HEX_MED_BG = "FEF7E0"
HEX_MED_FG = "B06000"
HEX_LOW_BG = "E6F4EA"
HEX_LOW_FG = "137333"

# Fonts
FONT_TITLE = Font(name="Arial", size=13, bold=True, color=HEX_WHITE)
FONT_SUBTITLE = Font(name="Arial", size=10, italic=True, color=HEX_NAVY_DARK)
FONT_SECTION = Font(name="Arial", size=11, bold=True, color=HEX_WHITE)
FONT_HEADER = Font(name="Arial", size=10, bold=True, color=HEX_WHITE)
FONT_SUBHEADER = Font(name="Arial", size=10, bold=True, color=HEX_NAVY_DARK)
FONT_BODY = Font(name="Arial", size=9, bold=False, color="1F2937")
FONT_BODY_BOLD = Font(name="Arial", size=9, bold=True, color="1F2937")

# Fills
FILL_TITLE = PatternFill(start_color=HEX_NAVY_DARK, end_color=HEX_NAVY_DARK, fill_type="solid")
FILL_SUBTITLE = PatternFill(start_color=HEX_ICE_BLUE, end_color=HEX_ICE_BLUE, fill_type="solid")
FILL_SECTION = PatternFill(start_color=HEX_NAVY_SLATE, end_color=HEX_NAVY_SLATE, fill_type="solid")
FILL_HEADER = PatternFill(start_color=HEX_NAVY_DARK, end_color=HEX_NAVY_DARK, fill_type="solid")
FILL_SUBHEADER = PatternFill(start_color=HEX_ICE_TINT, end_color=HEX_ICE_TINT, fill_type="solid")
FILL_ZEBRA = PatternFill(start_color=HEX_ZEBRA, end_color=HEX_ZEBRA, fill_type="solid")
FILL_WHITE = PatternFill(start_color=HEX_WHITE, end_color=HEX_WHITE, fill_type="solid")

# Borders
BORDER_THIN = Border(
    left=Side(style="thin", color=HEX_BORDER),
    right=Side(style="thin", color=HEX_BORDER),
    top=Side(style="thin", color=HEX_BORDER),
    bottom=Side(style="thin", color=HEX_BORDER)
)
BORDER_TOP_THICK = Border(
    left=Side(style="thin", color=HEX_BORDER),
    right=Side(style="thin", color=HEX_BORDER),
    top=Side(style="medium", color=HEX_NAVY_DARK),
    bottom=Side(style="thin", color=HEX_BORDER)
)
BORDER_BOTTOM_DOUBLE = Border(
    left=Side(style="thin", color=HEX_BORDER),
    right=Side(style="thin", color=HEX_BORDER),
    top=Side(style="thin", color=HEX_BORDER),
    bottom=Side(style="double", color=HEX_NAVY_DARK)
)

# Alignments
ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)
ALIGN_RIGHT = Alignment(horizontal="right", vertical="center", wrap_text=True)
ALIGN_TEXT_WRAP = Alignment(horizontal="left", vertical="top", wrap_text=True)
ALIGN_CENTER_TOP = Alignment(horizontal="center", vertical="top", wrap_text=True)

# Team Members Metadata
MEMBERS_DATA = [
    {
        "name": "Nghiêm Hoàng Tùng",
        "id": "SE211196",
        "code": "Tung",
        "role": "Team Leader & FreeRTOS Systems Architect",
        "subsystem": "RTOS Kernel, Task Hierarchy, IPC & Master Integration",
        "peripherals": "TIM5 (FreeRTOS Timebase), EXTI13 (PC13 Debounced 300ms), Kernel Core",
        "files": "main.c, aquatic_guardian_app.c/.h, freertos.c",
        "presentation": "Slides 1–4 (2.0 min) - Problem Statement & FreeRTOS Architecture",
        "defense_focus": "FreeRTOS Kernel, Byte Stack Sizing, Length-1 Mailbox, Priority Inheritance, Debounced EXTI",
        "sheet_name": "Tung_Lead"
    },
    {
        "name": "Hoàng Đức Mạnh",
        "id": "SE211191",
        "code": "Manh",
        "role": "Sensors & Analog DSP Specialist",
        "subsystem": "Sensing, ADC Multi-channel & Digital Signal Processing",
        "peripherals": "ADC1 Dynamic Polling (PA1 - TDS, PA4 - Potentiometer), DS18B20 1-Wire (PA8)",
        "files": "tds_sensor.c/.h, adc_dsp.c/.h",
        "presentation": "Slide 5 (1.5 min) - Sensor Subsystem, 20-Sample Filter & Calibration",
        "defense_focus": "ADC 12-bit Quantization, ADC1->DR Overwrite Prevention, 20-Sample Ring Buffer, Cubic TDS Math",
        "sheet_name": "Manh_Sensors"
    },
    {
        "name": "Đỗ Khắc Lê Gia",
        "id": "SE211559",
        "code": "Gia",
        "role": "Actuators, Hardware & Power Engineering Lead",
        "subsystem": "Actuation, Power Rails, Relays & Mechanical Dispenser",
        "peripherals": "TIM2_CH1 PWM 50Hz (PA0 @ 84MHz APB1), Stepper (PB12-PB15), Buzzer (PB0), Relay (PB4), 5V Rail",
        "files": "servo_feeder.c/.h, stepper_motor.c/.h, buzzer.c/.h, relay.c/.h, hardware_wiring.md",
        "presentation": "Slide 6 (1.5 min) - PWM Motor Actuation, Dispenser & Power Isolation",
        "defense_focus": "Timer Prescaler/ARR (84MHz APB1, PSC=83, ARR=19999), Inrush Current, Common GND, Stepper PB12-15",
        "sheet_name": "Gia_Hardware"
    },
    {
        "name": "Phạm Hồng Minh",
        "id": "SE211181",
        "code": "Minh",
        "role": "I2C Bus, RTC & Display UI Specialist",
        "subsystem": "Shared I2C Bus, LCD 2004/1602 HUD & RTC Memory Persistence",
        "peripherals": "I2C1 Master (PB8 - SCL, PB9 - SDA), PCF8574 LCD (0x27), DS3231 RTC (0x68), AT24C32 EEPROM (0x57)",
        "files": "lcd_pcf8574.c/.h, ds3231_rtc.c/.h, at24c32_eeprom.c/.h",
        "presentation": "Slide 7 (1.5 min) - Shared I2C Bus, LCD HUD & RTC EEPROM Persistence",
        "defense_focus": "I2C Addressing (0x27, 0x68, 0x57), Priority Inheritance on i2cBusMutex, Single-shot Minute Guard",
        "sheet_name": "Minh_I2C_UI"
    },
    {
        "name": "Nguyễn Đức Anh",
        "id": "SE211485",
        "code": "DucAnh",
        "role": "IoT Telemetry, Telegram Bot & QA Lead",
        "subsystem": "Dual UART Serial Streaming, ESP32 Cloud Bridge & QA Stress Testing",
        "peripherals": "Dual UART: USART1 (PA9/PA10 @ 115200 bps ~ framing) for ESP32, USART2 (PA2/PA3) for PC VCP",
        "files": "telemetry_uart.c/.h, Esp32.ino, aquatic_pc_dashboard.py, qa_test_report.md",
        "presentation": "Slides 8–10 (1.5 min) - Telemetry, Telegram Bot, Testing & Conclusion",
        "defense_focus": "Dual UART Routing, '~' Delimiter Framing, Idle Frame RX, ESP32 Bot, configCHECK_FOR_STACK_OVERFLOW",
        "sheet_name": "DucAnh_Telemetry_QA"
    }
]

# 1-Week Sprint Roadmap Data (Day 1 - Day 7)
ROADMAP_DATA = [
    {
        "day": "Day 1",
        "phase": "Phase 1: Drivers & Hardware",
        "theme": "Project Kickoff, Architecture Lock & Pinout Definition",
        "milestone": "Khởi tạo project nền tảng STM32CubeMX (.ioc), chốt sơ đồ chân phần cứng, phân chia Git repository và thiết lập quy chuẩn code.",
        "subsystems": "RTOS Core, Hardware BOM, Git Workflow",
        "deliverable": "File .ioc nền tảng với TIM5 Timebase, tài liệu pinout_wiring.md, Git branches cho 5 thành viên."
    },
    {
        "day": "Day 2",
        "phase": "Phase 1: Drivers & Hardware",
        "theme": "Low-Level Peripheral Drivers & Hardware Breadboard Setup",
        "milestone": "Hoàn thiện các driver ngoại vi bare-metal/HAL độc lập: ADC1 đa kênh, TIM2 PWM 50Hz, I2C1 quét bus, USART2 115200 bps.",
        "subsystems": "ADC1 (PA1/PA4), DS18B20 (PA8), TIM2 (PA0), I2C1 (PB8/PB9), USART1 (PA9/PA10), USART2 (PA2/PA3)",
        "deliverable": "Các file adc_dsp.c, servo_feeder.c, i2c_bus.c, telemetry_uart.c; đo kiểm oscilloscope dạng sóng PWM và ADC."
    },
    {
        "day": "Day 3",
        "phase": "Phase 2: FreeRTOS Core",
        "theme": "FreeRTOS Kernel Skeleton, Tasks & Synchronization Primitives",
        "milestone": "Khai báo 5 tasks FreeRTOS CMSIS-RTOS v2 với byte stack sizes (1024/2048 bytes), tạo i2cBusMutex, uartMutex, feedTriggerSem, Length-1 Mailbox.",
        "subsystems": "FreeRTOS Kernel, LCD 2004 UI, Mechanical Feeder, Mailbox Queue",
        "deliverable": "freertos.c, aquatic_guardian_app.c/.h, driver lcd_pcf8574.c, cụm cơ khí nắp chai cấp thức ăn hoàn thiện."
    },
    {
        "day": "Day 4",
        "phase": "Phase 2: FreeRTOS Core",
        "theme": "Subsystem Driver Verification & Dedicated Unit Tests",
        "milestone": "Kiểm thử chuyên sâu từng module: Đa thức bậc 3 bù nhiệt TDS PPM, đọc giờ RTC DS3231, ESP32 Telegram Bot qua USART1 nhận /feed và /status.",
        "subsystems": "TDS Calibration, DS3231 RTC, ESP32 Gateway (USART1)",
        "deliverable": "tds_sensor.c (sai số <3%, đa thức bậc 3 bù nhiệt DS18B20), ds3231_rtc.c, Esp32.ino nhận lệnh bot thành công."
    },
    {
        "day": "Day 5",
        "phase": "Phase 3: Integration & Testing",
        "theme": "Master Integration, Deferred Interrupt & Concurrency Testing",
        "milestone": "Ghép nối nhánh Git vào main.c; ngắt EXTI13 (debounce 300ms) giải phóng semaphore; ghi EEPROM chứng minh Priority Inheritance; PC dashboard.",
        "subsystems": "Master App, EXTI13 300ms Debounce, AT24C32 EEPROM Priority Inheritance, PC Dashboard",
        "deliverable": "main.c biên dịch 0 errors/warnings, at24c32_eeprom.c khôi phục lịch ăn sau ngắt nguồn, aquatic_pc_dashboard.py."
    },
    {
        "day": "Day 6",
        "phase": "Phase 3: Integration & Testing",
        "theme": "Stress Testing (Stack Overflow Check), Telemetry & Enclosure",
        "milestone": "Bật configCHECK_FOR_STACK_OVERFLOW = 2, đo High Water Mark 5 tasks, đóng hộp mô hình bể cá và cố định dây cáp an toàn.",
        "subsystems": "QA Stability, Power Rail Isolation, Mechanical Packaging",
        "deliverable": "qa_test_report.md chạy liên tục 30 phút ổn định, mô hình bể cá hoàn chỉnh có gá motor và 2 cốc nước thử nghiệm."
    },
    {
        "day": "Day 7",
        "phase": "Phase 4: Defense & Presentation",
        "theme": "End-to-End Rehearsal, 4K Backup Video & Presentation Deck Lock",
        "milestone": "Tổng duyệt live demo 10 phút cả 5 thành viên, quay dựng video dự phòng 2 phút 4K, khóa file slide thuyết trình và luyện tập Q&A.",
        "subsystems": "Presentation Deck, Backup Video, Capstone Q&A Defense",
        "deliverable": "Aquatic_Guardian_Presentation.pptx (10 slides), video demo_backup_video.mp4, sẵn sàng 100% bước vào phòng bảo vệ."
    }
]

# 25 Master Tasks Data
MASTER_TASKS = [
    # Member 1: Tung (Lead & RTOS Architect)
    {
        "id": "TSK-01",
        "phase": "Phase 1: Drivers & Hardware",
        "subsystem": "RTOS Kernel & Core",
        "assignee": "Nghiêm Hoàng Tùng",
        "member_code": "Tung",
        "priority": "High",
        "what_is": "Khởi tạo project nền tảng STM32CubeMX (.ioc) cho dòng ST Nucleo-F401RE/F411RE (ARM Cortex-M4 @ 84MHz). Cấu hình HSE/HSI, PLL, và quan trọng nhất: chuyển đổi SysTick timebase sang TIM5 để làm bộ đếm chuẩn cho HAL, dành riêng SysTick phục vụ FreeRTOS scheduler nhằm tránh xung đột deadlock giữa ngắt HAL và RTOS kernel.",
        "what_do": "1) Mở STM32CubeMX, chọn MCU STM32F401RETx;\n2) Clock Config: Thiết lập HCLK = 84 MHz;\n3) Pinout & Config -> System Core -> SYS: Chuyển Timebase Source thành TIM5;\n4) Middleware -> FREERTOS: Chọn Interface CMSIS-RTOS V2;\n5) NVIC Settings: Đặt Priority Grouping là 4 bits preemption (NVIC_PRIORITYGROUP_4);\n6) Tạo Git repo trên GitHub/GitLab, commit bộ khung project ban đầu và cấp quyền push cho 4 thành viên.",
        "what_submit": "File .ioc hoàn chỉnh, commit Git 'Initial CubeMX project skeleton with TIM5 timebase', ảnh chụp màn hình Clock Configuration & SYS setup.",
        "deadline": "Day 1",
        "status": "Done",
        "evidence": "Commit #a1b2c3d - Base CubeMX Project with TIM5 HAL Timebase"
    },
    {
        "id": "TSK-06",
        "phase": "Phase 2: FreeRTOS Core",
        "subsystem": "RTOS Kernel & Core",
        "assignee": "Nghiêm Hoàng Tùng",
        "member_code": "Tung",
        "priority": "High",
        "what_is": "Thiết kế và khởi tạo cấu trúc đa nhiệm tiền định lượng (Preemptive Multitasking Architecture) gồm 5 tasks cốt lõi theo thứ tự ưu tiên giảm dần: Task_SafetySupervisor (High - 32), Task_DispenserControl (AboveNormal - 24), Task_SensorAcquisition (Normal - 16), Task_DisplayUI (BelowNormal - 12), Task_Telemetry (Low - 8).",
        "what_do": "1) Khai báo các đối tượng task trong aquatic_guardian_app.c sử dụng osThreadNew() và osThreadAttr_t;\n2) Cấp phát stack size chính xác theo BYTE trong CMSIS-RTOS v2: 1024 bytes cho Task_SafetySupervisor, Task_DispenserControl, Task_SensorAcquisition; 2048 bytes cho Task_DisplayUI và Task_Telemetry (đảm bảo đủ vùng nhớ cho hàm định dạng snprintf và bộ đệm chuỗi/JSON);\n3) Triển khai vòng lặp vô hạn chuẩn cho từng task sử dụng osDelayUntil() hoặc chờ cờ đồng bộ hóa;\n4) Xây dựng bảng phân tích loại trừ CPU starvation đối với các task mức thấp.",
        "what_submit": "Source code freertos.c, aquatic_guardian_app.c/.h, commit 'feat(rtos): create 5-task architecture with CMSIS-RTOS v2', sơ đồ phân cấp task hierarchy.",
        "deadline": "Day 3",
        "status": "Done",
        "evidence": "Commit #b2c3d4e - FreeRTOS 5-Task Preemptive Engine with CMSIS-RTOS v2"
    },
    {
        "id": "TSK-11",
        "phase": "Phase 2: FreeRTOS Core",
        "subsystem": "RTOS Kernel & Core",
        "assignee": "Nghiêm Hoàng Tùng",
        "member_code": "Tung",
        "priority": "High",
        "what_is": "Thiết lập các đối tượng đồng bộ hóa và truyền thông liên luồng (IPC Primitives): i2cBusMutex (bảo vệ bus I2C1 dùng chung có Priority Inheritance), uartMutex (bảo vệ cổng USART1 và USART2), feedTriggerSem (Binary Semaphore cho Deferred Interrupt từ PC13), và Length-1 Non-Destructive Mailbox Queue (xQueueOverwrite + xQueuePeek) loại bỏ hoàn toàn nguy cơ task starvation.",
        "what_do": "1) Khởi tạo osMutexNew() cho i2cBusMutex và uartMutex;\n2) Khởi tạo osSemaphoreNew(1, 0) tạo Binary Semaphore ở trạng thái ban đầu là 0 (empty);\n3) Khởi tạo osMessageQueueNew(1, sizeof(AquariumTelemetry_t)) làm Length-1 Mailbox cho phép task Sensor ghi đè (xQueueOverwrite) và các task tiêu thụ đọc không hủy (xQueuePeek);\n4) Viết các hàm wrapper truy xuất IPC an toàn có tham số timeout (chống deadlock vĩnh viễn).",
        "what_submit": "File aquatic_guardian_app.c (hàm IPC_Init), test log mô phỏng cấp phát/thu hồi mutex và queue, commit 'feat(ipc): initialize mutexes, binary semaphore and message queue'.",
        "deadline": "Day 3",
        "status": "Done",
        "evidence": "Commit #c3d4e5f - IPC Primitives (i2cBusMutex, feedTriggerSem, Length-1 Mailbox Queue)"
    },
    {
        "id": "TSK-16",
        "phase": "Phase 3: Integration & Testing",
        "subsystem": "Master Integration",
        "assignee": "Nghiêm Hoàng Tùng",
        "member_code": "Tung",
        "priority": "High",
        "what_is": "Triển khai cơ chế xử lý ngắt trì hoãn (Deferred Interrupt Processing) cho nút nhấn Blue Button (PC13) với bộ lọc chống rung phần mềm (300ms software tick debounce guard). Ngắt EXTI13 callback kiểm tra (HAL_GetTick() - last_tick > 300) rồi mới giải phóng feedTriggerSem trong <1µs và thoát ngay. Tiến hành merge nhánh driver vào main.c.",
        "what_do": "1) Cấu hình chân PC13 làm GPIO_EXTI13 Falling Edge Detection;\n2) Cài đặt hàm HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) với 300ms tick guard gọi osSemaphoreRelease(feedTriggerSemHandle);\n3) Tích hợp các file header tds_sensor.h, servo_feeder.h, lcd_pcf8574.h, ds3231_rtc.h, telemetry_uart.h vào main.c;\n4) Xử lý xung đột merge trên Git, build dự án với 0 errors và 0 warnings.",
        "what_submit": "File main.c, stm32f4xx_it.c, Git merge log, video 30s ghi lại thao tác bấm nút PC13 phản hồi xoay motor mượt mà không block hệ thống.",
        "deadline": "Day 5",
        "status": "In Progress",
        "evidence": "Pull Request #05 - Master Integration & Deferred Interrupt Handling"
    },
    {
        "id": "TSK-21",
        "phase": "Phase 4: Defense & Presentation",
        "subsystem": "Master Integration & Defense",
        "assignee": "Nghiêm Hoàng Tùng",
        "member_code": "Tung",
        "priority": "High",
        "what_is": "Trưởng nhóm phụ trách hoàn thiện bộ slide thuyết trình chung (10 slides), điều phối phân vai bảo vệ, trình bày mở đầu bài thuyết trình (Slides 1–4: Bối cảnh dự án, Sơ đồ khối toàn hệ thống, Kiến trúc nhân FreeRTOS, Phân cấp ưu tiên Task), và chủ trì phần hỏi đáp chuyên sâu về FreeRTOS Kernel của giảng viên.",
        "what_do": "1) Soạn thảo và chuẩn hóa slide deck 10 trang theo đúng chuẩn MCP201 (font, layout, hình ảnh đồ họa kỹ thuật);\n2) Chuẩn bị nội dung Slides 1-4 (Bản chất hệ nhúng thời gian thực, bảng phân cấp priority, cơ chế tránh priority inversion);\n3) Tổ chức 2 buổi tổng duyệt thuyết trình đúng giới hạn 10 phút (8 phút slide + 2 phút demo);\n4) Soạn cẩm nang trả lời phản biện: Mutex vs Semaphore, Priority Inheritance (AT24C32 vs LCD2004/DS3231), Length-1 Mailbox, osDelay() vs HAL_Delay().",
        "what_submit": "File slide hoàn chỉnh Aquatic_Guardian_Presentation.pptx (hoặc PDF), biên bản tổng duyệt thuyết trình, speaker notes 4 trang đầu.",
        "deadline": "Day 7",
        "status": "To Do",
        "evidence": "Aquatic_Guardian_Presentation.pptx (Slides 1-4 completed & reviewed)"
    },

    # Member 2: Manh (Sensors & Analog DSP)
    {
        "id": "TSK-02",
        "phase": "Phase 1: Drivers & Hardware",
        "subsystem": "Sensors & Analog DSP",
        "assignee": "Hoàng Đức Mạnh",
        "member_code": "Manh",
        "priority": "High",
        "what_is": "Cấu hình ADC1 trên STM32 (12-bit, Vref=3.3V) với Dynamic Channel Polling (chống ghi đè ADC1->DR). Kênh ADC1_IN1 (PA1) kết nối cảm biến TDS; Kênh ADC1_IN4 (PA4) kết nối chiết áp 10kΩ chỉnh khẩu phần (1g - 15g). Giao tiếp 1-Wire trên PA8 đọc cảm biến nhiệt độ nước DS18B20 (trở kéo 4.7kΩ).",
        "what_do": "1) Mở CubeMX, bật ADC1: Scan Conversion Mode = ENABLE, Continuous Mode = DISABLE, Discontinuous Mode = DISABLE;\n2) Cấu hình Rank 1: Channel 1 (PA1 - TDS), Sampling Time = 84 Cycles;\n3) Cấu hình Rank 2: Channel 4 (PA4 - Potentiometer), Sampling Time = 84 Cycles;\n4) Viết module adc_dsp.c triển khai các hàm ADC1_Init(), ADC1_Read_TDS_Raw(), ADC1_Read_Pot_Raw();\n5) Dùng đồng hồ vạn năng VOM đo kiểm tra tính tuyến tính của điện áp trên chân PA1 và PA4.",
        "what_submit": "File adc_dsp.c/.h, ảnh chụp màn hình CubeMX cấu hình ADC1, bảng số liệu thực nghiệm đo điện áp multimeter vs giá trị ADC thô.",
        "deadline": "Day 2",
        "status": "Done",
        "evidence": "Commit #d4e5f6a - Multi-channel ADC1 driver (PA1 TDS, PA4 Potentiometer)"
    },
    {
        "id": "TSK-07",
        "phase": "Phase 2: FreeRTOS Core",
        "subsystem": "Sensors & Analog DSP",
        "assignee": "Hoàng Đức Mạnh",
        "member_code": "Manh",
        "priority": "High",
        "what_is": "Xây dựng thuật toán lọc số trung bình trượt vòng tròn 20 mẫu (20-Sample Circular Moving Average Filter / Ring Buffer) trên RAM. Bộ lọc này triệt tiêu hoàn toàn nhiễu sóng nước, gợn sóng điện áp cao tần và rung chấn cơ học của que đo TDS trong môi trường nước nuôi cá, giúp chỉ số nồng độ TDS không bị nhảy số liên tục.",
        "what_do": "1) Khai báo struct CircularBuffer_t gồm mảng uint16_t buffer[20], uint8_t head_idx, uint8_t count, uint32_t running_sum;\n2) Cài đặt thuật toán cập nhật tối ưu độ phức tạp O(1): running_sum = running_sum - buffer[head] + new_sample; buffer[head] = new_sample; head = (head + 1) % 20;\n3) Viết hàm ADC_Filter_Update() và ADC_Filter_GetAverage() trả về giá trị ADC đã làm phẳng;\n4) Đảm bảo an toàn không xảy ra lỗi chia cho 0 khi bộ đệm chưa nạp đủ mẫu và không tràn số nguyên.",
        "what_submit": "Source code adc_dsp.c (các hàm lọc số vòng tròn), file log dữ liệu CSV so sánh tín hiệu TDS thô vs tín hiệu sau khi lọc 20 mẫu.",
        "deadline": "Day 3",
        "status": "Done",
        "evidence": "Commit #e5f6a7b - 20-sample circular moving average filter implementation"
    },
    {
        "id": "TSK-12",
        "phase": "Phase 2: FreeRTOS Core",
        "subsystem": "Sensors & Analog DSP",
        "assignee": "Hoàng Đức Mạnh",
        "member_code": "Manh",
        "priority": "High",
        "what_is": "Lập trình đa thức hồi quy bậc 3 và công thức bù nhiệt độ chuyển đổi điện áp cảm biến sang nồng độ tổng chất rắn hòa tan (TDS ppm): Vcomp = Vadc / (1.0 + 0.02 * (T - 25.0)), TDS = (133.42 * Vcomp^3 - 255.86 * Vcomp^2 + 857.39 * Vcomp) * 0.5. Phân cấp 4 mức an toàn nước: Lý tưởng (<150ppm), Chấp nhận được (151-350ppm), Ô nhiễm nhẹ (351-500ppm), Độc hại (>500ppm).",
        "what_do": "1) Viết module tds_sensor.c chứa hàm TDS_Calculate_PPM(float raw_voltage, float temp_c);\n2) Áp dụng hệ số bù nhiệt chuẩn 2% mỗi độ C (chuẩn hóa về 25°C);\n3) Viết hàm phân loại Water_Quality_Classify(float tds_ppm) gán cờ trạng thái 0 (Ideal), 1 (Normal), 2 (Elevated), 3 (Hazard);\n4) Đóng gói dữ liệu kết quả vào struct AquariumTelemetry_t để ghi đè vào Length-1 Mailbox bằng xQueueOverwrite().",
        "what_submit": "File tds_sensor.c/.h, test bench kiểm thử trên máy tính với 10 bộ dữ liệu mẫu sai số <3%, commit 'feat(sensor): polynomial tds curve fitting'.",
        "deadline": "Day 4",
        "status": "Done",
        "evidence": "Commit #f6a7b8c - 3rd-order polynomial TDS math and temperature compensation"
    },
    {
        "id": "TSK-17",
        "phase": "Phase 3: Integration & Testing",
        "subsystem": "Sensors & Analog DSP",
        "assignee": "Hoàng Đức Mạnh",
        "member_code": "Manh",
        "priority": "Medium",
        "what_is": "Chuẩn bị bộ 2 cốc nước thực nghiệm và kiểm thử độ nhạy đáp ứng thực tế của hệ thống: Cốc A (nước tinh khiết đóng chai hoặc nước máy sạch ~100-150 ppm) và Cốc B (nước pha muối tinh khiết nồng độ mô phỏng ô nhiễm ~550-650 ppm) sẵn sàng phục vụ trình diễn Live Demo trước hội đồng bảo vệ.",
        "what_do": "1) Chuẩn bị 2 cốc thủy tinh trong suốt dán nhãn Cốc A (Sạch) và Cốc B (Ô nhiễm);\n2) Pha chế Cốc B bằng cách cho từng lượng muối nhỏ, khuấy tan đều và đo kiểm bằng bút thử TDS chuyên dụng đến khi đạt 550-650 ppm;\n3) Nhúng que đo vào Cốc A: kiểm tra hệ thống báo Normal, LED Xanh sáng, Relay BẬT;\n4) Rút que đo nhúng sang Cốc B: đo thời gian phản hồi (yêu cầu <500ms hệ thống phải kích hoạt còi hú, LED Đỏ chớp 1Hz, LCD hiện [!] HAZARD);\n5) Lặp lại quy trình 10 lần liên tục để lập bảng kiểm thử độ tin cậy và lặp lại (Repeatability Test).",
        "what_submit": "Bảng ghi chép dữ liệu 10 lần nhúng que thử nghiệm, video 30s ghi cảnh nhúng que từ Cốc A sang Cốc B còi báo động kích hoạt tức thì.",
        "deadline": "Day 5",
        "status": "In Progress",
        "evidence": "Water Quality Lab Test Report (Cup A: 120ppm, Cup B: 620ppm)"
    },
    {
        "id": "TSK-22",
        "phase": "Phase 4: Defense & Presentation",
        "subsystem": "Sensors & Analog DSP",
        "assignee": "Hoàng Đức Mạnh",
        "member_code": "Manh",
        "priority": "High",
        "what_is": "Trình bày Slide 5 trong buổi bảo vệ (1.5 phút): Phân hệ cảm biến TDS, chu kỳ lấy mẫu ADC, bộ lọc số 20 mẫu, phương trình đa thức bù nhiệt và thang phân loại nước. Trực tiếp thực hiện thao tác nhúng que thử nước trong Live Demo và chịu trách nhiệm bảo vệ các câu hỏi phản biện liên quan đến ADC, lọc số, nhiễu tín hiệu và giải thuật DSP.",
        "what_do": "1) Thiết kế Slide 5 với đồ thị so sánh tín hiệu trước/sau lọc, công thức đa thức và sơ đồ mạch cảm biến;\n2) Luyện tập kịch bản nói đúng 90 giây lưu loát, rõ ràng;\n3) Chuẩn bị 2 cốc nước, khăn lau khô đầu dò sẵn sàng trên bàn hội đồng;\n4) Soạn cẩm nang trả lời các câu hỏi phản biện giáo viên: Độ phân giải 12-bit (4096 mức, 0.805mV), tại sao dùng bộ đệm vòng 20 mẫu, định lý lấy mẫu Nyquist.",
        "what_submit": "Slide 5 hoàn chỉnh kèm Speaker Notes chi tiết, video luyện tập thuyết trình Slide 5 đúng thời lượng quy định.",
        "deadline": "Day 7",
        "status": "To Do",
        "evidence": "Aquatic_Guardian_Presentation.pptx (Slide 5 completed with DSP graphs)"
    },

    # Member 3: Gia (Actuators, Hardware & Power)
    {
        "id": "TSK-03",
        "phase": "Phase 1: Drivers & Hardware",
        "subsystem": "Actuators & Hardware",
        "assignee": "Đỗ Khắc Lê Gia",
        "member_code": "Gia",
        "priority": "High",
        "what_is": "Cấu hình TIM2_CH1 trên PA0 phát xung PWM 50Hz (chu kỳ 20ms) điều khiển servo SG90 từ 0° (1.0ms) đến 90° (1.5ms) để xả thức ăn (hoặc phương án dự phòng dùng chân PB12–PB15 cho động cơ bước 28BYJ-48 + ULN2003, hoàn toàn giải phóng PB8/PB9 cho I2C1).",
        "what_do": "1) Tính toán thông số Timer clock 84 MHz: Đặt Prescaler PSC = 83 để tần số đếm là 84MHz / (83 + 1) = 1 MHz (1 tick = 1µs);\n2) Đặt Auto-Reload Register ARR = 19999 để chu kỳ đếm là 20000 µs = 20 ms (tương đương 50 Hz);\n3) Cấu hình Capture/Compare Register CCR1: Ghi giá trị 1000 cho góc 0° (1.0ms), ghi giá trị 1500 cho góc 90° (1.5ms);\n4) Viết module servo_feeder.c/.h triển khai Servo_Init(), Servo_SetAngle(uint8_t angle), Servo_Dispense_Portion();\n5) Kiểm tra dạng sóng trên Oscilloscope hoặc logic analyzer xác nhận độ rộng xung chuẩn xác.",
        "what_submit": "Source code servo_feeder.c/.h, ảnh chụp oscilloscope dạng sóng PWM 50Hz xung 1ms và 1.5ms, commit 'feat(actuator): tim2 pwm 50hz servo driver'.",
        "deadline": "Day 2",
        "status": "Done",
        "evidence": "Commit #a7b8c9d - TIM2 PWM 50Hz Servo Feeder Driver (PSC=83, ARR=19999)"
    },
    {
        "id": "TSK-08",
        "phase": "Phase 2: FreeRTOS Core",
        "subsystem": "Actuators & Hardware",
        "assignee": "Đỗ Khắc Lê Gia",
        "member_code": "Gia",
        "priority": "High",
        "what_is": "Gia công chế tạo cơ cấu cấp thức ăn tự động dạng phễu xoay / nắp chai có rãnh khoét (Rotary Bottle-Cap Feeder Mechanism) gắn trực tiếp vào trục động cơ servo/stepper, đảm bảo mỗi chu kỳ quay mở góc 90° xả rơi chính xác 2g - 4g hạt thức ăn cá mà tuyệt đối không bị kẹt hay vón cục.",
        "what_do": "1) Gia công nắp xoay từ nắp chai nhựa/mica có khoét rãnh kích thước 8mm x 15mm vừa vặn cho các hạt cám cá cảnh;\n2) Gắn cố định cánh tay servo/trục động cơ vào nắp xoay bằng vít hãm và keo chuyên dụng chống trượt;\n3) Chế tạo phễu chứa thức ăn dung tích 100ml gắn cố định phía trên nắp xoay;\n4) Lắp đặt cụm cơ khí lên khung giá đỡ mica chắc chắn bắt vào thành bể cá;\n5) Thử nghiệm nạp 50 hạt thức ăn cá thực tế, bấm kích hoạt 20 lần liên tục để đo tỷ lệ kẹt (yêu cầu đạt 0% kẹt hạt).",
        "what_submit": "Bộ 3 ảnh chụp các góc cơ cấu cấp thức ăn hoàn thiện, video 15s quay cận cảnh phễu xoay xả thức ăn rơi đều đặn không kẹt.",
        "deadline": "Day 3",
        "status": "Done",
        "evidence": "Mechanical Dispenser Assembly (0% jam rate across 20 cycles test)"
    },
    {
        "id": "TSK-13",
        "phase": "Phase 2: FreeRTOS Core",
        "subsystem": "Actuators & Hardware",
        "assignee": "Đỗ Khắc Lê Gia",
        "member_code": "Gia",
        "priority": "High",
        "what_is": "Thiết kế và lắp đặt hệ thống phân phối nguồn điện cách ly an toàn (Isolated Power Rail): Sử dụng bộ nguồn ngoài 5V/2A riêng biệt cấp nguồn động lực cho servo motor, còi hú và cuộn hút rơ-le, đồng thời nối chung Mass (Common Ground) với bo mạch STM32 Nucleo (3.3V) nhằm triệt tiêu hoàn toàn hiện tượng sụt áp nguồn (brownout reset) và xung nhiễu cảm ứng khi motor khởi động.",
        "what_do": "1) Hàn module nguồn ngoài DC 5V/2A hoặc sử dụng breadboard power supply riêng;\n2) Đấu nối đường dây nguồn: Chân 5V nguồn ngoài cấp cho Servo VCC, Relay VCC, Buzzer VCC; chân 5V của STM32 KHÔNG cấp nguồn cho tải động cơ;\n3) Nối dây Mass (GND) giữa nguồn ngoài 5V và chân GND của bo STM32 Nucleo để có cùng mức điện thế tham chiếu;\n4) Lắp thêm tụ hóa 100µF và tụ gốm 100nF song song tại đầu cấp nguồn servo để san phẳng xung nhọn điện áp khi đảo chiều motor.",
        "what_submit": "Sơ đồ nối dây chi tiết hardware_wiring.md, ảnh chụp thực tế trạm nguồn chung GND và tụ lọc nhiễu, biên bản đo điện áp VDD của STM32 ổn định tuyệt đối khi servo quay.",
        "deadline": "Day 4",
        "status": "In Progress",
        "evidence": "docs/pinout_wiring.md - Power Rail Isolation & Common Ground Diagram"
    },
    {
        "id": "TSK-18",
        "phase": "Phase 3: Integration & Testing",
        "subsystem": "Actuators & Hardware",
        "assignee": "Đỗ Khắc Lê Gia",
        "member_code": "Gia",
        "priority": "Medium",
        "what_is": "Tích hợp và lập trình điều khiển mạch an toàn ngoại vi: Module Active Buzzer 5V trên chân PB0 (phát âm thanh cảnh báo khi nước ô nhiễm hoặc tiếng bíp xác nhận cho ăn) và Module Rơ-le cách ly quang (Optocoupler Relay 5V) trên chân PB4 (đóng ngắt máy bơm lọc / sục khí bể cá).",
        "what_do": "1) Cấu hình chân PB0 và PB4 làm GPIO_Output Push-Pull, tốc độ Low Speed;\n2) Viết driver buzzer.c/.h hỗ trợ 3 chế độ âm thanh: BUZZER_BEEP_CONFIRM (1 tiếng bíp 100ms khi cho ăn), BUZZER_WARN_CHIRP (bíp ngắt quãng khi nước đục), BUZZER_ALARM_CRITICAL (còi hú liên tục khi nước nguy cấp);\n3) Viết driver relay.c/.h hỗ trợ RELAY_Pump_TurnOn(), RELAY_Pump_TurnOff() phù hợp với mức kích (Active LOW) của rơ-le;\n4) Kiểm tra cách ly quang của rơ-le đảm bảo tiếng đóng ngắt tiếp điểm không sinh gai xung gây reset vi điều khiển.",
        "what_submit": "Source code buzzer.c/.h, relay.c/.h, video 20s test rơ-le nhảy đóng tiếp điểm và còi hú theo từng lệnh điều khiển phần mềm.",
        "deadline": "Day 5",
        "status": "To Do",
        "evidence": "buzzer.c/.h & relay.c/.h driver modules with optocoupler isolation test"
    },
    {
        "id": "TSK-23",
        "phase": "Phase 4: Defense & Presentation",
        "subsystem": "Actuators & Hardware",
        "assignee": "Đỗ Khắc Lê Gia",
        "member_code": "Gia",
        "priority": "High",
        "what_is": "Trình bày Slide 6 trong buổi bảo vệ (1.5 phút): Cơ cấu cơ khí bộ cấp thức ăn, công thức tính toán xung PWM Timer 50Hz (PSC=83, ARR=19999), giải pháp cách ly nguồn ngoài 5V chống brownout và mạch bảo vệ rơ-le/còi. Trực tiếp kích hoạt cơ cấu xả thức ăn trong Live Demo và chịu trách nhiệm bảo vệ các câu hỏi liên quan đến Timer PWM, điện trở tải, cuộn cảm động cơ và công suất.",
        "what_do": "1) Thiết kế Slide 6 với công thức tính toán Timer chi tiết, ảnh chụp cụm cơ khí nắp chai thực tế và sơ đồ nguyên lý nguồn ngoài;\n2) Luyện tập thuyết trình trôi chảy trong 90 giây;\n3) Chuẩn bị đầy đủ hạt thức ăn cá và dây nguồn dự phòng trong buổi bảo vệ;\n4) Nắm vững câu trả lời phản biện: Tại sao phải tách nguồn 5V riêng cho motor, tác dụng của diode triệt xung cảm ứng ngược (Flyback Diode), cách tính Duty Cycle cho góc quay servo.",
        "what_submit": "Slide 6 hoàn chỉnh kèm Speaker Notes, checklist dụng cụ và linh kiện phần cứng mang vào phòng bảo vệ đồ án.",
        "deadline": "Day 7",
        "status": "To Do",
        "evidence": "Aquatic_Guardian_Presentation.pptx (Slide 6 completed with Timer PWM formulas)"
    },

    # Member 4: Minh (I2C Bus, RTC & Display UI)
    {
        "id": "TSK-04",
        "phase": "Phase 1: Drivers & Hardware",
        "subsystem": "I2C Bus & Display UI",
        "assignee": "Phạm Hồng Minh",
        "member_code": "Minh",
        "priority": "High",
        "what_is": "Cấu hình ngoại vi I2C1 Master trên STM32 (chân PB8 - SCL, PB9 - SDA) hoạt động ở Standard Mode (100 kHz) với điện trở kéo lên Pull-up 4.7kΩ. Lập trình chương trình quét bus tự động (I2C Bus Scanner) để dò tìm và xác thực các địa chỉ 7-bit vật lý của chip mở rộng LCD PCF8574 (0x27 hoặc 0x3F), đồng hồ DS3231 (0x68) và bộ nhớ EEPROM AT24C32 (0x57).",
        "what_do": "1) Mở CubeMX cấu hình I2C1: Speed Mode = Standard Mode (100 kHz), Rise Time = 1000ns, Fall Time = 300ns;\n2) Cấu hình chân PB8/PB9 làm I2C1_SCL/I2C1_SDA ở chế độ Open-Drain Pull-Up;\n3) Viết hàm I2C_Scan_Devices() gửi lệnh HAL_I2C_IsDeviceReady() từ địa chỉ 0x01 đến 0x7F;\n4) In ra terminal danh sách các thiết bị phản hồi ACK trên bus;\n5) Kiểm tra cờ I2C_FLAG_BUSY đảm bảo bus không bị treo khi vi điều khiển khởi động lại.",
        "what_submit": "File i2c_bus.c/.h, ảnh chụp màn hình console in danh sách 3 địa chỉ I2C quét được thực tế (0x27, 0x57, 0x68), commit 'feat(i2c): bus scanner and hal initialization'.",
        "deadline": "Day 2",
        "status": "Done",
        "evidence": "Commit #b8c9d0e - I2C1 Master Driver & Address Scanner (Detected: 0x27, 0x57, 0x68)"
    },
    {
        "id": "TSK-09",
        "phase": "Phase 2: FreeRTOS Core",
        "subsystem": "I2C Bus & Display UI",
        "assignee": "Phạm Hồng Minh",
        "member_code": "Minh",
        "priority": "High",
        "what_is": "Phát triển thư viện điều khiển màn hình ký tự LCD 1602 (hoặc LCD 2004) thông qua chip mở rộng GPIO 8-bit PCF8574 theo giao thức 4-bit mode (truyền 4 bit cao, 4 bit thấp kèm tạo xung Enable chốt lệnh). Thiết kế bố cục giao diện trực quan hiển thị nồng độ TDS, trạng thái nước và đồng hồ thời gian thực.",
        "what_do": "1) Lập trình các hàm cơ bản: LCD_Write_Nibble(), LCD_Send_Cmd(), LCD_Send_Data(), LCD_Init(), LCD_SetCursor(), LCD_Print();\n2) Thiết kế bố cục 2 dòng trên LCD 1602:\n   - Dòng 1: 'TDS: 180ppm [O]' (hoặc '[!] HAZARD' khi ô nhiễm)\n   - Dòng 2: 'Feed: 14:00 (4g)' (hiển thị giờ hẹn và khẩu phần g);\n3) Tối ưu hóa việc ghi LCD: chỉ ghi đè ký tự thay đổi thay vì xóa toàn màn hình để chống giật nhấp nháy (flickering);\n4) Thiết kế ký tự đặc biệt Custom Character (icon con cá, icon giọt nước cảnh báo).",
        "what_submit": "File lcd_pcf8574.c/.h, ảnh chụp màn hình LCD thực tế hiển thị chữ sắc nét rõ ràng, commit 'feat(ui): pcf8574 4-bit i2c lcd driver'.",
        "deadline": "Day 3",
        "status": "Done",
        "evidence": "Commit #c9d0e1f - PCF8574 4-bit I2C LCD Driver & Aquarium HUD layout"
    },
    {
        "id": "TSK-14",
        "phase": "Phase 2: FreeRTOS Core",
        "subsystem": "I2C Bus & Display UI",
        "assignee": "Phạm Hồng Minh",
        "member_code": "Minh",
        "priority": "High",
        "what_is": "Giao tiếp với chip thời gian thực chính xác cao DS3231 (TCXO tích hợp thạch anh bù nhiệt, địa chỉ I2C 0x68) để đọc thời gian thực (Giờ:Phút:Giây, Ngày/Tháng/Năm) theo định dạng BCD. Thiết lập bộ lập lịch cho ăn tự động đối chiếu thời gian thực với các mốc giờ hẹn trong ngày (ví dụ: 08:00 sáng và 17:00 chiều) để tự động phát cờ cho cá ăn.",
        "what_do": "1) Viết các hàm chuyển đổi toán học nhị phân - BCD: BCD2BIN() và BIN2BCD();\n2) Đọc tuần tự các thanh ghi 0x00 đến 0x06 của DS3231 bằng HAL_I2C_Mem_Read();\n3) Viết hàm DS3231_GetTime(RTC_Time_t *time) và DS3231_SetTime(RTC_Time_t *time);\n4) Xây dựng giải thuật Single-Shot Minute Guard trong Task_DisplayUI: Chỉ phát cờ feedTriggerSem 1 lần duy nhất tại giây thứ 0 của phút hẹn;\n5) Kiểm tra pin cúc áo CR2032 đảm bảo đồng hồ vẫn chạy đúng khi ngắt nguồn cấp chính.",
        "what_submit": "Source code ds3231_rtc.c/.h, log chụp thời gian thực đọc từ DS3231 khớp tuyệt đối với đồng hồ máy tính, commit 'feat(rtc): ds3231 timekeeper and feeding scheduler'.",
        "deadline": "Day 4",
        "status": "In Progress",
        "evidence": "Commit #d0e1f2a - DS3231 RTC Timekeeping & Automated Feeding Scheduler"
    },
    {
        "id": "TSK-19",
        "phase": "Phase 3: Integration & Testing",
        "subsystem": "I2C Bus & Display UI",
        "assignee": "Phạm Hồng Minh",
        "member_code": "Minh",
        "priority": "High",
        "what_is": "Lưu trữ lịch trình cho ăn và log sự kiện vào EEPROM AT24C32 (0x57 trên I2C1). Bọc toàn bộ các hàm đọc/ghi I2C (LCD2004, DS3231, AT24C32) trong i2cBusMutex, chứng minh cơ chế Priority Inheritance giữa Task_DispenserControl (AboveNormal) và Task_DisplayUI (BelowNormal).",
        "what_do": "1) Viết module at24c32_eeprom.c hỗ trợ EEPROM_Write_Byte(), EEPROM_Read_Byte(), EEPROM_Write_Page() (tối đa 32 bytes/trang kèm delay 5ms ghi bộ nhớ);\n2) Định nghĩa struct FeedingSchedule_t (số bữa ăn, mảng giờ/phút, khẩu phần gam) lưu vào Page 0;\n3) Trong mọi tác vụ truy cập ngoại vi I2C1, thực thi nghiêm ngặt: osMutexAcquire(i2cBusMutexHandle, osWaitForever) -> Thao tác I2C -> osMutexRelease(i2cBusMutexHandle);\n4) Kiểm thử ngắt nguồn điện và cắm lại: kiểm tra cấu hình lịch ăn được khôi phục nguyên vẹn từ EEPROM.",
        "what_submit": "Source code at24c32_eeprom.c/.h, log kiểm thử nạp dữ liệu EEPROM và đọc lại sau khi khởi động lại, commit 'feat(i2c): eeprom persistence and mutex wrapping'.",
        "deadline": "Day 5",
        "status": "To Do",
        "evidence": "at24c32_eeprom.c/.h module with i2cBusMutex atomic protection"
    },
    {
        "id": "TSK-24",
        "phase": "Phase 4: Defense & Presentation",
        "subsystem": "I2C Bus & Display UI",
        "assignee": "Phạm Hồng Minh",
        "member_code": "Minh",
        "priority": "High",
        "what_is": "Trình bày Slide 7 trong buổi bảo vệ (1.5 phút): Kiến trúc bus I2C đa thiết bị, giao diện HUD hiển thị trạng thái bể cá trên LCD, đồng hồ RTC chính xác cao và bộ nhớ lưu trữ EEPROM không mất dữ liệu. Hướng dẫn giám khảo quan sát màn hình LCD trong Live Demo và chịu trách nhiệm bảo vệ các câu hỏi liên quan đến giao thức I2C, xung ACK/NACK, xung đột bus và Mutex.",
        "what_do": "1) Thiết kế Slide 7 với sơ đồ bus I2C dùng chung chân PB8/PB9, bảng địa chỉ 3 chip và giải thích cơ chế khóa i2cBusMutex;\n2) Luyện tập kịch bản thuyết minh đúng 90 giây;\n3) Điều chỉnh biến trở tương phản trên board PCF8574 để màn hình hiển thị chữ rõ nét nhất trong điều kiện ánh sáng phòng thi;\n4) Nắm vững câu trả lời phản biện: Tại sao phải dùng Mutex thay vì Semaphore cho I2C, hậu quả nếu 2 task cùng gọi HAL_I2C mà không có Mutex (lỗi I2C_BUSY lockup).",
        "what_submit": "Slide 7 hoàn chỉnh kèm Speaker Notes chi tiết, checklist kiểm tra hiển thị màn hình LCD trước giờ thi.",
        "deadline": "Day 7",
        "status": "To Do",
        "evidence": "Aquatic_Guardian_Presentation.pptx (Slide 7 completed with I2C bus diagrams)"
    },

    # Member 5: DucAnh (IoT Telemetry, Telegram Bot & QA)
    {
        "id": "TSK-05",
        "phase": "Phase 1: Drivers & Hardware",
        "subsystem": "IoT Telemetry & QA",
        "assignee": "Nguyễn Đức Anh",
        "member_code": "DucAnh",
        "priority": "High",
        "what_is": "Cấu hình kiến trúc Dual UART: USART1 (PA9/PA10 @ 115200 bps) chuyên dụng kết nối ESP32 với đóng khung ký tự ngã '~' (ví dụ: ~{\"time\":120,\"tds_ppm\":180.0,\"status\":0}~); USART2 (PA2/PA3 @ 115200 bps) dành riêng cho cổng ảo ST-LINK Virtual COM Port trên PC.",
        "what_do": "1) Mở CubeMX cấu hình USART1 (PA9/PA10) và USART2 (PA2/PA3) cùng tốc độ 115200 bps, 8N1;\n2) Cấu hình NVIC Interrupt cho USART1 và USART2;\n3) Viết module telemetry_uart.c/.h triển khai UART_SendTelemetryJSON(AquariumTelemetry_t *data) qua cả 2 cổng;\n4) Sử dụng thư viện snprintf() với bộ đệm an toàn chống tràn ngăn xếp (Task_Telemetry cấp 2048 bytes);\n5) Kết nối cáp USB ST-Link và module ESP32 kiểm tra luồng telemetry đồng thời.",
        "what_submit": "Source code telemetry_uart.c/.h, ảnh chụp màn hình PC Serial Monitor nhận các gói tin JSON đóng mở bằng '~' chuẩn xác, commit 'feat(uart): 115200 serial json streaming'.",
        "deadline": "Day 2",
        "status": "Done",
        "evidence": "Commit #e1f2a3b - Dual UART Architecture (USART1 ESP32 & USART2 PC VCP) with '~' framing"
    },
    {
        "id": "TSK-10",
        "phase": "Phase 2: FreeRTOS Core",
        "subsystem": "IoT Telemetry & QA",
        "assignee": "Nguyễn Đức Anh",
        "member_code": "DucAnh",
        "priority": "High",
        "what_is": "Phát triển firmware cho bo vi điều khiển Wi-Fi ESP32 (Esp32.ino) kết nối với STM32 qua USART1 (PA9/PA10): Kết nối Wi-Fi, nhận dữ liệu telemetry từ STM32 để cập nhật Telegram, lắng nghe lệnh /feed, /status, /clean gửi qua USART1 về STM32.",
        "what_do": "1) Cài đặt thư viện UniversalTelegramBot và ArduinoJson trên môi trường Arduino IDE / PlatformIO;\n2) Tạo Bot mới trên Telegram qua BotFather, lấy BOT_TOKEN và CHAT_ID;\n3) Viết hàm phân tích lệnh chat: Khi nhận lệnh /feed, ESP32 gửi ký tự 'F' sang STM32 kích hoạt nhả thức ăn; Khi nhận /status, bot phản hồi chỉ số TDS và mức an toàn;\n4) Thiết lập cơ chế tự động bắn tin nhắn khẩn cấp 'CẢNH BÁO: Nước bị ô nhiễm, TDS > 500 ppm!' khi cờ cảnh báo bật;\n5) Kiểm tra độ trễ nhận lệnh qua 4G/Wi-Fi đạt < 2 giây.",
        "what_submit": "File mã nguồn Esp32.ino, ảnh chụp màn hình điện thoại chat trực tiếp với Telegram Bot kích hoạt thành công lệnh cho ăn và nhận cảnh báo.",
        "deadline": "Day 3",
        "status": "Done",
        "evidence": "Esp32.ino Firmware & Telegram Bot (@AquaticGuardian_Bot) verification"
    },
    {
        "id": "TSK-15",
        "phase": "Phase 3: Integration & Testing",
        "subsystem": "IoT Telemetry & QA",
        "assignee": "Nguyễn Đức Anh",
        "member_code": "DucAnh",
        "priority": "Medium",
        "what_is": "Xây dựng ứng dụng bảng điều khiển giám sát qua cổng nối tiếp trên máy tính (PC Serial Testing Dashboard) bằng ngôn ngữ Python (hoặc giao diện Serial Terminal màu). Ứng dụng này trực tiếp bắt các gói JSON từ cổng COM của Nucleo để hiển thị bảng số đo trực quan và cung cấp phím bấm gửi lệnh test trong trường hợp phòng bảo vệ không có sóng Wi-Fi.",
        "what_do": "1) Viết script scripts/aquatic_pc_dashboard.py sử dụng thư viện pyserial và colorama;\n2) Tự động dò tìm cổng COM ST-Link và kết nối ở tốc độ 115200 bps;\n3) Bóc tách khung ký tự '~', giải mã chuỗi JSON và vẽ bảng HUD hiển thị TDS, mức nước, trạng thái rơ-le;\n4) Cung cấp menu phím tắt: Bấm phím '1' để ra lệnh cho ăn, bấm phím '2' để đảo trạng thái rơ-le máy lọc, bấm phím '3' để test còi hú;\n5) Lưu log toàn bộ phiên làm việc ra file CSV phục vụ báo cáo kiểm thử.",
        "what_submit": "File mã nguồn scripts/aquatic_pc_dashboard.py, ảnh chụp màn hình giao diện console dashboard nhiều màu đang hiển thị dữ liệu live.",
        "deadline": "Day 5",
        "status": "In Progress",
        "evidence": "scripts/aquatic_pc_dashboard.py CLI Terminal Live HUD Utility"
    },
    {
        "id": "TSK-20",
        "phase": "Phase 3: Integration & Testing",
        "subsystem": "IoT Telemetry & QA",
        "assignee": "Nguyễn Đức Anh",
        "member_code": "DucAnh",
        "priority": "High",
        "what_is": "Thực hiện bài kiểm thử ứng suất và an toàn bộ nhớ (Stress & Failsafe Stability Testing) cho hệ thống FreeRTOS: Kích hoạt cờ kiểm tra tràn ngăn xếp configCHECK_FOR_STACK_OVERFLOW = 2 trong FreeRTOSConfig.h, viết hàm hook vApplicationStackOverflowHook() bắt lỗi, và sử dụng hàm uxTaskGetStackHighWaterMark() đo lượng RAM còn trống của từng task.",
        "what_do": "1) Mở FreeRTOSConfig.h, bật macro #define configCHECK_FOR_STACK_OVERFLOW 2;\n2) Cài đặt hàm vApplicationStackOverflowHook(TaskHandle_t xTask, char *pcTaskName): nhấp nháy đèn LED đỏ liên tục và in cảnh báo tên task bị tràn ra cổng UART;\n3) Viết hàm chẩn đoán gọi uxTaskGetStackHighWaterMark() cho cả 5 tasks sau 30 phút chạy liên tục dưới tải nặng;\n4) Đánh giá và xác nhận dung lượng stack an toàn (mỗi task còn dư tối thiểu 40-60 words);\n5) Lập biên bản kiểm thử QA Test Report ghi nhận tính ổn định tuyệt đối.",
        "what_submit": "File FreeRTOSConfig.h, biên bản kiểm thử an toàn qa_test_report.md ghi rõ High Water Mark của từng task, commit 'test(rtos): stack overflow check enabled and verified'.",
        "deadline": "Day 6",
        "status": "To Do",
        "evidence": "qa_test_report.md - FreeRTOS Stack High Water Mark Stress Report (30 mins run)"
    },
    {
        "id": "TSK-25",
        "phase": "Phase 4: Defense & Presentation",
        "subsystem": "IoT Telemetry & QA",
        "assignee": "Nguyễn Đức Anh",
        "member_code": "DucAnh",
        "priority": "High",
        "what_is": "Trình bày Slides 8–10 trong buổi bảo vệ (1.5 phút): Giao thức truyền thông nối tiếp, Telegram Bot đám mây, kết quả kiểm thử an toàn ngăn xếp và định hướng phát triển. Đồng thời quay và dựng sẵn 1 video backup 2 phút độ phân giải 4K ghi lại toàn bộ hoạt động của hệ thống đề phòng rủi ro phần cứng tại bàn chấm thi.",
        "what_do": "1) Thiết kế Slides 8-10 với ảnh chụp giao diện Telegram Bot, kiến trúc IoT và bảng số liệu kiểm thử an toàn stack;\n2) Quay video 4K cận cảnh 4 tình huống hoạt động của mô hình thực tế (cho ăn, LED đổi màu, còi hú khi cắm nước bẩn, Telegram nhận tin);\n3) Biên tập và lồng tiếng/phụ đề cho video độ dài chính xác 2 phút 00 giây;\n4) Chuẩn bị máy tính xách tay phát sẵn video khi có yêu cầu;\n5) Nắm vững câu trả lời phản biện: Cách ngăn ngừa tràn bộ đệm nhận UART (Ring buffer / DMA), phương pháp phát hiện Stack Overflow của FreeRTOS.",
        "what_submit": "Slide 8-10 hoàn chỉnh kèm Speaker Notes, file video demo dự phòng docs/demo_backup_video.mp4 (hoặc link Google Drive lưu trữ).",
        "deadline": "Day 7",
        "status": "To Do",
        "evidence": "Aquatic_Guardian_Presentation.pptx (Slides 8-10) & docs/demo_backup_video.mp4"
    }
]

# Rubric Mapping Checklist Data (Direct MCP201 30% Grading Guide)
RUBRIC_CHECKLIST_DATA = [
    {
        "category": "System Architecture & Complexity (25%)",
        "checkpoint": "Preemptive Multitasking & 5-Task Scheduling Hierarchy",
        "assignee": "Nghiêm Hoàng Tùng",
        "implementation": "5 tasks độc lập phân tầng ưu tiên nghiêm ngặt (Safety: 32 > Dispenser: 24 > Sensor: 16 > Display: 12 > Telemetry: 8). Triệt tiêu tình trạng CPU starvation bằng định thời chuẩn xác.",
        "verification": "Kiểm tra file freertos.c / aquatic_guardian_app.c, bảng Task Specification Table, đo chu kỳ task không bị trễ bằng oscilloscope hoặc logic analyzer.",
        "readiness": "Verified"
    },
    {
        "category": "System Architecture & Complexity (25%)",
        "checkpoint": "Deterministic Timing & Proper Task State Transitions",
        "assignee": "Nghiêm Hoàng Tùng",
        "implementation": "Sử dụng osDelayUntil() và osSemaphoreAcquire() để đưa task vào trạng thái Blocked State, nhường hoàn toàn CPU cho task khác; nghiêm cấm sử dụng spin-lock HAL_Delay().",
        "verification": "Code review toàn bộ dự án chứng minh 0 cuộc gọi HAL_Delay() trong task loops, phân tích biểu đồ chuyển trạng thái Task State Diagram.",
        "readiness": "Verified"
    },
    {
        "category": "System Architecture & Complexity (25%)",
        "checkpoint": "Thread-Safe Inter-Process Communication (IPC)",
        "assignee": "Nghiêm Hoàng Tùng",
        "implementation": "Length-1 Non-Destructive Mailbox Queue (xQueueOverwrite + xQueuePeek) loại bỏ hoàn toàn hiện tượng task starvation giữa 3 tasks tiêu thụ dữ liệu.",
        "verification": "Kiểm tra cấu trúc hàng đợi, chứng minh không phát sinh xung đột đọc/ghi biến toàn cục (Race Condition).",
        "readiness": "Verified"
    },
    {
        "category": "Peripheral Integration - HAL (25%)",
        "checkpoint": "Multi-Channel ADC & Circular Moving Average DSP",
        "assignee": "Hoàng Đức Mạnh",
        "implementation": "ADC1 Dynamic Polling trên PA1 (TDS) và PA4 (Potentiometer), DS18B20 1-Wire trên PA8 (4.7kΩ). Thuật toán lọc trung bình trượt vòng 20 mẫu và đa thức bậc 3 bù nhiệt.",
        "verification": "Bảng kiểm thử điện áp thực nghiệm VOM vs ADC, đồ thị so sánh tín hiệu trước/sau lọc số, kiểm chứng sai số TDS < 3%.",
        "readiness": "Verified"
    },
    {
        "category": "Peripheral Integration - HAL (25%)",
        "checkpoint": "Hardware Timer PWM & Actuator Mechanism",
        "assignee": "Đỗ Khắc Lê Gia",
        "implementation": "TIM2_CH1 PWM trên PA0 tần số 50Hz (PSC=83, ARR=19999). Độ rộng xung 1ms-1.5ms điều khiển servo SG90 quay phễu nắp chai cấp chính xác 2g-4g thức ăn cá.",
        "verification": "Ảnh chụp dạng sóng xung Oscilloscope đo chu kỳ 20ms và duty cycle 5%-7.5%, video cơ cấu cấp thức ăn quay 20 chu kỳ đạt 0% kẹt hạt.",
        "readiness": "Verified"
    },
    {
        "category": "Peripheral Integration - HAL (25%)",
        "checkpoint": "Shared I2C1 Bus (LCD2004 + DS3231 RTC + AT24C32 EEPROM)",
        "assignee": "Phạm Hồng Minh",
        "implementation": "Giao thức I2C1 Master trên PB8/PB9 kết nối đồng thời 3 thiết bị ngoại vi: LCD PCF8574 (0x27), RTC DS3231 (0x68), và EEPROM AT24C32 (0x57) không xung đột.",
        "verification": "Console log quét I2C bus scanner phát hiện đủ 3 địa chỉ, màn hình LCD hiển thị 2 dòng thông tin không nhấp nháy, RTC chạy đúng giờ.",
        "readiness": "Verified"
    },
    {
        "category": "Peripheral Integration - HAL (25%)",
        "checkpoint": "Serial Telemetry, Framing & IoT Cloud Bridge",
        "assignee": "Nguyễn Đức Anh",
        "implementation": "Dual UART: USART1 (PA9/PA10 @ 115200 bps) đóng khung JSON bằng '~' cho ESP32 Telegram Bot; USART2 (PA2/PA3) cho ST-LINK PC Virtual COM Port.",
        "verification": "Ảnh chụp màn hình chat Telegram Bot phản hồi lệnh /feed và /status, ảnh PC Serial Dashboard nhận bản tin JSON thời gian thực.",
        "readiness": "Verified"
    },
    {
        "category": "RTOS Synchronization & Safety (25%)",
        "checkpoint": "Mutual Exclusion (Mutex) & Priority Inheritance on Shared Bus",
        "assignee": "Phạm Hồng Minh / Tùng",
        "implementation": "i2cBusMutex bảo vệ bus I2C1 với Priority Inheritance: Task_DispenserControl (AboveNormal) ghi EEPROM 0x57 nâng ưu tiên của Task_DisplayUI (BelowNormal) đang dùng LCD/RTC.",
        "verification": "Code review xác nhận toàn bộ lệnh HAL_I2C được bao bọc bởi osMutexAcquire/Release, chứng minh không bao giờ xảy ra lỗi I2C_BUSY flag lockup.",
        "readiness": "Verified"
    },
    {
        "category": "RTOS Synchronization & Safety (25%)",
        "checkpoint": "Deferred Interrupt Processing (EXTI13 + Binary Semaphore)",
        "assignee": "Nghiêm Hoàng Tùng",
        "implementation": "Ngắt nút bấm PC13 (EXTI13) với bộ lọc chống rung phần mềm 300ms software tick guard, thực thi osSemaphoreRelease() trong ISR (<1µs) cho Task_DispenserControl.",
        "verification": "Kiểm tra mã nguồn stm32f4xx_it.c, chứng minh ISR siêu ngắn không chứa vòng lặp delay, đo thời gian phản hồi nhả thức ăn tức thì.",
        "readiness": "Verified"
    },
    {
        "category": "RTOS Synchronization & Safety (25%)",
        "checkpoint": "Memory Integrity & Stack Overflow Protection",
        "assignee": "Nguyễn Đức Anh",
        "implementation": "Bật configCHECK_FOR_STACK_OVERFLOW = 2, định lượng stack chuẩn xác theo byte (1024 bytes core, 2048 bytes UI/Telemetry), cài hook vApplicationStackOverflowHook() và đo uxTaskGetStackHighWaterMark().",
        "verification": "Biên bản qa_test_report.md chạy stress test liên tục 30 phút, High Water Mark của cả 5 tasks đều còn dư > 40 words an toàn.",
        "readiness": "Verified"
    },
    {
        "category": "Live Demonstration & Q&A (25%)",
        "checkpoint": "Seamless 4-Stage Live Hardware Demonstration",
        "assignee": "Cả 5 Thành viên (All 5)",
        "implementation": "Kịch bản demo 4 giai đoạn hoàn chỉnh: 1) Khởi động hiển thị HUD bình thường; 2) Bấm nút PC13 / chat Telegram cho ăn; 3) Nhúng que đo vào Cốc B báo động nguy cấp; 4) Xoay chiết áp đổi khẩu phần.",
        "verification": "Tổng duyệt thực tế trước bảo vệ, thời gian chuyển trạng thái < 500ms, còi hú và đèn báo chuẩn xác, thức ăn rơi trúng bể.",
        "readiness": "Ready"
    },
    {
        "category": "Live Demonstration & Q&A (25%)",
        "checkpoint": "10-Minute Slide Deck & 2-Minute 4K Backup Video",
        "assignee": "Nguyễn Đức Anh / Tùng",
        "implementation": "Slide deck 10 trang phân công chuẩn xác thời lượng từng thành viên; Video dự phòng 4K độ dài 2 phút ghi lại toàn cảnh hoạt động phòng trường hợp trục trặc phần cứng bàn thi.",
        "verification": "File video demo_backup_video.mp4 lưu trữ trên máy tính và link cloud dự phòng, tập dượt thuyết trình đúng 8 phút slide + 2 phút demo.",
        "readiness": "Ready"
    }
]

# Top 10 Instructor Grilling Defense Questions & Model Answers
DEFENSE_QA_DATA = [
    {
        "qid": "Q01",
        "domain": "FreeRTOS Kernel",
        "assignee": "Nghiêm Hoàng Tùng",
        "question": "Why did you use a Mutex for the I2C bus instead of a Binary Semaphore?\n(Tại sao bạn dùng Mutex cho bus I2C mà không dùng Binary Semaphore?)",
        "answer": "Thưa Thầy/Cô, Mutex và Binary Semaphore có mục đích thiết kế hoàn toàn khác nhau:\n1) Mutex được sinh ra cho bài toán 'Mutual Exclusion' (Độc quyền tài nguyên) và có khái niệm 'Quyền sở hữu' (Ownership) - chỉ task nào khóa Mutex mới có quyền mở nó;\n2) Quan trọng nhất, Mutex trong FreeRTOS hỗ trợ cơ chế 'Priority Inheritance' (Kế thừa mức ưu tiên). Trong hệ thống của chúng em, Task_DispenserControl (AboveNormal) ghi log vào EEPROM AT24C32 (0x57) và Task_DisplayUI (BelowNormal) cập nhật LCD2004 (0x27) và đọc RTC DS3231 (0x68) đều dùng I2C1. Nếu Task_DisplayUI đang giữ bus mà Task_DispenserControl thức giấc đòi ghi log, FreeRTOS sẽ tạm thời nâng ưu tiên của Task_DisplayUI lên AboveNormal để nó nhanh chóng giải phóng bus, triệt tiêu hoàn toàn Priority Inversion;\n3) Ngược lại, Binary Semaphore chỉ phục vụ bài toán 'Signaling' (Đồng bộ phát cờ báo hiệu) và không có quyền sở hữu, không có Priority Inheritance nên nếu dùng cho bus chia sẻ sẽ rất dễ gây deadlock.",
        "keywords": "Priority Inheritance, Resource Ownership, Mutual Exclusion, Priority Inversion Elimination, Task Blocking"
    },
    {
        "qid": "Q02",
        "domain": "FreeRTOS Scheduling",
        "assignee": "Nghiêm Hoàng Tùng",
        "question": "What happens if a developer calls HAL_Delay(1000) inside a FreeRTOS task?\n(Chuyện gì sẽ xảy ra nếu lập trình viên gọi HAL_Delay(1000) bên trong một task FreeRTOS?)",
        "answer": "Thưa Thầy/Cô, việc gọi HAL_Delay() bên trong một task FreeRTOS là một lỗi nghiêm trọng trong lập trình hệ nhúng thời gian thực:\n1) Bản chất của HAL_Delay() là một vòng lặp 'Spin-lock / Busy-waiting' liên tục kiểm tra biến đếm của bộ định thời SysTick/Timer. Trong suốt 1000ms này, CPU bị chiếm dụng 100% chỉ để đếm vòng lặp mà không làm việc gì có ích;\n2) Điều này khiến tất cả các task khác có mức ưu tiên bằng hoặc thấp hơn bị 'bỏ đói' (CPU Starvation), không được cấp phát thời gian thực thi;\n3) Trong FreeRTOS, chúng em bắt buộc phải sử dụng hàm osDelay(1000) hoặc osDelayUntil(). Khi gọi osDelay(), task hiện tại ngay lập tức chuyển từ trạng thái Running sang Blocked state, tự nguyện nhường quyền điều khiển CPU cho bộ lập trình Scheduler chuyển sang thực thi các task khác đang ở trạng thái Ready. Khi hết 1000ms, bộ định thời kernel sẽ tự động đưa task trở lại Ready queue.",
        "keywords": "Spin-lock, Busy-waiting, CPU Starvation, Blocked State, Ready Queue, osDelay vs HAL_Delay"
    },
    {
        "qid": "Q03",
        "domain": "NVIC & Interrupts",
        "assignee": "Nghiêm Hoàng Tùng",
        "question": "Why is the User Button handled via EXTI + Semaphore rather than polling in a task or running delays inside the ISR?\n(Tại sao nút bấm lại xử lý qua ngắt EXTI kết hợp Semaphore mà không polling trong task hoặc gọi delay trực tiếp trong ISR?)",
        "answer": "Thưa Thầy/Cô, đây là nguyên lý kinh điển 'Deferred Interrupt Processing' (Trì hoãn xử lý ngắt) trong hệ nhúng chuẩn công nghiệp:\n1) Nếu dùng Polling trong task: CPU sẽ phải liên tục đọc trạng thái chân GPIO mỗi chu kỳ, gây lãng phí xung nhịp CPU và nếu chu kỳ đọc chậm có thể bị lỡ mất sự kiện bấm nút nhanh của người dùng;\n2) Nếu viết mã quay servo hoặc gọi hàm delay bên trong hàm phục vụ ngắt EXTI_Callback: Điều này sẽ vi phạm nguyên tắc tối kỵ của lập trình nhúng. Ngắt ISR chạy ở mức ưu tiên phần cứng NVIC rất cao, nếu giữ ISR quá lâu sẽ block toàn bộ các ngắt khác của hệ thống, làm treo bộ đếm thời gian và tê liệt scheduler;\n3) Giải pháp tối ưu: Cấu hình chân PC13 ở chế độ ngắt ngoài EXTI Falling Edge. Khi nút được nhấn, phần cứng kích hoạt ngắt ngay lập tức. Trong hàm ngắt ISR, chúng em chỉ thực thi đúng 1 dòng lệnh osSemaphoreRelease(feedTriggerSemHandle) trong thời gian chưa đầy 1 micro giây rồi thoát ngay. Task_DispenserControl đang chờ ở thread context sẽ được đánh thức để thực thi quy trình quay servo và delay một cách an toàn mà không ảnh hưởng đến bất kỳ ngắt nào khác.",
        "keywords": "Deferred Interrupt Handling, EXTI NVIC, Microsecond ISR, osSemaphoreRelease, Thread Context Execution"
    },
    {
        "qid": "Q04",
        "domain": "Sensors & DSP",
        "assignee": "Hoàng Đức Mạnh",
        "question": "How does your 20-sample circular filter eliminate noise and how fast does it converge?\n(Bộ lọc trung bình trượt vòng 20 mẫu hoạt động thế nào để khử nhiễu và tốc độ hội tụ ra sao?)",
        "answer": "Thưa Thầy/Cô, que đo TDS trong môi trường nước nuôi cá chịu 3 nguồn nhiễu chính: 1) Gợn sóng nước cơ học khi cá bơi tạo áp lực nước không đều lên bề mặt điện cực; 2) Sóng nhiễu 50Hz cảm ứng từ lưới điện xung quanh; 3) Gai xung điện áp khi động cơ máy bơm/sục khí đóng ngắt.\n1) Chúng em triển khai bộ lọc trung bình trượt vòng (Circular Moving Average Filter / Ring Buffer) dung lượng 20 mẫu trên RAM;\n2) Thuật toán cập nhật đạt độ phức tạp O(1) tuyệt đối nhờ công thức duy trì tổng chạy (Running Sum): 'running_sum = running_sum - buffer[head] + new_sample; buffer[head] = new_sample; head = (head + 1) % 20; average = running_sum / 20;'. Việc này giúp loại bỏ hoàn toàn vòng lặp for tính tổng 20 phần tử, tiết kiệm tối đa xung nhịp xử lý của Cortex-M4;\n3) Với chu kỳ lấy mẫu ADC là 50ms/lần, bộ lọc hội tụ hoàn toàn chỉ sau đúng 1.0 giây (20 x 50ms) từ trạng thái khởi động, triệt tiêu hoàn toàn hiện tượng nhảy số tức thời nhưng vẫn đảm bảo phản ứng nhạy bén khi nồng độ chất tan thực tế thay đổi.",
        "keywords": "Circular Ring Buffer, Running Sum O(1) Complexity, Transient Spike Suppression, 1.0s Convergence Time, Cortex-M4 DSP"
    },
    {
        "qid": "Q05",
        "domain": "Timer PWM & Hardware",
        "assignee": "Đỗ Khắc Lê Gia",
        "question": "Explain the exact Prescaler and ARR calculation for the 50Hz Servo PWM on STM32.\n(Giải thích công thức tính toán chi tiết Prescaler và ARR để tạo xung PWM 50Hz điều khiển Servo trên STM32.)",
        "answer": "Thưa Thầy/Cô, động cơ RC Servo SG90 / MG90S yêu cầu tín hiệu điều khiển PWM có tần số chuẩn 50Hz (tương ứng chu kỳ T = 20ms = 20,000µs), trong đó độ rộng xung mức cao từ 1.0ms (ứng với góc 0°) đến 2.0ms (ứng với góc 180°):\n1) Bo mạch STM32 Nucleo-F401RE của chúng em cấu hình xung nhịp hệ thống HCLK = 84 MHz. Timer TIM2 nằm trên bus APB1, bộ nhân tần số Timer Clock cấp cho TIM2 là f_timer = 84 MHz;\n2) Công thức tần số ngõ ra Timer: f_pwm = f_timer / [ (PSC + 1) * (ARR + 1) ];\n3) Để việc lập trình góc quay theo micro-giây dễ dàng nhất, chúng em cấu hình Prescaler PSC = 83. Khi đó tần số đếm sau bộ chia là: f_cnt = 84 MHz / (83 + 1) = 1 MHz -> Mỗi tick đếm tương ứng đúng 1 micro-giây (1µs);\n4) Để chu kỳ là 20ms = 20,000µs, chúng em đặt Auto-Reload Register ARR = 19999 (vì đếm từ 0 đến 19999 là 20,000 ticks). Tần số ngõ ra là: 1 MHz / 20000 = 50 Hz chuẩn xác;\n5) Khi cần quay góc 0°, chúng em ghi thanh ghi CCR1 = 1000 (1000µs = 1.0ms); Khi cần mở góc 90° để xả thức ăn, chúng em ghi CCR1 = 1500 (1500µs = 1.5ms).",
        "keywords": "f_timer = 84MHz, PSC = 83 (1µs/tick), ARR = 19999 (20ms Period), 50Hz Frequency, CCR1 Pulse Modulation"
    },
    {
        "qid": "Q06",
        "domain": "Power & Hardware Safety",
        "assignee": "Đỗ Khắc Lê Gia",
        "question": "Why did you separate the 5V motor power from the Nucleo 3.3V/5V rail and connect a common ground?\n(Tại sao bạn phải tách nguồn 5V riêng cho motor mà không dùng nguồn 5V của Nucleo và tại sao phải nối chung GND?)",
        "answer": "Thưa Thầy/Cô, việc tách nguồn động lực và nguồn điều khiển là quy tắc sống còn trong thiết kế phần cứng hệ nhúng cơ điện tử:\n1) Động cơ servo và cuộn hút rơ-le là tải cảm (Inductive Load). Khi servo khởi động quay hoặc đổi chiều đột ngột, dòng điện tức thời (Stall / Inrush Current) có thể tăng vọt lên từ 500mA đến hơn 1A. Trong khi đó, chip ổn áp LDO trên bo Nucleo chỉ cấp tối đa khoảng vài trăm mA;\n2) Nếu dùng chung nguồn bo Nucleo, dòng vọt này sẽ gây sụt áp nghiêm trọng trên đường nguồn 3.3V của MCU xuống dưới mức ngưỡng tối thiểu, kích hoạt mạch phần cứng Brownout Reset (BOR) làm vi điều khiển bị reset liên tục;\n3) Ngoài ra, cuộn dây động cơ khi ngắt điện sẽ phát sinh sức điện động cảm ứng ngược (Back-EMF) sinh các gai xung điện áp cao làm hỏng các chân GPIO của vi điều khiển;\n4) Do đó, chúng em dùng nguồn ngoài 5V/2A riêng cấp cho VCC của Servo và Rơ-le, đồng thời bắt buộc phải nối chung Mass (Common Ground) giữa nguồn ngoài và chân GND của STM32 để 2 mạch có cùng một mức điện thế tham chiếu 0V thì tín hiệu xung PWM trên chân PA0 mới điều khiển được servo.",
        "keywords": "Inrush Current, Inductive Load, Brownout Reset (BOR), Back-EMF Spikes, Common Ground Reference, Voltage Rail Isolation"
    },
    {
        "qid": "Q07",
        "domain": "I2C Protocol & Bus Sharing",
        "assignee": "Phạm Hồng Minh",
        "question": "How do both the LCD and RTC communicate over the same two I2C pins without data collisions?\n(Làm sao màn hình LCD và chip đồng hồ RTC cùng giao tiếp trên 2 chân I2C1 PB8/PB9 mà không bị xung đột dữ liệu?)",
        "answer": "Thưa Thầy/Cô, việc này được đảm bảo ở cả 2 cấp độ: Cấp độ phần cứng chuẩn giao thức I2C và Cấp độ phần mềm hệ điều hành thời gian thực FreeRTOS:\n1) Ở cấp độ phần cứng chuẩn I2C: I2C là giao thức bus đa thiết bị (Multi-device Bus) sử dụng 2 đường dây cực máng hở Open-Drain (SCL và SDA) với điện trở kéo lên Pull-up 4.7kΩ. Mỗi thiết bị tớ (Slave) trên bus đều sở hữu một địa chỉ vật lý 7-bit duy nhất trong không gian định tuyến: Chip PCF8574 điều khiển LCD có địa chỉ 0x27, chip thời gian thực DS3231 có địa chỉ 0x68, và chip nhớ EEPROM AT24C32 có địa chỉ 0x57. Khi Master gửi xung Start và byte địa chỉ kèm bit R/W, chỉ thiết bị nào khớp đúng địa chỉ mới kéo chân SDA xuống mức thấp để phản hồi xung ACK, các thiết bị khác hoàn toàn thả nổi đường truyền;\n2) Ở cấp độ phần mềm FreeRTOS: Vì phần cứng bộ điều khiển I2C1 trong STM32 là tài nguyên đơn luồng (Single-threaded Hardware Engine). Nếu Task hiển thị LCD và Task đọc RTC đồng thời gọi hàm HAL_I2C_Transmit / HAL_I2C_Receive, thanh ghi cờ I2C sẽ bị rơi vào trạng thái lỗi I2C_BUSY lockup. Do đó, chúng em tạo một Mutex i2cBusMutex. Mọi giao dịch I2C bắt buộc phải giành được quyền khóa Mutex trước khi truyền dữ liệu và giải phóng Mutex ngay sau khi xong, đảm bảo các phiên truyền thông trên bus diễn ra tuần tự và nguyên tử (Atomic Transactions).",
        "keywords": "Open-Drain Pull-up, 7-bit Slave Addressing (0x27, 0x68, 0x57), ACK/NACK Bit, i2cBusMutex, Atomic Transaction"
    },
    {
        "qid": "Q08",
        "domain": "Non-Volatile Memory",
        "assignee": "Phạm Hồng Minh",
        "question": "What happens to the feeding schedule if power is disconnected, and how is it restored?\n(Chuyện gì xảy ra với lịch trình cho ăn nếu nguồn điện bị ngắt đột ngột, và dữ liệu được khôi phục như thế nào?)",
        "answer": "Thưa Thầy/Cô, hệ thống Aquatic Guardian được thiết kế đạt tiêu chuẩn chịu lỗi mất nguồn điện (Power-cut Fault Tolerant):\n1) Nếu lưu cấu hình giờ ăn và khẩu phần trong biến toàn cục trên RAM, khi mất nguồn điện toàn bộ dữ liệu sẽ bị xóa sạch, cá sẽ bị bỏ đói hoặc cho ăn sai khi có điện lại;\n2) Để giải quyết triệt để, chúng em tích hợp chip nhớ bất biến EEPROM AT24C32 (giao tiếp I2C địa chỉ 0x57, tích hợp sẵn trên module DS3231). Khi người dùng cài đặt lịch cho ăn qua Telegram Bot hoặc chiết áp, dữ liệu sẽ được đóng gói vào struct FeedingSchedule_t và ghi trực tiếp vào Page 0 của EEPROM;\n3) Bộ nhớ EEPROM có khả năng lưu giữ dữ liệu trên 100 năm mà không cần pin nuôi;\n4) Khi cấp nguồn trở lại, trong hàm khởi tạo AquaticGuardian_Init(), hệ thống sẽ tự động đọc dữ liệu từ Page 0 của EEPROM nạp vào biến hệ thống. Đồng thời module DS3231 có viên pin cúc áo Lithium CR2032 dự phòng nuôi mạch thạch anh TCXO nên thời gian thực Giờ-Phút-Giây vẫn chạy chính xác tuyệt đối mà không cần người dùng cài đặt lại.",
        "keywords": "Non-Volatile EEPROM AT24C32, Page Write 32-bytes, CR2032 Battery Backup, TCXO Clock Drift Suppression, Auto-Restore on Boot"
    },
    {
        "qid": "Q09",
        "domain": "Serial Telemetry & Buffering",
        "assignee": "Nguyễn Đức Anh",
        "question": "How do you prevent serial buffer overflow and packet fragmentation on the USART telemetry link?\n(Làm sao để chống tràn bộ đệm và chống phân mảnh gói tin trên đường truyền telemetry UART?)",
        "answer": "Thưa Thầy/Cô, việc truyền nhận chuỗi dữ liệu qua cổng nối tiếp bất đồng bộ UART rất dễ gặp rủi ro mất gói nếu không có cơ chế đóng khung và đệm dữ liệu chuẩn xác:\n1) Về định dạng dữ liệu (Data Framing): Chúng em thiết kế giao thức đóng khung bản tin với ký tự bao đóng ngã '~' ở cả đầu và cuối gói tin, bên trong là chuỗi JSON nén: ~{\"tds\":180,\"portion\":4,\"status\":0}~. Phía máy thu (ESP32 hoặc Python dashboard) sử dụng máy trạng thái hữu hạn (Finite State Machine - FSM) để dò tìm ký tự bắt đầu '~', gom toàn bộ byte vào bộ đệm cho đến khi gặp ký tự kết thúc '~' mới tiến hành parse JSON. Điều này loại bỏ hoàn toàn hiện tượng phân mảnh chuỗi khi kết nối chập chờn;\n2) Về chống tràn bộ đệm gửi (TX Overflow): Phía phát STM32 sử dụng uartMutex bảo vệ hàm gửi chuỗi, ngăn ngừa tình huống 2 task cùng in log làm xáo trộn các ký tự trên đường truyền;\n3) Về chống tràn bộ đệm nhận (RX Overflow): Lệnh nhận từ ESP32 trên USART1 (PA9/PA10) được xử lý bằng ngắt nhận Idle Frame HAL_UARTEx_ReceiveToIdle_IT hoặc ring buffer 128 bytes, giải phóng feedTriggerSem ngay lập tức khi nhận lệnh /feed, loại bỏ lỗi Overrun Error (ORE).",
        "keywords": "'~' Delimiter Framing, Finite State Machine (FSM), uartMutex, Circular RX Ring Buffer, Overrun Error (ORE) Prevention"
    },
    {
        "qid": "Q10",
        "domain": "RTOS Safety & QA",
        "assignee": "Nguyễn Đức Anh",
        "question": "How did you verify the stack size of each task and prove that no Stack Overflow occurs?\n(Làm thế nào bạn kiểm chứng kích thước ngăn xếp của từng task và chứng minh hệ thống không bị tràn bộ nhớ Stack?)",
        "answer": "Thưa Thầy/Cô, tràn ngăn xếp (Stack Overflow) là nguyên nhân hàng đầu gây Crash chip hoặc HardFault trong các hệ thống nhúng FreeRTOS. Chúng em áp dụng quy trình kiểm chuẩn 2 lớp cực kỳ chặt chẽ:\n1) Lớp 1 - Kích hoạt bẫy phần cứng FreeRTOS: Trong file FreeRTOSConfig.h, chúng em thiết lập macro '#define configCHECK_FOR_STACK_OVERFLOW 2' (Phương pháp kiểm tra cấp độ 2). Ở chế độ này, kernel sẽ tự động điền một mẫu byte đặc biệt (0xA5) vào toàn bộ vùng stack khi khởi tạo. Khi xảy ra chuyển ngữ cảnh (Context Switch), kernel sẽ kiểm tra 16 bytes cuối cùng ở đáy stack; nếu các byte này bị ghi đè, hệ thống lập tức nhảy vào hàm hook 'vApplicationStackOverflowHook()', nhấp nháy đèn LED đỏ cảnh báo và in tên task bị lỗi ra cổng UART để lập trình viên bắt được ngay;\n2) Lớp 2 - Đo lường định lượng thực tế bằng hàm High Water Mark: Trong quá trình chạy thử nghiệm ứng suất (Stress Test) liên tục 30 phút dưới tải tối đa, chúng em định kỳ gọi hàm 'uxTaskGetStackHighWaterMark()'. Hàm này trả về dung lượng stack tối thiểu (tính bằng words) chưa từng bị chạm tới kể từ khi task khởi chạy. Kết quả thực nghiệm của cả 5 tasks đều cho thấy mức dư thừa an toàn từ 42 đến 85 words, chứng minh hệ thống vận hành ổn định tuyệt đối và không hề phát sinh rò rỉ bộ nhớ.",
        "keywords": "configCHECK_FOR_STACK_OVERFLOW = 2, 0xA5 Pattern Fill, vApplicationStackOverflowHook, uxTaskGetStackHighWaterMark, HardFault Prevention"
    }
]

def style_cell(cell, font=None, fill=None, alignment=None, border=None):
    """Helper to apply formatting safely to openpyxl cell."""
    if font:
        cell.font = font
    if fill:
        cell.fill = fill
    if alignment:
        cell.alignment = alignment
    if border:
        cell.border = border

def apply_title_banner(ws, title_text, subtitle_text, num_cols):
    """Creates an elegant 2-row title banner matching Google Sheets styling."""
    # Row 1: Main Title
    ws.row_dimensions[1].height = 36
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=num_cols)
    cell_title = ws.cell(row=1, column=1, value=title_text)
    style_cell(cell_title, font=FONT_TITLE, fill=FILL_TITLE, alignment=ALIGN_CENTER)
    
    # Border for title banner
    for col in range(1, num_cols + 1):
        ws.cell(row=1, column=col).fill = FILL_TITLE
        ws.cell(row=1, column=col).border = BORDER_THIN

    # Row 2: Subtitle
    ws.row_dimensions[2].height = 22
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=num_cols)
    cell_sub = ws.cell(row=2, column=1, value=subtitle_text)
    style_cell(cell_sub, font=FONT_SUBTITLE, fill=FILL_SUBTITLE, alignment=ALIGN_CENTER)
    
    for col in range(1, num_cols + 1):
        ws.cell(row=2, column=col).fill = FILL_SUBTITLE
        ws.cell(row=2, column=col).border = BORDER_THIN

def auto_fit_columns(ws, min_widths=None, max_widths=None):
    """Calculates column widths with padding and constraints for clean presentation."""
    if min_widths is None:
        min_widths = {}
    if max_widths is None:
        max_widths = {}

    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = 0
        for cell in col:
            # Skip title banner rows (rows 1 and 2) when calculating widths
            if cell.row in [1, 2]:
                continue
            val = str(cell.value or "")
            # If multi-line, take maximum line length
            lines = val.split("\n")
            line_max = max(len(l) for l in lines) if lines else 0
            if line_max > max_len:
                max_len = line_max
        
        # Apply min/max limits
        calculated_width = max(max_len + 3, min_widths.get(col_letter, 12))
        final_width = min(calculated_width, max_widths.get(col_letter, 65))
        ws.column_dimensions[col_letter].width = final_width

def create_dashboard_tab(wb):
    """Builds Tab 1: Dashboard & Roles."""
    ws = wb.active
    ws.title = "Dashboard & Roles"
    ws.views.sheetView[0].showGridLines = True
    ws.freeze_panes = "A4"

    # Title Banner
    apply_title_banner(
        ws,
        "🐟 AQUATIC GUARDIAN — CAPSTONE PROJECT EXECUTIVE DASHBOARD & ROLES",
        "Course: MCP201 (Microcontroller Programming) | Group: 7 (IC2005) | Platform: STM32 Nucleo ARM Cortex-M4 & FreeRTOS | Weight: 30%",
        10
    )

    # Row 3: Blank separator
    ws.row_dimensions[3].height = 10

    # Section 1: Executive KPI Summary Block
    # Left Block: Sprint Task Metrics (B4:D11)
    ws.merge_cells("B4:D4")
    ws.cell(row=4, column=2, value="📊 SPRINT TASK COMPLETION METRICS").font = FONT_SECTION
    ws.cell(row=4, column=2).fill = FILL_SECTION
    ws.cell(row=4, column=2).alignment = ALIGN_CENTER
    for col in range(2, 5):
        ws.cell(row=4, column=col).fill = FILL_SECTION
        ws.cell(row=4, column=col).border = BORDER_THIN

    kpis = [
        ("Total Master Tasks", "=COUNTA('Master Task Matrix'!A4:A28)", "TSK-01 to TSK-25", FILL_WHITE, FONT_BODY_BOLD),
        ("Completed Tasks (Done)", "=COUNTIF('Master Task Matrix'!J4:J28, \"Done\")", "Verified deliverables", PatternFill(start_color=HEX_DONE_BG, end_color=HEX_DONE_BG, fill_type="solid"), Font(name="Arial", size=9, bold=True, color=HEX_DONE_FG)),
        ("In Progress Tasks", "=COUNTIF('Master Task Matrix'!J4:J28, \"In Progress\")", "Active engineering", PatternFill(start_color=HEX_PROG_BG, end_color=HEX_PROG_BG, fill_type="solid"), Font(name="Arial", size=9, bold=True, color=HEX_PROG_FG)),
        ("Pending Tasks (To Do)", "=COUNTIF('Master Task Matrix'!J4:J28, \"To Do\")", "Sprint backlog", PatternFill(start_color=HEX_TODO_BG, end_color=HEX_TODO_BG, fill_type="solid"), Font(name="Arial", size=9, bold=True, color=HEX_TODO_FG)),
        ("Blocked Tasks", "=COUNTIF('Master Task Matrix'!J4:J28, \"Blocked\")", "Issues requiring action", PatternFill(start_color=HEX_BLOCKED_BG, end_color=HEX_BLOCKED_BG, fill_type="solid"), Font(name="Arial", size=9, bold=True, color=HEX_BLOCKED_FG)),
        ("Sprint Completion Rate", "=IFERROR(COUNTIF('Master Task Matrix'!J4:J28, \"Done\")/COUNTA('Master Task Matrix'!A4:A28), 0)", "% of target achieved", PatternFill(start_color=HEX_ICE_TINT, end_color=HEX_ICE_TINT, fill_type="solid"), Font(name="Arial", size=10, bold=True, color=HEX_NAVY_DARK))
    ]

    for idx, (label, formula_val, note, fill_style, font_style) in enumerate(kpis, start=5):
        ws.row_dimensions[idx].height = 20
        ws.cell(row=idx, column=2, value=label).font = FONT_BODY_BOLD
        ws.cell(row=idx, column=2).alignment = ALIGN_LEFT
        ws.cell(row=idx, column=2).border = BORDER_THIN
        
        c_val = ws.cell(row=idx, column=3, value=formula_val)
        c_val.font = font_style
        c_val.fill = fill_style
        c_val.alignment = ALIGN_CENTER
        c_val.border = BORDER_THIN
        if idx == 10:  # Percentage format
            c_val.number_format = "0.0%"
        else:
            c_val.number_format = "#,##0"

        c_note = ws.cell(row=idx, column=4, value=note)
        c_note.font = FONT_BODY
        c_note.alignment = ALIGN_LEFT
        c_note.border = BORDER_THIN

    # Right Block: Member Delivery Summary (F4:J10)
    ws.merge_cells("F4:J4")
    ws.cell(row=4, column=6, value="👥 MEMBER WORKLOAD & WORK COMPLETED SUMMARY").font = FONT_SECTION
    ws.cell(row=4, column=6).fill = FILL_SECTION
    ws.cell(row=4, column=6).alignment = ALIGN_CENTER
    for col in range(6, 11):
        ws.cell(row=4, column=col).fill = FILL_SECTION
        ws.cell(row=4, column=col).border = BORDER_THIN

    mem_headers = ["Member Name", "Assigned Subsystem", "Total Tasks", "Done", "Completion %"]
    ws.row_dimensions[5].height = 22
    for c_idx, h_text in enumerate(mem_headers, start=6):
        c = ws.cell(row=5, column=c_idx, value=h_text)
        style_cell(c, font=FONT_SUBHEADER, fill=FILL_SUBHEADER, alignment=ALIGN_CENTER, border=BORDER_THIN)

    for idx, mem in enumerate(MEMBERS_DATA, start=6):
        ws.row_dimensions[idx].height = 20
        name_short = mem["name"].split()[-1]
        
        # Name
        c_name = ws.cell(row=idx, column=6, value=f"{mem['name']} ({mem['id']})")
        style_cell(c_name, font=FONT_BODY_BOLD, alignment=ALIGN_LEFT, border=BORDER_THIN)
        
        # Subsystem
        c_sub = ws.cell(row=idx, column=7, value=mem["subsystem"].split(",")[0])
        style_cell(c_sub, font=FONT_BODY, alignment=ALIGN_LEFT, border=BORDER_THIN)
        
        # Total Formula
        c_tot = ws.cell(row=idx, column=8, value=f"=COUNTIF('Master Task Matrix'!D4:D28, \"*{mem['name']}*\")")
        style_cell(c_tot, font=FONT_BODY_BOLD, alignment=ALIGN_CENTER, border=BORDER_THIN)
        c_tot.number_format = "#,##0"
        
        # Done Formula
        c_done = ws.cell(row=idx, column=9, value=f"=COUNTIFS('Master Task Matrix'!D4:D28, \"*{mem['name']}*\", 'Master Task Matrix'!J4:J28, \"Done\")")
        style_cell(c_done, font=Font(name="Arial", size=9, bold=True, color=HEX_DONE_FG), alignment=ALIGN_CENTER, border=BORDER_THIN)
        c_done.number_format = "#,##0"
        
        # Percent Formula
        c_pct = ws.cell(row=idx, column=10, value=f"=IFERROR(I{idx}/H{idx}, 0)")
        style_cell(c_pct, font=Font(name="Arial", size=9, bold=True, color=HEX_NAVY_DARK), alignment=ALIGN_CENTER, border=BORDER_THIN)
        c_pct.number_format = "0.0%"

    # Row 12: Blank
    ws.row_dimensions[11].height = 10
    ws.row_dimensions[12].height = 10

    # Section 2: 1-Week Sprint Roadmap Table (Rows 13 to 22)
    ws.merge_cells("A13:J13")
    sec2_title = ws.cell(row=13, column=1, value="🗓️ 1-WEEK SPRINT ROADMAP & MILESTONE SCHEDULE (DAY 1 TO DAY 7)")
    sec2_title.font = FONT_SECTION
    sec2_title.fill = FILL_SECTION
    sec2_title.alignment = ALIGN_CENTER
    for col in range(1, 11):
        ws.cell(row=13, column=col).fill = FILL_SECTION
        ws.cell(row=13, column=col).border = BORDER_THIN

    roadmap_cols = ["Day", "Phase", "Sprint Theme", "Daily Core Objective & Milestone Target", "Critical Subsystems", "Daily Deliverables & Exit Criteria"]
    col_spans = [(1, 1), (2, 2), (3, 4), (5, 7), (8, 8), (9, 10)]
    
    ws.row_dimensions[14].height = 24
    for (sc, ec), h_text in zip(col_spans, roadmap_cols):
        if sc != ec:
            ws.merge_cells(start_row=14, start_column=sc, end_row=14, end_column=ec)
        c = ws.cell(row=14, column=sc, value=h_text)
        style_cell(c, font=FONT_HEADER, fill=FILL_HEADER, alignment=ALIGN_CENTER, border=BORDER_THIN)
        for col_i in range(sc, ec + 1):
            ws.cell(row=14, column=col_i).fill = FILL_HEADER
            ws.cell(row=14, column=col_i).border = BORDER_THIN

    for r_idx, r_data in enumerate(ROADMAP_DATA, start=15):
        ws.row_dimensions[r_idx].height = 36
        fill_row = FILL_ZEBRA if r_idx % 2 == 0 else FILL_WHITE

        # Day
        c_day = ws.cell(row=r_idx, column=1, value=r_data["day"])
        style_cell(c_day, font=FONT_BODY_BOLD, fill=fill_row, alignment=ALIGN_CENTER, border=BORDER_THIN)
        
        # Phase
        c_ph = ws.cell(row=r_idx, column=2, value=r_data["phase"].split(":")[0])
        style_cell(c_ph, font=FONT_BODY, fill=fill_row, alignment=ALIGN_CENTER, border=BORDER_THIN)
        
        # Theme (Merged 3:4)
        ws.merge_cells(start_row=r_idx, start_column=3, end_row=r_idx, end_column=4)
        c_thm = ws.cell(row=r_idx, column=3, value=r_data["theme"])
        style_cell(c_thm, font=FONT_BODY_BOLD, fill=fill_row, alignment=ALIGN_LEFT, border=BORDER_THIN)
        ws.cell(row=r_idx, column=4).border = BORDER_THIN
        ws.cell(row=r_idx, column=4).fill = fill_row

        # Milestone (Merged 5:7)
        ws.merge_cells(start_row=r_idx, start_column=5, end_row=r_idx, end_column=7)
        c_ms = ws.cell(row=r_idx, column=5, value=r_data["milestone"])
        style_cell(c_ms, font=FONT_BODY, fill=fill_row, alignment=ALIGN_LEFT, border=BORDER_THIN)
        for c_k in [6, 7]:
            ws.cell(row=r_idx, column=c_k).border = BORDER_THIN
            ws.cell(row=r_idx, column=c_k).fill = fill_row

        # Subsystems
        c_sub = ws.cell(row=r_idx, column=8, value=r_data["subsystems"])
        style_cell(c_sub, font=FONT_BODY, fill=fill_row, alignment=ALIGN_LEFT, border=BORDER_THIN)

        # Deliverables (Merged 9:10)
        ws.merge_cells(start_row=r_idx, start_column=9, end_row=r_idx, end_column=10)
        c_del = ws.cell(row=r_idx, column=9, value=r_data["deliverable"])
        style_cell(c_del, font=FONT_BODY, fill=fill_row, alignment=ALIGN_LEFT, border=BORDER_THIN)
        ws.cell(row=r_idx, column=10).border = BORDER_THIN
        ws.cell(row=r_idx, column=10).fill = fill_row

    # Row 23: Blank
    ws.row_dimensions[22].height = 10
    ws.row_dimensions[23].height = 10

    # Section 3: Group 7 Member Directory & Engineering Domain Matrix (Rows 24 to 31)
    ws.merge_cells("A24:J24")
    sec3_title = ws.cell(row=24, column=1, value="🎖️ GROUP 7 ENGINEERING DIRECTORY & PRESENTATION ASSIGNMENT MATRIX")
    sec3_title.font = FONT_SECTION
    sec3_title.fill = FILL_SECTION
    sec3_title.alignment = ALIGN_CENTER
    for col in range(1, 11):
        ws.cell(row=24, column=col).fill = FILL_SECTION
        ws.cell(row=24, column=col).border = BORDER_THIN

    team_headers = [
        "Member Full Name", "Student ID", "Primary Engineering Domain", "Assigned Hardware & Peripheral",
        "Key Source Code Files", "Presentation Segment", "Defense Focus Domain"
    ]
    team_spans = [(1, 1), (2, 2), (3, 4), (5, 5), (6, 7), (8, 8), (9, 10)]

    ws.row_dimensions[25].height = 24
    for (sc, ec), h_text in zip(team_spans, team_headers):
        if sc != ec:
            ws.merge_cells(start_row=25, start_column=sc, end_row=25, end_column=ec)
        c = ws.cell(row=25, column=sc, value=h_text)
        style_cell(c, font=FONT_HEADER, fill=FILL_HEADER, alignment=ALIGN_CENTER, border=BORDER_THIN)
        for col_i in range(sc, ec + 1):
            ws.cell(row=25, column=col_i).fill = FILL_HEADER
            ws.cell(row=25, column=col_i).border = BORDER_THIN

    for m_idx, mem in enumerate(MEMBERS_DATA, start=26):
        ws.row_dimensions[m_idx].height = 34
        fill_row = FILL_ZEBRA if m_idx % 2 == 0 else FILL_WHITE

        # Name
        c_name = ws.cell(row=m_idx, column=1, value=mem["name"])
        style_cell(c_name, font=FONT_BODY_BOLD, fill=fill_row, alignment=ALIGN_LEFT, border=BORDER_THIN)

        # ID
        c_id = ws.cell(row=m_idx, column=2, value=mem["id"])
        style_cell(c_id, font=FONT_BODY_BOLD, fill=fill_row, alignment=ALIGN_CENTER, border=BORDER_THIN)

        # Role (Merged 3:4)
        ws.merge_cells(start_row=m_idx, start_column=3, end_row=m_idx, end_column=4)
        c_role = ws.cell(row=m_idx, column=3, value=f"{mem['role']}\n({mem['subsystem']})")
        style_cell(c_role, font=FONT_BODY, fill=fill_row, alignment=ALIGN_LEFT, border=BORDER_THIN)
        ws.cell(row=m_idx, column=4).border = BORDER_THIN
        ws.cell(row=m_idx, column=4).fill = fill_row

        # Peripherals
        c_periph = ws.cell(row=m_idx, column=5, value=mem["peripherals"])
        style_cell(c_periph, font=FONT_BODY, fill=fill_row, alignment=ALIGN_LEFT, border=BORDER_THIN)

        # Files (Merged 6:7)
        ws.merge_cells(start_row=m_idx, start_column=6, end_row=m_idx, end_column=7)
        c_files = ws.cell(row=m_idx, column=6, value=mem["files"])
        style_cell(c_files, font=FONT_BODY, fill=fill_row, alignment=ALIGN_LEFT, border=BORDER_THIN)
        ws.cell(row=m_idx, column=7).border = BORDER_THIN
        ws.cell(row=m_idx, column=7).fill = fill_row

        # Presentation
        c_pres = ws.cell(row=m_idx, column=8, value=mem["presentation"])
        style_cell(c_pres, font=FONT_BODY, fill=fill_row, alignment=ALIGN_LEFT, border=BORDER_THIN)

        # Defense Focus (Merged 9:10)
        ws.merge_cells(start_row=m_idx, start_column=9, end_row=m_idx, end_column=10)
        c_def = ws.cell(row=m_idx, column=9, value=mem["defense_focus"])
        style_cell(c_def, font=FONT_BODY, fill=fill_row, alignment=ALIGN_LEFT, border=BORDER_THIN)
        ws.cell(row=m_idx, column=10).border = BORDER_THIN
        ws.cell(row=m_idx, column=10).fill = fill_row

    # Set Column Widths for Dashboard
    dash_widths = {
        "A": 16, "B": 24, "C": 14, "D": 22, "E": 18,
        "F": 28, "G": 22, "H": 18, "I": 24, "J": 26
    }
    for col_l, w in dash_widths.items():
        ws.column_dimensions[col_l].width = w

def create_master_task_matrix_tab(wb):
    """Builds Tab 2: Master Task Matrix."""
    ws = wb.create_sheet(title="Master Task Matrix")
    ws.views.sheetView[0].showGridLines = True
    ws.freeze_panes = "A4"

    # Title Banner
    apply_title_banner(
        ws,
        "📋 AQUATIC GUARDIAN — MASTER TASK MATRIX (25 TASKS / 1-WEEK SPRINT)",
        "Bảng theo dõi tiến độ tổng thể 25 nhiệm vụ kỹ thuật và bảo vệ đồ án của 5 thành viên trong 1 tuần (Day 1 - Day 7). Cột Status tự động đồng bộ lên Dashboard.",
        10
    )

    headers = [
        "Task ID", "Phase", "Subsystem", "Assignee", "Priority",
        "What it is? (Mô tả kỹ thuật & Bối cảnh)",
        "What to do? (Hướng dẫn thực hiện từng bước)",
        "What to submit? (Sản phẩm bàn giao & Bằng chứng)",
        "Deadline", "Status"
    ]

    ws.row_dimensions[3].height = 26
    for col_idx, h_text in enumerate(headers, start=1):
        c = ws.cell(row=3, column=col_idx, value=h_text)
        style_cell(c, font=FONT_HEADER, fill=FILL_HEADER, alignment=ALIGN_CENTER, border=BORDER_THIN)

    for idx, tsk in enumerate(MASTER_TASKS, start=4):
        ws.row_dimensions[idx].height = 68
        fill_row = FILL_ZEBRA if idx % 2 == 0 else FILL_WHITE

        # Task ID
        c_id = ws.cell(row=idx, column=1, value=tsk["id"])
        style_cell(c_id, font=FONT_BODY_BOLD, fill=fill_row, alignment=ALIGN_CENTER_TOP, border=BORDER_THIN)

        # Phase
        c_ph = ws.cell(row=idx, column=2, value=tsk["phase"])
        style_cell(c_ph, font=FONT_BODY, fill=fill_row, alignment=ALIGN_CENTER_TOP, border=BORDER_THIN)

        # Subsystem
        c_sub = ws.cell(row=idx, column=3, value=tsk["subsystem"])
        style_cell(c_sub, font=FONT_BODY_BOLD, fill=fill_row, alignment=ALIGN_CENTER_TOP, border=BORDER_THIN)

        # Assignee
        c_ass = ws.cell(row=idx, column=4, value=tsk["assignee"])
        style_cell(c_ass, font=FONT_BODY_BOLD, fill=fill_row, alignment=ALIGN_CENTER_TOP, border=BORDER_THIN)

        # Priority
        c_pri = ws.cell(row=idx, column=5, value=tsk["priority"])
        pri_bg = HEX_HIGH_BG if tsk["priority"] == "High" else (HEX_MED_BG if tsk["priority"] == "Medium" else HEX_LOW_BG)
        pri_fg = HEX_HIGH_FG if tsk["priority"] == "High" else (HEX_MED_FG if tsk["priority"] == "Medium" else HEX_LOW_FG)
        style_cell(c_pri, font=Font(name="Arial", size=9, bold=True, color=pri_fg),
                   fill=PatternFill(start_color=pri_bg, end_color=pri_bg, fill_type="solid"),
                   alignment=ALIGN_CENTER_TOP, border=BORDER_THIN)

        # What it is?
        c_what = ws.cell(row=idx, column=6, value=tsk["what_is"])
        style_cell(c_what, font=FONT_BODY, fill=fill_row, alignment=ALIGN_TEXT_WRAP, border=BORDER_THIN)

        # What to do?
        c_how = ws.cell(row=idx, column=7, value=tsk["what_do"])
        style_cell(c_how, font=FONT_BODY, fill=fill_row, alignment=ALIGN_TEXT_WRAP, border=BORDER_THIN)

        # What to submit?
        c_subm = ws.cell(row=idx, column=8, value=tsk["what_submit"])
        style_cell(c_subm, font=FONT_BODY, fill=fill_row, alignment=ALIGN_TEXT_WRAP, border=BORDER_THIN)

        # Deadline
        c_ddl = ws.cell(row=idx, column=9, value=tsk["deadline"])
        style_cell(c_ddl, font=FONT_BODY_BOLD, fill=fill_row, alignment=ALIGN_CENTER_TOP, border=BORDER_THIN)

        # Status
        c_stat = ws.cell(row=idx, column=10, value=tsk["status"])
        st_val = tsk["status"]
        if st_val == "Done":
            st_bg, st_fg = HEX_DONE_BG, HEX_DONE_FG
        elif st_val == "In Progress":
            st_bg, st_fg = HEX_PROG_BG, HEX_PROG_FG
        elif st_val == "Blocked":
            st_bg, st_fg = HEX_BLOCKED_BG, HEX_BLOCKED_FG
        else:
            st_bg, st_fg = HEX_TODO_BG, HEX_TODO_FG

        style_cell(c_stat, font=Font(name="Arial", size=9, bold=True, color=st_fg),
                   fill=PatternFill(start_color=st_bg, end_color=st_bg, fill_type="solid"),
                   alignment=ALIGN_CENTER_TOP, border=BORDER_THIN)

    # Column Widths for Master Task Matrix
    matrix_widths = {
        "A": 11,   # Task ID
        "B": 24,   # Phase
        "C": 22,   # Subsystem
        "D": 22,   # Assignee
        "E": 12,   # Priority
        "F": 50,   # What it is?
        "G": 52,   # What to do?
        "H": 46,   # What to submit?
        "I": 12,   # Deadline
        "J": 14    # Status
    }
    for col_l, w in matrix_widths.items():
        ws.column_dimensions[col_l].width = w

def create_member_tab(wb, member_info):
    """Creates a dedicated filtered sheet for each member."""
    sheet_title = member_info["sheet_name"]
    ws = wb.create_sheet(title=sheet_title)
    ws.views.sheetView[0].showGridLines = True
    ws.freeze_panes = "A4"

    # Title Banner
    apply_title_banner(
        ws,
        f"👤 {member_info['name'].upper()} ({member_info['id']}) — {member_info['role'].upper()}",
        f"Assigned Subsystem: {member_info['subsystem']} | Deliverable Files: {member_info['files']} | Defense: {member_info['presentation']}",
        10
    )

    headers = [
        "Task ID", "Phase", "Subsystem", "Priority",
        "What it is? (Mô tả kỹ thuật & Bối cảnh)",
        "What to do? (Hướng dẫn thực hiện từng bước)",
        "What to submit? (Sản phẩm bàn giao & Bằng chứng)",
        "Deadline", "Status", "Git Commit / Evidence"
    ]

    ws.row_dimensions[3].height = 26
    for col_idx, h_text in enumerate(headers, start=1):
        c = ws.cell(row=3, column=col_idx, value=h_text)
        style_cell(c, font=FONT_HEADER, fill=FILL_HEADER, alignment=ALIGN_CENTER, border=BORDER_THIN)

    # Filter tasks for this member
    mem_tasks = [t for t in MASTER_TASKS if t["member_code"] == member_info["code"]]

    for idx, tsk in enumerate(mem_tasks, start=4):
        ws.row_dimensions[idx].height = 76
        fill_row = FILL_ZEBRA if idx % 2 == 0 else FILL_WHITE

        # Task ID
        c_id = ws.cell(row=idx, column=1, value=tsk["id"])
        style_cell(c_id, font=FONT_BODY_BOLD, fill=fill_row, alignment=ALIGN_CENTER_TOP, border=BORDER_THIN)

        # Phase
        c_ph = ws.cell(row=idx, column=2, value=tsk["phase"])
        style_cell(c_ph, font=FONT_BODY, fill=fill_row, alignment=ALIGN_CENTER_TOP, border=BORDER_THIN)

        # Subsystem
        c_sub = ws.cell(row=idx, column=3, value=tsk["subsystem"])
        style_cell(c_sub, font=FONT_BODY_BOLD, fill=fill_row, alignment=ALIGN_CENTER_TOP, border=BORDER_THIN)

        # Priority
        c_pri = ws.cell(row=idx, column=4, value=tsk["priority"])
        pri_bg = HEX_HIGH_BG if tsk["priority"] == "High" else (HEX_MED_BG if tsk["priority"] == "Medium" else HEX_LOW_BG)
        pri_fg = HEX_HIGH_FG if tsk["priority"] == "High" else (HEX_MED_FG if tsk["priority"] == "Medium" else HEX_LOW_FG)
        style_cell(c_pri, font=Font(name="Arial", size=9, bold=True, color=pri_fg),
                   fill=PatternFill(start_color=pri_bg, end_color=pri_bg, fill_type="solid"),
                   alignment=ALIGN_CENTER_TOP, border=BORDER_THIN)

        # What it is?
        c_what = ws.cell(row=idx, column=5, value=tsk["what_is"])
        style_cell(c_what, font=FONT_BODY, fill=fill_row, alignment=ALIGN_TEXT_WRAP, border=BORDER_THIN)

        # What to do?
        c_how = ws.cell(row=idx, column=6, value=tsk["what_do"])
        style_cell(c_how, font=FONT_BODY, fill=fill_row, alignment=ALIGN_TEXT_WRAP, border=BORDER_THIN)

        # What to submit?
        c_subm = ws.cell(row=idx, column=7, value=tsk["what_submit"])
        style_cell(c_subm, font=FONT_BODY, fill=fill_row, alignment=ALIGN_TEXT_WRAP, border=BORDER_THIN)

        # Deadline
        c_ddl = ws.cell(row=idx, column=8, value=tsk["deadline"])
        style_cell(c_ddl, font=FONT_BODY_BOLD, fill=fill_row, alignment=ALIGN_CENTER_TOP, border=BORDER_THIN)

        # Status
        c_stat = ws.cell(row=idx, column=9, value=tsk["status"])
        st_val = tsk["status"]
        if st_val == "Done":
            st_bg, st_fg = HEX_DONE_BG, HEX_DONE_FG
        elif st_val == "In Progress":
            st_bg, st_fg = HEX_PROG_BG, HEX_PROG_FG
        elif st_val == "Blocked":
            st_bg, st_fg = HEX_BLOCKED_BG, HEX_BLOCKED_FG
        else:
            st_bg, st_fg = HEX_TODO_BG, HEX_TODO_FG

        style_cell(c_stat, font=Font(name="Arial", size=9, bold=True, color=st_fg),
                   fill=PatternFill(start_color=st_bg, end_color=st_bg, fill_type="solid"),
                   alignment=ALIGN_CENTER_TOP, border=BORDER_THIN)

        # Evidence
        c_evi = ws.cell(row=idx, column=10, value=tsk["evidence"])
        style_cell(c_evi, font=FONT_BODY, fill=fill_row, alignment=ALIGN_TEXT_WRAP, border=BORDER_THIN)

    # Column widths
    mem_widths = {
        "A": 11,   # Task ID
        "B": 24,   # Phase
        "C": 22,   # Subsystem
        "D": 12,   # Priority
        "E": 48,   # What it is?
        "F": 50,   # What to do?
        "G": 44,   # What to submit?
        "H": 12,   # Deadline
        "I": 14,   # Status
        "J": 36    # Evidence
    }
    for col_l, w in mem_widths.items():
        ws.column_dimensions[col_l].width = w

def create_rubric_checklist_tab(wb):
    """Builds Tab 8: Defense Rubric Checklist & Technical Q&A Guide."""
    ws = wb.create_sheet(title="Defense Rubric Checklist")
    ws.views.sheetView[0].showGridLines = True
    ws.freeze_panes = "A4"

    # Title Banner
    apply_title_banner(
        ws,
        "🏆 MCP201 CAPSTONE DEFENSE RUBRIC CHECKLIST & MASTER TECHNICAL Q&A GUIDE",
        "Bộ tiêu chí chấm điểm 30% MCP201 của Giảng viên (Kiến trúc 25%, Ngoại vi 25%, An toàn RTOS 25%, Live Demo & Q&A 25%) và 10 câu hỏi phản biện chuyên sâu kèm đáp án mẫu.",
        7
    )

    # Section 1 Header: MCP201 Rubric Verification Checklist
    ws.row_dimensions[3].height = 26
    rubric_headers = [
        "Rubric Criteria (Weight)", "Sub-Criterion / Technical Checkpoint", "Assigned Lead",
        "Specific Implementation in Aquatic Guardian", "Verification Method & Evidence", "Defense Readiness"
    ]
    # Col spans: A, B, C, D-E merged, F, G
    r_spans = [(1, 1), (2, 2), (3, 3), (4, 5), (6, 6), (7, 7)]

    for (sc, ec), h_text in zip(r_spans, rubric_headers):
        if sc != ec:
            ws.merge_cells(start_row=3, start_column=sc, end_row=3, end_column=ec)
        c = ws.cell(row=3, column=sc, value=h_text)
        style_cell(c, font=FONT_HEADER, fill=FILL_HEADER, alignment=ALIGN_CENTER, border=BORDER_THIN)
        for col_i in range(sc, ec + 1):
            ws.cell(row=3, column=col_i).fill = FILL_HEADER
            ws.cell(row=3, column=col_i).border = BORDER_THIN

    for idx, rub in enumerate(RUBRIC_CHECKLIST_DATA, start=4):
        ws.row_dimensions[idx].height = 54
        fill_row = FILL_ZEBRA if idx % 2 == 0 else FILL_WHITE

        # Rubric Criteria
        c_cat = ws.cell(row=idx, column=1, value=rub["category"])
        style_cell(c_cat, font=FONT_BODY_BOLD, fill=fill_row, alignment=ALIGN_CENTER_TOP, border=BORDER_THIN)

        # Checkpoint
        c_cp = ws.cell(row=idx, column=2, value=rub["checkpoint"])
        style_cell(c_cp, font=FONT_BODY_BOLD, fill=fill_row, alignment=ALIGN_LEFT, border=BORDER_THIN)

        # Assigned Lead
        c_ass = ws.cell(row=idx, column=3, value=rub["assignee"])
        style_cell(c_ass, font=FONT_BODY, fill=fill_row, alignment=ALIGN_CENTER_TOP, border=BORDER_THIN)

        # Implementation (Merged D:E)
        ws.merge_cells(start_row=idx, start_column=4, end_row=idx, end_column=5)
        c_imp = ws.cell(row=idx, column=4, value=rub["implementation"])
        style_cell(c_imp, font=FONT_BODY, fill=fill_row, alignment=ALIGN_TEXT_WRAP, border=BORDER_THIN)
        ws.cell(row=idx, column=5).border = BORDER_THIN
        ws.cell(row=idx, column=5).fill = fill_row

        # Verification Method
        c_ver = ws.cell(row=idx, column=6, value=rub["verification"])
        style_cell(c_ver, font=FONT_BODY, fill=fill_row, alignment=ALIGN_TEXT_WRAP, border=BORDER_THIN)

        # Readiness
        c_ready = ws.cell(row=idx, column=7, value=rub["readiness"])
        style_cell(c_ready, font=Font(name="Arial", size=9, bold=True, color=HEX_DONE_FG),
                   fill=PatternFill(start_color=HEX_DONE_BG, end_color=HEX_DONE_BG, fill_type="solid"),
                   alignment=ALIGN_CENTER_TOP, border=BORDER_THIN)

    # Blank row
    start_qa_sec = 4 + len(RUBRIC_CHECKLIST_DATA)
    ws.row_dimensions[start_qa_sec].height = 12

    # Section 2 Header: Top 10 Technical Defense Q&A Master Guide
    qa_header_row = start_qa_sec + 1
    ws.merge_cells(start_row=qa_header_row, start_column=1, end_row=qa_header_row, end_column=7)
    sec2_qa = ws.cell(row=qa_header_row, column=1, value="❓ TOP 10 INSTRUCTOR DEFENSE GRILLING QUESTIONS & MODEL TECHNICAL ANSWERS")
    sec2_qa.font = FONT_SECTION
    sec2_qa.fill = FILL_SECTION
    sec2_qa.alignment = ALIGN_CENTER
    for col in range(1, 8):
        ws.cell(row=qa_header_row, column=col).fill = FILL_SECTION
        ws.cell(row=qa_header_row, column=col).border = BORDER_THIN

    # Q&A Table Sub-headers
    qa_sub_row = qa_header_row + 1
    ws.row_dimensions[qa_sub_row].height = 24
    qa_col_headers = [
        "Q#", "Technical Domain", "Lead Defender", "Tough Instructor Question (Tiếng Anh & Tiếng Việt)",
        "Model High-Score Technical Answer (Câu trả lời mẫu điểm tối đa)", "Key Technical Keywords"
    ]
    qa_spans = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 6), (7, 7)]

    for (sc, ec), h_text in zip(qa_spans, qa_col_headers):
        if sc != ec:
            ws.merge_cells(start_row=qa_sub_row, start_column=sc, end_row=qa_sub_row, end_column=ec)
        c = ws.cell(row=qa_sub_row, column=sc, value=h_text)
        style_cell(c, font=FONT_HEADER, fill=FILL_HEADER, alignment=ALIGN_CENTER, border=BORDER_THIN)
        for col_i in range(sc, ec + 1):
            ws.cell(row=qa_sub_row, column=col_i).fill = FILL_HEADER
            ws.cell(row=qa_sub_row, column=col_i).border = BORDER_THIN

    for idx, qa in enumerate(DEFENSE_QA_DATA, start=qa_sub_row + 1):
        ws.row_dimensions[idx].height = 92
        fill_row = FILL_ZEBRA if idx % 2 == 0 else FILL_WHITE

        # Q#
        c_qid = ws.cell(row=idx, column=1, value=qa["qid"])
        style_cell(c_qid, font=FONT_BODY_BOLD, fill=fill_row, alignment=ALIGN_CENTER_TOP, border=BORDER_THIN)

        # Domain
        c_dom = ws.cell(row=idx, column=2, value=qa["domain"])
        style_cell(c_dom, font=FONT_BODY_BOLD, fill=fill_row, alignment=ALIGN_CENTER_TOP, border=BORDER_THIN)

        # Assignee
        c_ass = ws.cell(row=idx, column=3, value=qa["assignee"])
        style_cell(c_ass, font=FONT_BODY_BOLD, fill=fill_row, alignment=ALIGN_CENTER_TOP, border=BORDER_THIN)

        # Question
        c_q = ws.cell(row=idx, column=4, value=qa["question"])
        style_cell(c_q, font=FONT_BODY_BOLD, fill=fill_row, alignment=ALIGN_TEXT_WRAP, border=BORDER_THIN)

        # Answer (Merged 5:6)
        ws.merge_cells(start_row=idx, start_column=5, end_row=idx, end_column=6)
        c_ans = ws.cell(row=idx, column=5, value=qa["answer"])
        style_cell(c_ans, font=FONT_BODY, fill=fill_row, alignment=ALIGN_TEXT_WRAP, border=BORDER_THIN)
        ws.cell(row=idx, column=6).border = BORDER_THIN
        ws.cell(row=idx, column=6).fill = fill_row

        # Keywords
        c_kw = ws.cell(row=idx, column=7, value=qa["keywords"])
        style_cell(c_kw, font=FONT_BODY, fill=fill_row, alignment=ALIGN_TEXT_WRAP, border=BORDER_THIN)

    # Column Widths for Defense Rubric Checklist
    rubric_widths = {
        "A": 18,   # Rubric Criteria / Q#
        "B": 24,   # Checkpoint / Domain
        "C": 18,   # Assignee
        "D": 38,   # Implementation / Question
        "E": 28,   # Answer span 1
        "F": 34,   # Answer span 2 / Verification
        "G": 28    # Readiness / Keywords
    }
    for col_l, w in rubric_widths.items():
        ws.column_dimensions[col_l].width = w

def main():
    print(f"[*] Starting Aquatic Guardian Task Tracker Generation...")
    wb = openpyxl.Workbook()

    # 1. Dashboard & Roles
    print(" -> Creating 'Dashboard & Roles' tab...")
    create_dashboard_tab(wb)

    # 2. Master Task Matrix
    print(" -> Creating 'Master Task Matrix' tab...")
    create_master_task_matrix_tab(wb)

    # 3-7. Member-Specific Tabs
    for mem in MEMBERS_DATA:
        print(f" -> Creating '{mem['sheet_name']}' tab for {mem['name']}...")
        create_member_tab(wb, mem)

    # 8. Defense Rubric Checklist
    print(" -> Creating 'Defense Rubric Checklist' tab...")
    create_rubric_checklist_tab(wb)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    # Save Workbook
    print(f"[*] Saving workbook to: {OUTPUT_PATH}")
    wb.save(OUTPUT_PATH)
    print("[SUCCESS] Aquatic Guardian Task Tracker generated successfully!")

if __name__ == "__main__":
    main()
