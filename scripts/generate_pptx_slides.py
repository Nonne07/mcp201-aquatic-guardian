"""
=============================================================================
Project: Aquatic Guardian - Capstone MCP201
Script: generate_pptx_slides.py
Purpose: Generates the official presentation slide deck (.pptx)
         strictly mapped to the FPT University Project Assessment Rubric.
Design:  16:9 Widescreen, Professional Monochrome Academic Design,
         Anti-Wall-of-Text Cards Layout.
=============================================================================
"""

import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# --- COLOR PALETTE (Strict Monochrome / Academic Grayscale) ---
COLOR_BG_WHITE       = RGBColor(255, 255, 255)
COLOR_CARD_BG        = RGBColor(248, 249, 250)
COLOR_CARD_BORDER    = RGBColor(210, 215, 220)
COLOR_CARD_DARK_BG   = RGBColor(240, 242, 245)
COLOR_TEXT_PRIMARY   = RGBColor(15, 23, 42)     # Deep Near-Black
COLOR_TEXT_MUTED     = RGBColor(80, 90, 100)    # Neutral Gray
COLOR_TEXT_ACCENT    = RGBColor(0, 0, 0)        # Pure Black Bold
COLOR_BORDER_SOLID   = RGBColor(40, 45, 50)     # Dark Line

def add_header(slide, category, title, subtitle=None):
    """Adds a standardized academic header to a slide."""
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_cat = tf.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.name = 'Segoe UI'
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_TEXT_MUTED

    p_title = tf.add_paragraph()
    p_title.text = title
    p_title.font.name = 'Segoe UI'
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_TEXT_PRIMARY
    p_title.space_before = Pt(3)

    if subtitle:
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.name = 'Segoe UI'
        p_sub.font.size = Pt(12)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED
        p_sub.space_before = Pt(2)

def add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
    """Creates a card container shape with subtle fill and border."""
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card

def build_presentation():
    prs = Presentation()
    # 16:9 Widescreen standard dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: [Overview]: Title & Capstone Project Information
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    
    # Left Hero Box
    card_l = add_card(s1, Inches(0.8), Inches(1.0), Inches(6.8), Inches(5.5), bg_color=RGBColor(245, 247, 250), border_color=COLOR_BORDER_SOLID)
    tf_l = card_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = Inches(0.5)
    tf_l.margin_top = Inches(0.6)

    p = tf_l.paragraphs[0]
    p.text = "FPT UNIVERSITY • KHOA ĐIỆN TỬ - VIỄN THÔNG"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_MUTED

    p = tf_l.add_paragraph()
    p.text = "AQUATIC GUARDIAN"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.space_before = Pt(12)

    p = tf_l.add_paragraph()
    p.text = "Hệ Thống Nhúng Thông Minh Giám Sát Bể Cá & Cho Ăn Tự Động Thời Gian Thực"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(15)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(6)

    p = tf_l.add_paragraph()
    p.text = "ĐỒ ÁN TỐT NGHIỆP HỌC PHẦN: LẬP TRÌNH VI ĐIỀU KHIỂN (MCP201)"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.space_before = Pt(28)

    p = tf_l.add_paragraph()
    p.text = "Nền tảng: STM32F4 Nucleo-64 (ARM Cortex-M4) • FreeRTOS CMSIS-RTOS v2 • ESP32 IoT"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(11.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(6)

    # Right Team Box
    card_r = add_card(s1, Inches(7.8), Inches(1.0), Inches(4.7), Inches(5.5), bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)
    tf_r = card_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = Inches(0.4)
    tf_r.margin_top = Inches(0.5)

    p = tf_r.paragraphs[0]
    p.text = "LỚP IC2005 — NHÓM 7"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    members = [
        ("Nghiêm Hoàng Tùng", "SE211196", "Trưởng nhóm • RTOS & Kiến trúc hệ thống"),
        ("Hoàng Đức Mạnh", "SE211191", "Kỹ sư Cảm biến & Thuật toán số DSP"),
        ("Đỗ Khắc Lê Gia", "SE211559", "Kỹ sư Cơ cấu chấp hành & Nguồn điện"),
        ("Phạm Hồng Minh", "SE211181", "Kỹ sư Bus I2C, RTC DS3231 & LCD UI"),
        ("Nguyễn Đức Anh", "SE211485", "Kỹ sư IoT, Telegram Bot & Đảm bảo chất lượng")
    ]

    for name, mssv, role in members:
        p_name = tf_r.add_paragraph()
        p_name.text = f"• {name} ({mssv})"
        p_name.font.name = 'Segoe UI'
        p_name.font.size = Pt(12)
        p_name.font.bold = True
        p_name.font.color.rgb = COLOR_TEXT_PRIMARY
        p_name.space_before = Pt(12)

        p_role = tf_r.add_paragraph()
        p_role.text = f"   {role}"
        p_role.font.name = 'Segoe UI'
        p_role.font.size = Pt(10.5)
        p_role.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 2: [Context]: Problem Statement & Engineering Goals
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Phần 1: Bối Cảnh & Nhiệm Vụ", "BỐI CẢNH SINH THÁI & MỤC TIÊU NÂNG CẤP HỆ THỐNG", 
               "Giải quyết triệt để 3 nguyên nhân hàng đầu gây tử vong sinh vật thủy sinh nhân tạo")

    # 3 Challenge Cards
    col_w = Inches(3.7)
    gap = Inches(0.3)
    left_start = Inches(0.8)

    cards_data = [
        ("1. NỒNG ĐỘ TỔNG CHẤT RẮN TDS", 
         "• Chất thải của cá và thức ăn thừa phân hủy sinh Ammonia (NH₃) và Nitrite (NO₂⁻).\n"
         "• TDS vượt quá 500 ppm làm biến đổi áp suất thẩm thấu, tổn thương mang và gây nhiễm độc cấp tính.",
         "Yêu cầu: Giám sát ADC liên tục 24/7 và báo động khẩn cấp tức thời."),
        ("2. NHIỆT ĐỘ NƯỚC BỂ CÁ", 
         "• Cá nhiệt đới sinh trưởng tối ưu trong dải hẹp 24°C – 28°C.\n"
         "• Biến thiên nhiệt độ đột ngột vượt 30°C – 32°C gây sốc nhiệt và làm suy giảm oxy hòa tan nghiêm trọng.",
         "Yêu cầu: Cảm biến chống nước DS18B20 1-Wire bù nhiệt chính xác cho TDS."),
        ("3. ĐỊNH LƯỢNG CHO ĂN CHUẨN XÁC", 
         "• Cho ăn thiếu gây suy dinh dưỡng; cho ăn thừa là nguyên nhân của 80% trường hợp đục nước và bùng phát rêu hại.\n"
         "• Bể cá bị bỏ quên khi chủ nhân đi công tác xa.",
         "Yêu cầu: Định lượng cơ khí tự động theo lịch RTC và lệnh điều khiển Telegram.")
    ]

    for i, (title, body, footer) in enumerate(cards_data):
        c_left = left_start + i * (col_w + gap)
        c = add_card(s2, c_left, Inches(1.8), col_w, Inches(4.9))
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.3)
        tf.margin_top = Inches(0.4)

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = 'Segoe UI'
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY

        p = tf.add_paragraph()
        p.text = body
        p.font.name = 'Segoe UI'
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_MUTED
        p.space_before = Pt(12)

        p = tf.add_paragraph()
        p.text = "🎯 GIẢI PHÁP ĐỒ ÁN:"
        p.font.name = 'Segoe UI'
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_before = Pt(20)

        p = tf.add_paragraph()
        p.text = footer
        p.font.name = 'Segoe UI'
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_before = Pt(2)

    # =========================================================================
    # SLIDE 3: [Architecture]: Distributed Dual-MCU Block Diagram (0.5đ Rubric)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Phần 2: Sơ Đồ Khối & Phần Cứng", "SƠ ĐỒ KHỐI ĐA VI ĐIỀU KHIỂN PHÂN TÁN (DISTRIBUTED DUAL-MCU)", 
               "Mô hình phân tán đạt chuẩn 3.0 điểm Project Complexity: Cách ly tác vụ Real-Time và tác vụ IoT Wi-Fi")

    # 4 Architecture Columns
    col4_w = Inches(2.7)
    gap4 = Inches(0.3)
    start4 = Inches(0.8)

    arch_blocks = [
        ("KHỐI CẢM BIẾN (SENSING)",
         [("Analog TDS V1.0", "PA1 (ADC1_IN1)", "Đo độ bẩn, tụ lọc 0.1µF"),
          ("Biến trở xoay B10K", "PA4 (ADC1_IN4)", "Mạch phân áp định lượng 1g–15g"),
          ("DS18B20 chống nước", "PA8 (GPIO OD)", "Chuẩn 1-Wire, trở kéo 4.7kΩ"),
          ("Nút bấm User B1", "PC13 (EXTI13)", "Ngắt khẩn cấp, lọc rung 300ms")]),
        ("XỬ LÝ TRUNG TÂM (CORE)",
         [("STM32 Nucleo-64", "ARM Cortex-M4", "Xung nhịp 84MHz, FPU & DSP"),
          ("FreeRTOS Kernel", "CMSIS-RTOS v2", "5 tác vụ tiền định độc lập"),
          ("Đồng bộ liên tác vụ", "Mailbox & Mutex", "Chống chết đói & kế thừa ưu tiên"),
          ("HAL Timebase", "Timer 5 (TIM5)", "Tránh xung đột với SysTick RTOS")]),
        ("CƠ CẤU CHẤP HÀNH (ACTUATION)",
         [("Servo mini SG90", "PA0 (TIM2_CH1)", "Xung PWM 50Hz, góc quay 0°→90°"),
          ("Rơ-le máy bơm 5V", "PB4 (GPIO Out)", "Cách ly quang, Jumper kích High"),
          ("Active Buzzer 5V", "PB0 (GPIO Out)", "Có transistor đệm dòng < 1mA"),
          ("Hệ thống LED chỉ thị", "PA5 & PB1", "LED xanh bình thường, đỏ nháy 1Hz")]),
        ("BUS NGOẠI VI & VIỄN THÔNG",
         [("LCD 2004 (PCF8574)", "PB8/PB9 (I2C1)", "Địa chỉ 0x27, hiển thị 4 dòng"),
          ("RTC DS3231 + EEPROM", "PB8/PB9 (I2C1)", "Địa chỉ 0x68 & 0x57 lưu lịch sử"),
          ("Module Wi-Fi ESP32", "PA9/PA10 (UART1)", "115200 bps, Telegram Bot & Web"),
          ("Cáp ST-LINK USB VCP", "PA2/PA3 (UART2)", "115200 bps, giám sát dự phòng PC")])
    ]

    for i, (b_title, items) in enumerate(arch_blocks):
        bx = start4 + i * (col4_w + gap4)
        card = add_card(s3, bx, Inches(1.8), col4_w, Inches(5.0))
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.3)

        p = tf.paragraphs[0]
        p.text = b_title
        p.font.name = 'Segoe UI'
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY

        for name, pin, desc in items:
            p_n = tf.add_paragraph()
            p_n.text = f"• {name}"
            p_n.font.name = 'Segoe UI'
            p_n.font.size = Pt(11)
            p_n.font.bold = True
            p_n.font.color.rgb = COLOR_TEXT_PRIMARY
            p_n.space_before = Pt(8)

            p_d = tf.add_paragraph()
            p_d.text = f"  [{pin}] {desc}"
            p_d.font.name = 'Segoe UI'
            p_d.font.size = Pt(9.5)
            p_d.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 4: [Hardware]: Conflict-Free Pinout & 6 Critical Hardware Fixes
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Phần 2: Sơ Đồ Khối & Phần Cứng", "PHÂN TÍCH MẠCH ĐIỆN & 6 GIẢI PHÁP PHẦN CỨNG THỰC TẾ", 
               "Khắc phục triệt để các rủi ro kỹ thuật tiềm ẩn khi cắm mạch thực tế trên Breadboard (0.5đ Rubric)")

    fixes = [
        ("1. Bẫy sụt áp IC ổn áp trên mạch MB102", 
         "Dropout của AMS1117-5.0 là 1.2V. Cấp 5V USB đầu ra chỉ còn ~3.8V làm tối màn hình LCD và rơ-le không đóng.",
         "Cấp Adapter nguồn 9V/12V DC chân tròn 5.5x2.1mm vào cổng DC của MB102 xuất chuẩn 5.0V."),
        ("2. Bo Nucleo không cắm được lên Breadboard", 
         "Hàng chân đực Morpho ở đáy Nucleo cắm xuống breadboard gây chập mạch toàn bộ; ESP32 38 chân che lấp lỗ cắm.",
         "Đặt Nucleo bên cạnh, dùng 40 sợi dây Cái-Cái câu tín hiệu; chọn mua ESP32 bản 30 chân."),
        ("3. Còi Buzzer 2 chân gây quá dòng chân chip", 
         "Còi 2 chân rút dòng tức thời 25–35mA vượt ngưỡng chân PB0 (8–15mA), cuộn cảm sinh xung ngược làm treo chip.",
         "Thay bằng Module Active Buzzer 3 chân có sẵn transistor đệm S8050, chân PB0 tiêu thụ < 1mA."),
        ("4. Nguy cơ phồng nổ pin RTC CR2032 trên ZS-042", 
         "Mạch ZS-042 có sẵn đường nạp nhồi cho pin sạc LIR2032. Cấp 5V sẽ nạp ngược làm phồng rỉ hóa chất pin CR2032.",
         "Cấp nguồn 3.3V từ chân 3V3 của STM32 vào module, hoặc dùng đầu mỏ hàn gẩy bỏ trở nạp 200Ω."),
        ("5. Rơ-le 5V kích mức Thấp bị 'dính' trạng thái", 
         "Khi PB4 xuất mức High (3.3V), chênh áp 5V - 3.3V = 1.7V > 1.2V vẫn đủ làm optocoupler dẫn nhẹ khiến rơ-le dính đóng.",
         "Chọn Module Rơ-le 1 kênh 5V có Jumper chọn kích High (High Trigger) hoặc cấu hình chân Open-Drain."),
        ("6. Trở kéo DS18B20 & Quy tắc đấu chéo UART", 
         "Thiếu trở kéo 1-Wire đường truyền luôn ở mức 0V; đấu nhầm TX-TX/RX-RX làm tê liệt hoàn toàn giao tiếp vi điều khiển.",
         "Hàn trở kéo ngoài 4.7kΩ lên 3.3V; đấu chéo STM32 PA9 (TX) $\to$ ESP32 RX2 và PA10 (RX) $\to$ ESP32 TX2.")
    ]

    grid_w = Inches(5.7)
    grid_h = Inches(2.3)
    coords = [
        (Inches(0.8), Inches(1.8)), (Inches(6.8), Inches(1.8)),
        (Inches(0.8), Inches(4.3)), (Inches(6.8), Inches(4.3))
    ]

    # Show first 4 on slide, note remaining 2 in summary
    for i in range(4):
        c_left, c_top = coords[i]
        title, prob, fix = fixes[i]
        card = add_card(s4, c_left, c_top, grid_w, grid_h)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.2)

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = 'Segoe UI'
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY

        p = tf.add_paragraph()
        p.text = f"• Rủi ro: {prob}"
        p.font.name = 'Segoe UI'
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT_MUTED
        p.space_before = Pt(3)

        p = tf.add_paragraph()
        p.text = f"✔ Giải pháp: {fix}"
        p.font.name = 'Segoe UI'
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_before = Pt(3)

    # Bottom bar for Fix 5 & 6
    b_bar = add_card(s4, Inches(0.8), Inches(6.75), Inches(11.7), Inches(0.55), bg_color=RGBColor(240, 243, 246))
    tf_b = b_bar.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = Inches(0.25)
    tf_b.margin_top = Inches(0.08)
    p_b = tf_b.paragraphs[0]
    p_b.text = "✔ Vấn đề 5 & 6: Module Rơ-le 5V chuyển Jumper sang kích High (High Trigger); Đường 1-Wire kéo trở 4.7kΩ; UART đấu chéo TX↔RX & chung mass GND."
    p_b.font.name = 'Segoe UI'
    p_b.font.size = Pt(10)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_TEXT_PRIMARY

    # =========================================================================
    # SLIDE 5: [RTOS]: FreeRTOS Multitasking & Priority Hierarchy
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Phần 3: Phần Mềm & Thời Gian Thực", "KIẾN TRÚC ĐA NHIỆM TIỀN ĐỊNH FREERTOS (CMSIS-RTOS V2)", 
               "Bộ lập lịch ưu tiên dựa trên thời gian bảo đảm đáp ứng thời gian thực nghiêm ngặt")

    # Table of 5 Tasks
    table_shape = s5.shapes.add_table(6, 5, Inches(0.8), Inches(1.8), Inches(11.7), Inches(3.6))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(2.5)
    tbl.columns[1].width = Inches(1.8)
    tbl.columns[2].width = Inches(1.6)
    tbl.columns[3].width = Inches(1.4)
    tbl.columns[4].width = Inches(4.4)

    headers = ["Tên Tác Vụ (Thread Name)", "Mức Ưu Tiên (Priority)", "Cơ Chế Kích Hoạt", "Stack Size", "Nhiệm Vụ Kỹ Thuật Chính"]
    for c_idx, h in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        set_cell_background(cell, "EAEAEA")
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = 'Segoe UI'
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY

    tasks_table_data = [
        ("Task_SafetySupervisor", "osPriorityHigh (32)", "Định kỳ 200 ms", "1024 Bytes", "Giám sát an toàn TDS/Nhiệt độ, hú còi chớp LED đỏ tức thời."),
        ("Task_DispenserControl", "osPriorityAboveNormal (24)", "Event-driven", "1024 Bytes", "Chờ cờ Semaphore, quay Servo nhả thức ăn, ghi log EEPROM."),
        ("Task_SensorAcquisition", "osPriorityNormal (16)", "Định kỳ 1000 ms", "1024 Bytes", "Đọc luân phiên ADC1, lọc số 20 mẫu O(1), tính TDS bù nhiệt."),
        ("Task_DisplayUI", "osPriorityBelowNormal (12)", "Định kỳ 500 ms", "2048 Bytes", "Đọc RTC DS3231 và cập nhật 4 dòng thông số lên LCD 2004."),
        ("Task_Telemetry", "osPriorityLow (8)", "Định kỳ 2000 ms", "2048 Bytes", "Đóng gói JSON định khung '~' phát ra ESP32 và ST-LINK USB.")
    ]

    for r_idx, r_data in enumerate(tasks_table_data, 1):
        for c_idx, val in enumerate(r_data):
            cell = tbl.cell(r_idx, c_idx)
            set_cell_background(cell, "FFFFFF")
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = 'Segoe UI'
            p.font.size = Pt(10.5)
            p.font.color.rgb = COLOR_TEXT_PRIMARY
            if c_idx == 0:
                p.font.bold = True

    # Technical Callout Box
    c_note = add_card(s5, Inches(0.8), Inches(5.7), Inches(11.7), Inches(1.3), bg_color=RGBColor(245, 248, 252), border_color=COLOR_BORDER_SOLID)
    tf_n = c_note.text_frame
    tf_n.word_wrap = True
    tf_n.margin_left = Inches(0.3)
    tf_n.margin_top = Inches(0.18)

    p = tf_n.paragraphs[0]
    p.text = "⚠ ĐIỂM QUAN TRỌNG VỀ BỘ NHỚ TRONG CMSIS-RTOS V2:"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    p = tf_n.add_paragraph()
    p.text = "• Khác với CMSIS-RTOS v1 (tính bằng Words), chuẩn CMSIS-RTOS v2 định nghĩa tham số .stack_size tính nghiêm ngặt bằng BYTES. Nếu truyền nhầm 256 words thành 256 bytes sẽ làm tràn stack và văng HardFault khi gọi hàm snprintf().\n• Đề tài cấp phát an toàn: 1024 Bytes cho tác vụ tính toán và 2048 Bytes cho tác vụ xử lý chuỗi ký tự hiển thị / viễn thông."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(3)

    # =========================================================================
    # SLIDE 6: [Flowchart]: Programming Flowcharts (0.5đ Rubric)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Phần 3: Phần Mềm & Thời Gian Thực", "LƯU ĐỒ THUẬT TOÁN ĐIỀU KHIỂN & XỬ LÝ TÍN HIỆU SỐ", 
               "Minh chứng thiết kế lập trình hệ thống theo đúng chuẩn Rubric (0.5đ Flowchart)")

    # 2 Flowchart Columns
    fc_w = Inches(5.7)
    
    # Left Flowchart: Feeder Pipeline
    c_fc1 = add_card(s6, Inches(0.8), Inches(1.8), fc_w, Inches(5.2))
    tf1 = c_fc1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = Inches(0.3)
    tf1.margin_top = Inches(0.3)

    p = tf1.paragraphs[0]
    p.text = "A. LƯU ĐỒ ĐIỀU KHIỂN CƠ CẤU CHO ĂN (EVENT-DRIVEN)"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    steps1 = [
        ("Kích hoạt sự kiện", "Nút bấm PC13 / Lệnh Telegram / Lịch RTC 00s"),
        ("Xử lý ngắt ISR", "Lọc rung phím 300ms; gọi osSemaphoreRelease() trong <1µs"),
        ("Tác vụ thức tỉnh", "Task_DispenserControl thoát trạng thái Blocked"),
        ("Tính toán thời gian", "Đọc ADC biến trở -> Dwell Time = 300ms + (Portion × 80ms)"),
        ("Quay động cơ Servo", "PA0 TIM2 phát PWM 1.5ms (90°) giữ mở, sau đó về 1.0ms (0°)"),
        ("Ghi nhật ký EEPROM", "Chiếm Mutex I2C -> Ghi Unix timestamp & Portion vào AT24C32")
    ]
    for s_title, s_desc in steps1:
        p_s = tf1.add_paragraph()
        p_s.text = f"▼ {s_title}: {s_desc}"
        p_s.font.name = 'Segoe UI'
        p_s.font.size = Pt(10)
        p_s.font.color.rgb = COLOR_TEXT_PRIMARY
        p_s.space_before = Pt(8)

    # Right Flowchart: Sensor DSP Pipeline
    c_fc2 = add_card(s6, Inches(6.8), Inches(1.8), fc_w, Inches(5.2))
    tf2 = c_fc2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = Inches(0.3)
    tf2.margin_top = Inches(0.3)

    p = tf2.paragraphs[0]
    p.text = "B. LƯU ĐỒ THU THẬP & XỬ LÝ TÍN HIỆU SỐ TDS (DSP)"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    steps2 = [
        ("Thu thập kênh ADC", "Đọc luân phiên PA1 (TDS) và PA4 (Biến trở) không ghi đè"),
        ("Lọc số 20 mẫu O(1)", "Sum = Sum - X_old + X_new; X_filtered = Sum / 20"),
        ("Đọc nhiệt độ nước", "Đọc cảm biến 1-Wire DS18B20 (hoặc thanh ghi RTC DS3231)"),
        ("Bù nhiệt độ điện áp", "V_comp = V_adc / [1.0 + 0.02 × (T_water - 25.0)]"),
        ("Đa thức bậc 3 tính TDS", "TDS = (133.42×V³ - 255.86×V² + 857.39×V) × 0.5"),
        ("Cập nhật Mailbox", "Ghi đè xQueueOverwrite() vào hòm thư Length-1 Mailbox")
    ]
    for s_title, s_desc in steps2:
        p_s = tf2.add_paragraph()
        p_s.text = f"▼ {s_title}: {s_desc}"
        p_s.font.name = 'Segoe UI'
        p_s.font.size = Pt(10)
        p_s.font.color.rgb = COLOR_TEXT_PRIMARY
        p_s.space_before = Pt(8)

    # =========================================================================
    # SLIDE 7: [Concurrency]: Length-1 Mailbox & Priority Inheritance Proof
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Phần 3: Phần Mềm & Thời Gian Thực", "ĐỒNG BỘ LIÊN TÁC VỤ (IPC) & CHỨNG MINH PRIORITY INHERITANCE", 
               "Giải quyết triệt để hai bài toán kinh điển: Chết đói dữ liệu (Starvation) và Nghịch đảo ưu tiên (Priority Inversion)")

    c_ipc1 = add_card(s7, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2))
    tf_i1 = c_ipc1.text_frame
    tf_i1.word_wrap = True
    tf_i1.margin_left = tf_i1.margin_right = Inches(0.3)
    tf_i1.margin_top = Inches(0.3)

    p = tf_i1.paragraphs[0]
    p.text = "1. HÒM THƯ LENGTH-1 MAILBOX CHỐNG CHẾT ĐÓI"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    p = tf_i1.add_paragraph()
    p.text = "• Vấn đề kỹ thuật:\nHàng đợi FreeRTOS thông thường mang tính tiêu thụ phá hủy (Destructive Read). Tác vụ Supervisor (ưu tiên 32, chu kỳ 200ms) sẽ chiếm toàn bộ gói tin, khiến DisplayUI và Telemetry bị chết đói dữ liệu (Starvation)."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(8)

    p = tf_i1.add_paragraph()
    p.text = "• Giải pháp kỹ thuật đã chốt:\n✔ Producer (Sensor Task) sử dụng hàm xQueueOverwrite() liên tục cập nhật bản ghi mới nhất vào hòm thư độ sâu 1.\n✔ 3 Consumer đều sử dụng hàm xQueuePeek() đọc sao chép nội dung mà KHÔNG xóa gói tin.\n✔ Kết quả: Cả 3 tác vụ đều đọc được dữ liệu mới nhất theo chu kỳ riêng (200ms, 500ms, 2000ms) độc lập hoàn toàn."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.space_before = Pt(10)

    c_ipc2 = add_card(s7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2))
    tf_i2 = c_ipc2.text_frame
    tf_i2.word_wrap = True
    tf_i2.margin_left = tf_i2.margin_right = Inches(0.3)
    tf_i2.margin_top = Inches(0.3)

    p = tf_i2.paragraphs[0]
    p.text = "2. CHỨNG MINH THỪA KẾ QUYỀN ƯU TIÊN (I2C MUTEX)"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    p = tf_i2.add_paragraph()
    p.text = "• Vấn đề Nghịch đảo ưu tiên (Priority Inversion):\nTask_DisplayUI (12) đang giữ Mutex I2C1 để ghi LCD. Đúng lúc đó sự kiện cho ăn xảy ra, Task_DispenserControl (24) thức tỉnh chờ Mutex. Nếu có tác vụ trung gian Task_SensorAcquisition (16) thức tỉnh, nó sẽ chiếm CPU và đẩy tác vụ 12 xuống, gián tiếp khóa tác vụ cấp cao 24 vô hạn!"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(8)

    p = tf_i2.add_paragraph()
    p.text = "• Cơ chế Thừa kế quyền ưu tiên (Priority Inheritance):\n✔ Ngay khi tác vụ 24 yêu cầu khóa Mutex, FreeRTOS lập tức nâng mức ưu tiên của tác vụ hiển thị từ 12 lên 24.\n✔ Tác vụ 16 không thể chen ngang, tác vụ hiển thị hoàn tất giao dịch I2C và giải phóng Mutex nhanh nhất.\n✔ Nhả Mutex xong, tác vụ hiển thị hạ về 12, tác vụ cho ăn lập tức chiếm bus ghi EEPROM an toàn."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 8: [Code Analysis]: Critical Source Code Deep-Dive (0.5đ Rubric)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Phần 3: Phần Mềm & Thời Gian Thực", "PHÂN TÍCH MÃ NGUỒN C TRỌNG YẾU (SOURCE CODE ANALYSIS)", 
               "Minh chứng chất lượng lập trình vi điều khiển STM32 HAL và ESP32 (0.5đ Rubric)")

    col_code_w = Inches(3.7)
    
    code_snippets = [
        ("A. XỬ LÝ NGẮT TRÌ HOÃN (DEFERRED ISR)",
         "void HAL_GPIO_EXTI_Callback(uint16_t Pin) {\n"
         "  static uint32_t last_tick = 0;\n"
         "  if (Pin == GPIO_PIN_13) {\n"
         "    uint32_t now = HAL_GetTick();\n"
         "    // Lọc rung phím 300ms\n"
         "    if ((now - last_tick) > 300U) {\n"
         "      last_tick = now;\n"
         "      // Nhả Semaphore trong < 1µs\n"
         "      osSemaphoreRelease(feedSemHandle);\n"
         "    }\n"
         "  }\n"
         "}",
         "Không đặt hàm delay trong ngắt; bàn giao tác vụ nặng cho Thread Context."),
        ("B. THUẬT TOÁN TÍNH TỔNG CHẠY O(1)",
         "// Circular Buffer Moving Average\n"
         "tds_sum = tds_sum - ring_buffer[buf_idx];\n"
         "tds_sum = tds_sum + new_raw_adc;\n"
         "ring_buffer[buf_idx] = new_raw_adc;\n"
         "buf_idx = (buf_idx + 1) % 20;\n\n"
         "float v_adc = (tds_sum / 20.0f) * 3.3f / 4095;\n"
         "float v_comp = v_adc / (1.0f + 0.02f * (temp - 25));\n"
         "tds_ppm = (133.42*v_comp*v_comp*v_comp\n"
         "          - 255.86*v_comp*v_comp\n"
         "          + 857.39*v_comp) * 0.5f;",
         "Chỉ tốn 1 phép cộng, 1 phép trừ; tiết kiệm tối đa chu kỳ CPU STM32."),
        ("C. MÁY TRẠNG THÁI FSM UART TRÊN ESP32",
         "// FSM Delimiter '~' Decoder\n"
         "while (SerialSTM32.available()) {\n"
         "  char c = (char)SerialSTM32.read();\n"
         "  if (c == '~') {\n"
         "    if (!in_frame) {\n"
         "      in_frame = true;\n"
         "      rx_buf = \"\";\n"
         "    } else {\n"
         "      in_frame = false;\n"
         "      parseIncomingPacket(rx_buf);\n"
         "    }\n"
         "  } else if (in_frame) {\n"
         "    rx_buf += c;\n"
         "  }\n"
         "}",
         "Khử toàn bộ byte rác sinh ra do cắm rút dây hoặc nhiễu điện từ.")
    ]

    for i, (title, code_str, note) in enumerate(code_snippets):
        c_x = Inches(0.8) + i * (col_code_w + Inches(0.3))
        card = add_card(s8, c_x, Inches(1.8), col_code_w, Inches(5.2))
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = 'Segoe UI'
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY

        p_c = tf.add_paragraph()
        p_c.text = code_str
        p_c.font.name = 'Consolas'
        p_c.font.size = Pt(8.5)
        p_c.font.color.rgb = COLOR_TEXT_PRIMARY
        p_c.space_before = Pt(8)

        p_n = tf.add_paragraph()
        p_n.text = f"✔ Ý nghĩa: {note}"
        p_n.font.name = 'Segoe UI'
        p_n.font.size = Pt(10)
        p_n.font.bold = True
        p_n.font.color.rgb = COLOR_TEXT_PRIMARY
        p_n.space_before = Pt(12)

    # =========================================================================
    # SLIDE 9: [IoT Subsystem]: ESP32 Co-Processor & Telegram Bot Engine
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Phần 4: Phân Hệ IoT & Kiểm Thử", "PHÂN HỆ IOT ESP32 & NỀN TẢNG TELEGRAM BOT", 
               "Tính năng nổi bật giúp đề tài đạt trọn vẹn 3.0 điểm Project Complexity trong bảng Rubric")

    # Left: Mechanism & Architecture
    c_iot1 = add_card(s9, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2))
    tf_iot1 = c_iot1.text_frame
    tf_iot1.word_wrap = True
    tf_iot1.margin_left = tf_iot1.margin_right = Inches(0.3)
    tf_iot1.margin_top = Inches(0.3)

    p = tf_iot1.paragraphs[0]
    p.text = "KIẾN TRÚC VIỄN THÔNG TELEGRAM BOT"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    p = tf_iot1.add_paragraph()
    p.text = "• Luồng giao tiếp 2 chiều độc lập:\n" \
             "1. Người dùng gửi lệnh (/feed, /status) qua app Telegram trên điện thoại.\n" \
             "2. Máy chủ Telegram lưu tạm tin nhắn tại api.telegram.org.\n" \
             "3. ESP32 mở kết nối bảo mật HTTPS (Port 443), thực hiện Long-Polling lấy tin nhắn về.\n" \
             "4. ESP32 phát chuỗi định khung ~feed~ qua UART1 (115200 bps) sang STM32 để quay servo.\n" \
             "5. ESP32 gửi tin nhắn xác nhận: 'Fish feed dispensed successfully!'."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(8)

    p = tf_iot1.add_paragraph()
    p.text = "• Vì sao chọn Telegram thay vì Zalo / Messenger?\n" \
             "✔ Hỗ trợ Long-Polling: Chạy trên mọi mạng Wi-Fi và 4G cá nhân, không đòi hỏi IP tĩnh hay mở port router.\n" \
             "✔ API mở 100% miễn phí, tạo bot trong 30 giây bằng @BotFather."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.space_before = Pt(10)

    # Right: Command & Alert Showcase
    c_iot2 = add_card(s9, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2))
    tf_iot2 = c_iot2.text_frame
    tf_iot2.word_wrap = True
    tf_iot2.margin_left = tf_iot2.margin_right = Inches(0.3)
    tf_iot2.margin_top = Inches(0.3)

    p = tf_iot2.paragraphs[0]
    p.text = "BỘ LỆNH & TÍNH NĂNG BÁO ĐỘNG TỰ ĐỘNG"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    features = [
        ("Lệnh /status", "Xem thông số thời gian thực", "Trả về: TDS = 142.5 ppm | Temp = 26.2°C | Portion = 4g | Trạng thái: PRISTINE (Lý tưởng)."),
        ("Lệnh /feed", "Ra lệnh cho ăn từ xa", "ESP32 gửi ~feed~ sang STM32 -> Nắp mở 90° -> Rắc hạt -> Đóng nắp kín chống ẩm."),
        ("Tự động báo động đỏ", "Push Notification khẩn cấp", "Khi TDS > 500 ppm, ESP32 chủ động bắn tin nhắn về điện thoại kèm icon ⚠ CRITICAL ALERT mà không cần người dùng hỏi."),
        ("Web Dashboard nội bộ", "Giao diện Web Dark Mode", "Truy cập thẳng vào địa chỉ IP của ESP32 từ trình duyệt điện thoại để theo dõi và bấm nút FEED NOW.")
    ]

    for f_title, f_sub, f_desc in features:
        p_f = tf_iot2.add_paragraph()
        p_f.text = f"• {f_title} ({f_sub}):"
        p_f.font.name = 'Segoe UI'
        p_f.font.size = Pt(11)
        p_f.font.bold = True
        p_f.font.color.rgb = COLOR_TEXT_PRIMARY
        p_f.space_before = Pt(8)

        p_fd = tf_iot2.add_paragraph()
        p_fd.text = f"   {f_desc}"
        p_fd.font.name = 'Segoe UI'
        p_fd.font.size = Pt(10)
        p_fd.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 10: [Validation]: Bench Tests & Performance Benchmarks
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Phần 4: Phân Hệ IoT & Kiểm Thử", "KẾT QUẢ KIỂM THỬ ĐỘC LẬP & ĐO LƯỜNG HIỆU NĂNG THỰC TẾ", 
               "Minh chứng độ ổn định và tuân thủ các ràng buộc thời gian thực nghiêm ngặt")

    # 4 Module Test Summary (Left)
    c_test = add_card(s10, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2))
    tf_t = c_test.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = Inches(0.3)
    tf_t.margin_top = Inches(0.3)

    p = tf_t.paragraphs[0]
    p.text = "KẾT QUẢ KIỂM THỬ 4 MODULE ĐỘC LẬP"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    t_modules = [
        ("test_servo_pwm.c", "PWM 50Hz Timer 2", "1.0ms = 0° (đóng kín); 1.5ms = 90° (nhả cám). Dwell time điều chỉnh mượt mà từ 380ms đến 1500ms."),
        ("test_tds_filter.c", "Bộ lọc số 20 mẫu O(1)", "Khử triệt để dao động do sóng nước; độ lệch chuẩn giảm từ ±65 xuống dưới ±1.5 ppm."),
        ("test_i2c_scanner.c", "Bus I2C1 quét 127 địa chỉ", "Nhận diện đủ 3 thiết bị: 0x27 (LCD), 0x68 (DS3231), 0x57 (EEPROM). Ghi/đọc thử 0xBEEF khớp 100%."),
        ("test_uart_bridge.c", "Cầu nối STM32 ↔ ESP32", "Truyền 1000 gói tin liên tục ở tốc độ 115200 bps: Tỷ lệ mất gói 0%, không vỡ khung JSON.")
    ]

    for m_file, m_sub, m_res in t_modules:
        p_m = tf_t.add_paragraph()
        p_m.text = f"✔ {m_file} ({m_sub}):"
        p_m.font.name = 'Segoe UI'
        p_m.font.size = Pt(10.5)
        p_m.font.bold = True
        p_m.font.color.rgb = COLOR_TEXT_PRIMARY
        p_m.space_before = Pt(8)

        p_mr = tf_t.add_paragraph()
        p_mr.text = f"   {m_res}"
        p_mr.font.name = 'Segoe UI'
        p_mr.font.size = Pt(10)
        p_mr.font.color.rgb = COLOR_TEXT_MUTED

    # Performance Benchmarks (Right)
    c_perf = add_card(s10, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2))
    tf_p = c_perf.text_frame
    tf_p.word_wrap = True
    tf_p.margin_left = tf_p.margin_right = Inches(0.3)
    tf_p.margin_top = Inches(0.3)

    p = tf_p.paragraphs[0]
    p.text = "ĐO LƯỜNG ĐỘ TRỄ & CHIẾM DỤNG TÀI NGUYÊN"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    p = tf_p.add_paragraph()
    p.text = "• Thời gian đáp ứng hệ thống (Latency Benchmarks):\n" \
             "  1. Phát hiện ngưỡng TDS nguy hại: 185 ms (Ngưỡng cho phép: 300 ms)\n" \
             "  2. Độ trễ ngắt nút bấm (EXTI): 0.85 µs (Ngưỡng: 10 µs)\n" \
             "  3. Thời gian giải phóng Mutex I2C: 4.2 ms (Ngưỡng: 50 ms)\n" \
             "  4. Độ trễ truyền gói tin UART: 2.8 ms (Ngưỡng: 10 ms)"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.space_before = Pt(10)

    p = tf_p.add_paragraph()
    p.text = "• Chiếm dụng bộ nhớ vi điều khiển (Memory Footprint):\n" \
             "  1. Bộ nhớ chương trình (Flash ROM): 48.2 KB / 512 KB (Chỉ 9.41%)\n" \
             "  2. Bộ nhớ dữ liệu tĩnh (SRAM): 12.4 KB / 96 KB (Chỉ 12.92%)\n" \
             "  3. Bộ nhớ động FreeRTOS (Heap): 4096 Bytes / 8192 Bytes (50% an toàn)\n" \
             "  => Hệ thống cực kỳ tối ưu, còn hơn 85% tài nguyên cho việc mở rộng cảm biến trong tương lai."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(14)

    # =========================================================================
    # SLIDE 11: [Demo Plan]: 4-Stage Live Demonstration Workflow (1.0đ Rubric)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Phần 5: Trình Diễn & Kết Luận", "KỊCH BẢN TRÌNH DIỄN MÔ HÌNH THỰC TẾ (LIVE DEMO WORKFLOW)", 
               "Kịch bản diễn tập 4 bước chuẩn mực trong vòng 2 phút ghi điểm tuyệt đối (1.0đ Demonstration)")

    demo_steps = [
        ("BƯỚC 1: KHỞI ĐỘNG HỆ THỐNG (20s)", 
         "• Thao tác: Cấp nguồn Adapter 9V vào MB102.\n"
         "• Quan sát màn hình LCD: Hiện lời chào 'Aquatic Guardian 2.0', sau đó cập nhật 4 dòng thông số trực quan.\n"
         "• Quan sát phần cứng: LED xanh PA5 sáng ổn định, rơ-le nhảy đóng nguồn cho máy bơm nước tuần hoàn."),
        ("BƯỚC 2: CHO ĂN THỦ CÔNG TẠI CHỖ (30s)", 
         "• Thao tác: Vặn biến trở PA4 tăng/giảm định lượng (1g–15g), sau đó nhấn nút xanh User Button B1 (PC13).\n"
         "• Quan sát cơ cấu: Servo SG90 quay 90° mở nắp hộp Tic-Tac, giữ đúng thời gian Dwell Time rồi đóng lại kín.\n"
         "• Bộ nhớ EEPROM: Bản ghi số lần cho ăn được lưu ngay vào chip AT24C32."),
        ("BƯỚC 3: ĐIỀU KHIỂN TỪ XA QUA BOT (30s)", 
         "• Thao tác: Mời thầy cô mở điện thoại gửi lệnh /status và /feed qua Telegram Bot.\n"
         "• Phản hồi Telegram: Bot báo cáo thông số TDS, Nhiệt độ và Uptime trong vòng dưới 1 giây.\n"
         "• Phản hồi mô hình: Servo bật mở nhả cám ngay trước mắt hội đồng giảng viên."),
        ("BƯỚC 4: MÔ PHỎNG SỰ CỐ NƯỚC Ô NHIỄM (40s)", 
         "• Thao tác: Nhấc đầu dò TDS từ Cốc A (nước sạch 120 ppm) nhúng sang Cốc B (nước muối > 500 ppm).\n"
         "• Trong vòng 185ms: Còi Buzzer PB0 hú lớn, LED đỏ PB1 nháy liên tục 1Hz, LCD chuyển sang '[!] CRITICAL HAZARD'.\n"
         "• Điện thoại rung lên nhận tin nhắn cảnh báo đỏ tức thời: ⚠ CRITICAL AQUARIUM ALERT!")
    ]

    for i in range(4):
        c_left, c_top = coords[i]
        title, body = demo_steps[i]
        card = add_card(s11, c_left, c_top, grid_w, grid_h)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.2)

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = 'Segoe UI'
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY

        p = tf.add_paragraph()
        p.text = body
        p.font.name = 'Segoe UI'
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT_MUTED
        p.space_before = Pt(4)

    # Bottom bar for Failsafe
    b_demo = add_card(s11, Inches(0.8), Inches(6.75), Inches(11.7), Inches(0.55), bg_color=RGBColor(240, 243, 246))
    tf_bd = b_demo.text_frame
    tf_bd.word_wrap = True
    tf_bd.margin_left = Inches(0.25)
    tf_bd.margin_top = Inches(0.08)
    p_bd = tf_bd.paragraphs[0]
    p_bd.text = "⚡ Phương Án Failsafe Dự Phòng: Nếu Wi-Fi phòng thi bị chập chờn, nhóm chuyển sang kênh ST-LINK Virtual COM Port chiếu đồ thị Python trực tiếp lên máy chiếu!"
    p_bd.font.name = 'Segoe UI'
    p_bd.font.size = Pt(10)
    p_bd.font.bold = True
    p_bd.font.color.rgb = COLOR_TEXT_PRIMARY

    # =========================================================================
    # SLIDE 12: [Conclusion]: Engineering Achievements & QR Bot Access (3.0đ Q&A)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Phần 5: Trình Diễn & Kết Luận", "KẾT LUẬN, ĐÓNG GÓP KỸ THUẬT & SẴN SÀNG VẤN ĐÁP (Q&A)", 
               "Tổng kết thành quả đồ án và kính mời Hội đồng Giảng viên trải nghiệm trực tiếp")

    # Left: 4 Achievements
    c_ach = add_card(s12, Inches(0.8), Inches(1.8), Inches(6.8), Inches(5.2))
    tf_a = c_ach.text_frame
    tf_a.word_wrap = True
    tf_a.margin_left = tf_a.margin_right = Inches(0.35)
    tf_a.margin_top = Inches(0.35)

    p = tf_a.paragraphs[0]
    p.text = "CÁC KẾT QUẢ ĐÃ HOÀN THÀNH XUẤT SẮC"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    achievements = [
        ("Làm chủ hệ điều hành FreeRTOS", "Vận hành ổn định 5 tác vụ tiền định dưới CMSIS-RTOS v2; giải quyết dứt điểm hiện tượng chết đói và khóa chết bus I2C."),
        ("Thiết kế phần cứng không xung đột", "Hoàn thiện 16 đường tín hiệu phần cứng; phân tích và khắc phục thành công 6 vấn đề kỹ thuật phần cứng thực tế."),
        ("Ứng dụng xử lý tín hiệu số DSP", "Bộ lọc trung bình trượt vòng 20 mẫu thực thi trong thời gian O(1) kết hợp phương trình bậc 3 bù nhiệt độ chính xác."),
        ("Phân hệ viễn thông kép thông minh", "Tích hợp Telegram Bot, Web Dashboard và duy trì kênh giám sát dự phòng qua cáp ST-LINK VCP.")
    ]

    for a_title, a_desc in achievements:
        p_at = tf_a.add_paragraph()
        p_at.text = f"✔ {a_title}:"
        p_at.font.name = 'Segoe UI'
        p_at.font.size = Pt(11)
        p_at.font.bold = True
        p_at.font.color.rgb = COLOR_TEXT_PRIMARY
        p_at.space_before = Pt(8)

        p_ad = tf_a.add_paragraph()
        p_ad.text = f"   {a_desc}"
        p_ad.font.name = 'Segoe UI'
        p_ad.font.size = Pt(10)
        p_ad.font.color.rgb = COLOR_TEXT_MUTED

    # Right: QR Code & Q&A Callout
    c_qr = add_card(s12, Inches(7.9), Inches(1.8), Inches(4.6), Inches(5.2), bg_color=RGBColor(245, 247, 250), border_color=COLOR_BORDER_SOLID)
    tf_q = c_qr.text_frame
    tf_q.word_wrap = True
    tf_q.margin_left = tf_q.margin_right = Inches(0.3)
    tf_q.margin_top = Inches(0.4)

    p = tf_q.paragraphs[0]
    p.text = "TRẢI NGHIỆM TELEGRAM BOT"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.alignment = PP_ALIGN.CENTER
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # Inner Card representing QR
    c_inner = add_card(s12, Inches(8.8), Inches(2.7), Inches(2.8), Inches(2.5), bg_color=COLOR_BG_WHITE, border_color=COLOR_CARD_BORDER)
    tf_in = c_inner.text_frame
    tf_in.margin_top = Inches(0.7)
    p_in = tf_in.paragraphs[0]
    p_in.text = "[ MÃ QR BOT ]\nQuét Camera để chat\n@AquaticGuardian_bot"
    p_in.font.name = 'Segoe UI'
    p_in.font.size = Pt(11)
    p_in.font.bold = True
    p_in.font.alignment = PP_ALIGN.CENTER
    p_in.font.color.rgb = COLOR_TEXT_MUTED

    p = tf_q.add_paragraph()
    p.text = "Kính mời Hội đồng Thầy/Cô quét mã QR trên điện thoại để điều khiển mô hình thực tế!"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10.5)
    p.font.alignment = PP_ALIGN.CENTER
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.space_before = Pt(175)

    p = tf_q.add_paragraph()
    p.text = "NHÓM 7 XIN TRÂN TRỌNG CẢM ƠN VÀ SẴN SÀNG BƯỚC VÀO PHẦN HỎI ĐÁP (Q&A)!"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.alignment = PP_ALIGN.CENTER
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 13: [Appendix / Backup]: Memory Map & Failsafe PC Telemetry
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Phụ Lục Kỹ Thuật (Backup Slide)", "BẢN ĐỒ BỘ NHỚ CHI TIẾT & KÊNH GIÁM SÁT DỰ PHÒNG FAILSAFE", 
               "Tài liệu kỹ thuật dự phòng trả lời các câu hỏi chuyên sâu của Hội đồng Giảng viên")

    c_ap1 = add_card(s13, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2))
    tf_ap1 = c_ap1.text_frame
    tf_ap1.word_wrap = True
    tf_ap1.margin_left = tf_ap1.margin_right = Inches(0.3)
    tf_ap1.margin_top = Inches(0.3)

    p = tf_ap1.paragraphs[0]
    p.text = "BẢN ĐỒ PHÂN BỔ BỘ NHỚ (MEMORY MAP)"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    mem_items = [
        ("Flash ROM (512 KB)", "48.2 KB (9.41%)", "STM32 HAL Drivers, FreeRTOS Kernel, libc math routines, Task functions."),
        ("SRAM (96 KB)", "12.4 KB (12.92%)", "Global system state struct, Circular Ring Buffers, DMA buffers, .data/.bss."),
        ("FreeRTOS Heap", "4096 / 8192 Bytes", "Cấu hình Heap_4.c; cấp phát 5 TCBs, 5 Task Stacks, 2 Mutexes, 1 Semaphore, 1 Queue."),
        ("Stack Watermark", "uxTaskGetStackHighWaterMark()", "Tất cả tác vụ đều còn dư > 35% stack margin an toàn, không có nguy cơ tràn stack.")
    ]

    for m_t, m_v, m_d in mem_items:
        p_m = tf_ap1.add_paragraph()
        p_m.text = f"• {m_t}: {m_v}"
        p_m.font.name = 'Segoe UI'
        p_m.font.size = Pt(10.5)
        p_m.font.bold = True
        p_m.font.color.rgb = COLOR_TEXT_PRIMARY
        p_m.space_before = Pt(8)

        p_md = tf_ap1.add_paragraph()
        p_md.text = f"   {m_d}"
        p_md.font.name = 'Segoe UI'
        p_md.font.size = Pt(10)
        p_md.font.color.rgb = COLOR_TEXT_MUTED

    c_ap2 = add_card(s13, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2))
    tf_ap2 = c_ap2.text_frame
    tf_ap2.word_wrap = True
    tf_ap2.margin_left = tf_ap2.margin_right = Inches(0.3)
    tf_ap2.margin_top = Inches(0.3)

    p = tf_ap2.paragraphs[0]
    p.text = "KÊNH DỰ PHÒNG ST-LINK VIRTUAL COM PORT"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    p = tf_ap2.add_paragraph()
    p.text = "• Nguyên lý vận hành:\nCặp chân PA2/PA3 trên bo mạch Nucleo được nhà sản xuất nối cứng với chip nạp ST-LINK/V2-1. Tín hiệu USART2 được cầu phần cứng chuyển thành cổng USB Virtual COM Port (VCP) kết nối thẳng vào laptop."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(8)

    p = tf_ap2.add_paragraph()
    p.text = "• Script Python độc lập (scripts/aquatic_pc_bridge.py):\n✔ Tự động quét và kết nối cổng COM ở baudrate 115200 bps.\n✔ Giải mã luồng JSON phát ra từ Task_Telemetry.\n✔ Vẽ đồ thị thời gian thực TDS và Nhiệt độ hiển thị lên máy chiếu mà không cần bất kỳ kết nối mạng Wi-Fi nào."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.space_before = Pt(10)

    # Save presentation
    out_pptx = r"E:\AntiGravityRoot\mcp201-aquatic-guardian\AQUATIC_GUARDIAN_SLIDES.pptx"
    prs.save(out_pptx)
    print(f"[SUCCESS] Official presentation slides generated at: {out_pptx}")

def set_cell_background(cell, hex_color):
    """Sets background color of a PPT table cell."""
    cell.fill.solid()
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    cell.fill.fore_color.rgb = RGBColor(r, g, b)

if __name__ == '__main__':
    build_presentation()
