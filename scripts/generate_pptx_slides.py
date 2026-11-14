"""
=============================================================================
Project: Aquatic Guardian - Capstone MCP201 (Class IC2005 - Group 7)
Script:  generate_pptx_slides.py
Purpose: Generates the official presentation slide deck (.pptx)
         with 100% proper, accented Vietnamese typography (Tiếng Việt có dấu).
Design:  16:9 Widescreen, Anti-Wall-of-Text, Clean Card Hierarchy,
         Generous Whitespace, Strict 10-15 Words/Bullet, Executive Monochrome.
=============================================================================
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# --- COLOR PALETTE (Clean Academic Monochrome / Slate) ---
COLOR_BG_WHITE       = RGBColor(255, 255, 255)
COLOR_CARD_BG        = RGBColor(248, 250, 252)    # Slate 50
COLOR_CARD_ALT       = RGBColor(241, 245, 249)    # Slate 100
COLOR_CARD_DARK      = RGBColor(15, 23, 42)       # Slate 900 (Dark Accent)
COLOR_BORDER_LIGHT   = RGBColor(226, 232, 240)    # Slate 200
COLOR_BORDER_MEDIUM  = RGBColor(203, 213, 225)    # Slate 300
COLOR_BORDER_DARK    = RGBColor(15, 23, 42)       # Slate 900
COLOR_TEXT_PRIMARY   = RGBColor(15, 23, 42)       # Deep Slate 900
COLOR_TEXT_MUTED     = RGBColor(71, 85, 105)      # Slate 600
COLOR_TEXT_WHITE     = RGBColor(255, 255, 255)
COLOR_CODE_BG        = RGBColor(15, 23, 42)       # Dark Terminal Box
COLOR_CODE_TEXT      = RGBColor(241, 245, 249)

def add_header(slide, category, title, takeaway=None):
    """Adds a standardized clean header with a prominent takeaway line."""
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_cat = tf.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.name = 'Segoe UI'
    p_cat.font.size = Pt(9.5)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_TEXT_MUTED

    p_title = tf.add_paragraph()
    p_title.text = title
    p_title.font.name = 'Segoe UI'
    p_title.font.size = Pt(18)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_TEXT_PRIMARY
    p_title.space_before = Pt(2)

    if takeaway:
        p_sub = tf.add_paragraph()
        p_sub.text = takeaway
        p_sub.font.name = 'Segoe UI'
        p_sub.font.size = Pt(10.5)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED
        p_sub.space_before = Pt(2)

def add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_LIGHT, border_width=Pt(1)):
    """Creates a card container shape with subtle fill and border."""
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = border_width
    else:
        card.line.fill.background()
    return card

def add_badge(slide, left, top, width, height, text, bg_color=COLOR_CARD_DARK, text_color=COLOR_TEXT_WHITE, font_size=9.0):
    """Creates a clean solid badge for section headers."""
    badge = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    badge.fill.solid()
    badge.fill.fore_color.rgb = bg_color
    badge.line.fill.background()
    tf = badge.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = text
    p.font.name = 'Segoe UI'
    p.font.size = Pt(font_size)
    p.font.bold = True
    p.font.color.rgb = text_color
    p.alignment = PP_ALIGN.CENTER
    return badge

def set_cell_background(cell, hex_color):
    """Sets background color of a PPT table cell."""
    cell.fill.solid()
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    cell.fill.fore_color.rgb = RGBColor(r, g, b)

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: Title Slide (Trang Tiêu Đề Có Dấu)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    
    # Left Hero Box
    c_l = add_card(s1, Inches(0.8), Inches(1.2), Inches(6.8), Inches(5.0), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_DARK, border_width=Pt(1.5))
    tf_l = c_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = Inches(0.5)
    tf_l.margin_top = Inches(0.5)

    p = tf_l.paragraphs[0]
    p.text = "TRƯỜNG ĐẠI HỌC FPT • KHOA ĐIỆN TỬ - VIỄN THÔNG"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
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
    p.text = "Hệ Thống Nhúng Giám Sát Chất Lượng Nước & Cho Ăn Tự Động"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(6)

    p = tf_l.add_paragraph()
    p.text = "ĐỒ ÁN TỐT NGHIỆP HỌC PHẦN: LẬP TRÌNH VI ĐIỀU KHIỂN (MCP201)"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.space_before = Pt(28)

    p = tf_l.add_paragraph()
    p.text = "STM32F401RE Nucleo • FreeRTOS (CMSIS-RTOS v2) • ESP32 Wi-Fi Co-Processor\nRepository: https://github.com/Nonne07/mcp201-aquatic-guardian"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(8)

    # Right Team Box
    c_r = add_card(s1, Inches(7.8), Inches(1.2), Inches(4.733), Inches(5.0), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s1, Inches(7.8), Inches(1.2), Inches(4.733), Inches(0.4), "NHÓM 7 — LỚP IC2005", bg_color=COLOR_CARD_DARK)
    tf_r = c_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = Inches(0.35)
    tf_r.margin_top = Inches(0.55)

    team = [
        ("Nghiêm Hoàng Tùng (SE211196)", "Trưởng nhóm • Kiến trúc & Lập lịch FreeRTOS"),
        ("Hoàng Đức Mạnh (SE211191)", "Cảm biến & Thuật toán lọc tín hiệu số DSP"),
        ("Đỗ Khắc Lê Gia (SE211559)", "Cơ cấu chấp hành Servo, Rơ-le & Nguồn điện"),
        ("Phạm Hồng Minh (SE211181)", "Giao tiếp bus I2C1, RTC DS3231 & Giao diện LCD"),
        ("Nguyễn Đức Anh (SE211485)", "Phân hệ IoT, Telegram Bot API & Kiểm thử")
    ]
    for idx, (m_name, m_role) in enumerate(team):
        p = tf_r.add_paragraph() if idx > 0 else tf_r.paragraphs[0]
        p.text = m_name
        p.font.name = 'Segoe UI'
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY
        if idx > 0:
            p.space_before = Pt(10)

        p_r = tf_r.add_paragraph()
        p_r.text = m_role
        p_r.font.name = 'Segoe UI'
        p_r.font.size = Pt(9.5)
        p_r.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 2: Problem Statement (Bối Cảnh Sinh Thái)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Phần 1: Bối Cảnh & Mục Tiêu", 
               "3 NGUYÊN NHÂN CHÍNH GÂY SUY THOÁI BỂ CÁ & GIẢI PHÁP", 
               "Loại bỏ rủi ro ô nhiễm nước và giúp sinh vật thủy sinh phát triển ổn định")

    c_w = Inches(3.7)
    gap = Inches(0.3)
    y_start = Inches(1.8)

    cards_p2 = [
        ("1. NỒNG ĐỘ TDS NGUY HẠI", "> 500 ppm",
         "- Thức ăn thừa & chất thải phân hủy sinh độc tố Ammonia và Nitrite.\n"
         "- TDS > 500 ppm làm hỏng biểu mô mang và sốc thẩm thấu sinh học.\n"
         "- Hệ thống: Giám sát ADC1 thời gian thực và báo động tức thì < 200ms."),
        ("2. BIẾN ĐỘNG NHIỆT ĐỘ", "24°C – 28°C",
         "- Cá nhiệt đới chỉ thích nghi trong dải nhiệt độ tiêu chuẩn 24°C – 28°C.\n"
         "- Nhiệt độ tăng vượt 30°C làm suy giảm nghiêm trọng lượng oxy hòa tan (DO).\n"
         "- Hệ thống: Cảm biến DS18B20 1-Wire bù nhiệt chuẩn xác cho giá trị TDS."),
        ("3. SAI LỆCH ĐỊNH LƯỢNG", "80% Cá Chết",
         "- Cho ăn dư thừa làm đục nước; quên cho ăn làm cá suy kiệt thể trạng.\n"
         "- Chủ vắng nhà dài ngày không thể kiểm soát lịch trình dinh dưỡng.\n"
         "- Hệ thống: Định lượng 1g – 15g qua Servo, RTC hẹn giờ & Bot từ xa.")
    ]

    for i, (title, stat, body) in enumerate(cards_p2):
        cx = Inches(0.8) + i * (c_w + gap)
        card = add_card(s2, cx, y_start, c_w, Inches(4.8), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
        add_badge(s2, cx, y_start, c_w, Inches(0.4), title, bg_color=COLOR_CARD_DARK)
        
        # Stat callout
        stat_box = add_card(s2, cx + Inches(0.3), y_start + Inches(0.6), c_w - Inches(0.6), Inches(0.65), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_LIGHT)
        tf_s = stat_box.text_frame
        p_s = tf_s.paragraphs[0]
        p_s.text = stat
        p_s.font.name = 'Segoe UI'
        p_s.font.size = Pt(13)
        p_s.font.bold = True
        p_s.font.color.rgb = COLOR_TEXT_PRIMARY
        p_s.alignment = PP_ALIGN.CENTER

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.3)
        tf.margin_top = Inches(1.35)

        p = tf.paragraphs[0]
        p.text = body
        p.font.name = 'Segoe UI'
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 3: System Block Diagram (Sơ Đồ Khối Kiến Trúc Phân Tán)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Phần 2: Sơ Đồ Khối & Phần Cứng", 
               "SƠ ĐỒ KHỐI HỆ THỐNG PHÂN TÁN (DISTRIBUTED DUAL-MCU)", 
               "Tách biệt giữa Điều khiển Thời gian thực (STM32) và Mạng viễn thông IoT (ESP32)")

    col_y = Inches(1.7)
    col_h = Inches(4.2)

    cols_s3 = [
        ("1. CẢM BIẾN (INPUT)", Inches(0.8), Inches(2.6), [
            ("TDS Analog V1.0", "PA1 (ADC1_IN1)", "Lọc tụ gốm 0.1 µF"),
            ("Biến trở B10K", "PA4 (ADC1_IN4)", "Chỉnh liều 1g – 15g"),
            ("DS18B20 1-Wire", "PA8 (GPIO OD)", "Trở kéo ngoài 4.7 kΩ"),
            ("Nút User B1", "PC13 (EXTI13)", "Lọc rung phím 300 ms")
        ]),
        ("2. NUCLEO-64 (CORE)", Inches(3.7), Inches(3.8), [
            ("STM32F401RE", "ARM Cortex-M4", "Xung nhịp 84 MHz, FPU"),
            ("FreeRTOS v2", "CMSIS-RTOS v2", "5 Tác vụ đa nhiệm tiền định"),
            ("Đồng bộ IPC", "Length-1 Mailbox", "Chống tắc nghẽn dữ liệu"),
            ("Kế thừa ưu tiên", "Mutex I2C1", "Chống khóa chết bus")
        ]),
        ("3. CHẤP HÀNH (OUTPUT)", Inches(7.8), Inches(2.6), [
            ("Servo SG90", "PA0 (TIM2 PWM)", "Quay 90° xả thức ăn"),
            ("Rơ-le 5V", "PB4 (GPIO Out)", "Đóng ngắt máy bơm mini"),
            ("Active Buzzer", "PB0 (Đệm S8050)", "Còi báo động khẩn cấp"),
            ("LCD 2004", "PB8/PB9 (I2C1)", "Hiển thị 4 dòng thông số")
        ]),
        ("4. IOT BRIDGE", Inches(10.7), Inches(1.833), [
            ("ESP32 Wi-Fi", "UART1 @ 115200", "Định khung '~'"),
            ("Telegram Bot", "HTTPS Long-Poll", "Lệnh /status & /feed"),
            ("Web Local", "Port 80 HTTP", "Dashboard điện thoại"),
            ("3.0 điểm Rubric", "Complexity", "Module truyền thông")
        ])
    ]

    for title, cx, cw, items in cols_s3:
        card = add_card(s3, cx, col_y, cw, col_h, bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
        add_badge(s3, cx, col_y, cw, Inches(0.35), title, bg_color=COLOR_CARD_DARK)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.18)
        tf.margin_top = Inches(0.45)

        for idx, (name, pin, desc) in enumerate(items):
            p = tf.add_paragraph() if idx > 0 else tf.paragraphs[0]
            p.text = name
            p.font.name = 'Segoe UI'
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = COLOR_TEXT_PRIMARY
            if idx > 0:
                p.space_before = Pt(6)

            p_s = tf.add_paragraph()
            p_s.text = f"  [{pin}] {desc}"
            p_s.font.name = 'Segoe UI'
            p_s.font.size = Pt(8.5)
            p_s.font.color.rgb = COLOR_TEXT_MUTED

    # Bottom Takeaway Note
    b_note = add_card(s3, Inches(0.8), Inches(6.1), Inches(11.733), Inches(0.7), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_DARK, border_width=Pt(1.2))
    tf_bn = b_note.text_frame
    tf_bn.word_wrap = True
    tf_bn.margin_left = Inches(0.25)
    tf_bn.margin_top = Inches(0.1)
    p = tf_bn.paragraphs[0]
    p.text = "[NGUYÊN LÝ KIẾN TRÚC DUAL-MCU]: STM32 đảm bảo đáp ứng thời gian thực cứng (Hard Real-Time); ESP32 đảm nhận kết nối Wi-Fi/Telegram không tất định. Hai vi điều khiển liên kết qua UART1 định khung '~' ở tốc độ 115200 bps."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # =========================================================================
    # SLIDE 4: Hardware Analysis (Phân Tích Mạch Điện)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Phần 2: Sơ Đồ Khối & Phần Cứng", 
               "PHÂN TÍCH MẠCH ĐIỆN & 4 GIẢI PHÁP PHẦN CỨNG THỰC NGHIỆM", 
               "Khắc phục triệt để các rủi ro sụt áp, dòng cảm biến và sai lệch mức logic khi cắm mạch thực tế")

    grid_w = Inches(5.7)
    grid_h = Inches(2.2)
    coords4 = [
        (Inches(0.8), Inches(1.8)), (Inches(6.833), Inches(1.8)),
        (Inches(0.8), Inches(4.3)), (Inches(6.833), Inches(4.3))
    ]

    hw_cards = [
        ("1. SỤT ÁP IC ỔN ÁP MB102",
         "Rủi ro: Dropout của AMS1117 là 1.2V. Cấp 5V USB làm sụt áp đầu ra xuống ~3.8V, khiến LCD bị tối và rơ-le không đóng được.",
         "Giải pháp: Cấp Adapter DC 9V/12V qua cổng chân tròn 5.5mm, bảo đảm đầu ra luôn đạt chuẩn 5.0V ổn định."),
        ("2. QUÁ DÒNG CÒI ACTIVE BUZZER",
         "Rủi ro: Còi buzzer 2 chân rút dòng tức thời 25 – 35 mA vượt ngưỡng chân PB0 (8 – 15 mA), xung cảm gây treo chip.",
         "Giải pháp: Sử dụng Module Buzzer 3 chân có đệm Transistor S8050, giảm dòng điều khiển chân PB0 xuống < 1 mA."),
        ("3. NGUY CƠ HỎNG PIN RTC CR2032",
         "Rủi ro: Mạch ZS-042 có sẵn đường nạp nhồi cho pin sạc LIR2032. Cấp 5V làm nạp ngược gây phồng rỉ pin CR2032 tiêu chuẩn.",
         "Giải pháp: Cấp nguồn 3.3V từ STM32 vào chân VCC của module để vô hiệu hóa mạch sạc, hoặc cách ly điện trở nạp 200 Ω."),
        ("4. HIỆN TƯỢNG DÍNH ĐÓNG RƠ-LE 5V",
         "Rủi ro: Chênh lệch mức logic giữa 3.3V (STM32) và 5.0V (Rơ-le Low-Trigger) làm optocoupler luôn dẫn nhẹ, rơ-le không nhả.",
         "Giải pháp: Chọn module rơ-le có Jumper chuyển sang chế độ High-Trigger phù hợp chuẩn logic 3.3V của vi điều khiển.")
    ]

    for i in range(4):
        cx, cy = coords4[i]
        title, prob, fix = hw_cards[i]
        card = add_card(s4, cx, cy, grid_w, grid_h, bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
        add_badge(s4, cx, cy, grid_w, Inches(0.35), title, bg_color=COLOR_CARD_DARK)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.4)

        p = tf.paragraphs[0]
        p.text = prob
        p.font.name = 'Segoe UI'
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_TEXT_MUTED

        p_f = tf.add_paragraph()
        p_f.text = fix
        p_f.font.name = 'Segoe UI'
        p_f.font.size = Pt(9.5)
        p_f.font.bold = True
        p_f.font.color.rgb = COLOR_TEXT_PRIMARY
        p_f.space_before = Pt(6)

    # Bottom bar
    b_hw = add_card(s4, Inches(0.8), Inches(6.65), Inches(11.733), Inches(0.45), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_LIGHT)
    tf_bh = b_hw.text_frame
    tf_bh.word_wrap = True
    tf_bh.margin_left = Inches(0.2)
    tf_bh.margin_top = Inches(0.08)
    p = tf_bh.paragraphs[0]
    p.text = "[NGUYÊN TẮC BỔ TRỢ]: Trở kéo ngoài 4.7 kΩ cho DS18B20; Đấu chéo UART1 (PA9 TX -> RX2, PA10 RX <- TX2); Chung mass GND toàn mạch."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # =========================================================================
    # SLIDE 5: FreeRTOS 5 Tasks (Kiến Trúc Đa Nhiệm FreeRTOS)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Phần 3: Phần Mềm & Thời Gian Thực", 
               "KIẾN TRÚC ĐA NHIỆM TIỀN ĐỊNH FREERTOS (CMSIS-RTOS V2)", 
               "Phân rã 5 tác vụ độc lập, lập lịch ưu tiên tuyệt đối loại bỏ hoàn toàn blocking delay")

    # Table of 5 Tasks
    table_shape = s5.shapes.add_table(6, 5, Inches(0.8), Inches(1.8), Inches(11.733), Inches(3.4))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(2.6)
    tbl.columns[1].width = Inches(1.8)
    tbl.columns[2].width = Inches(1.5)
    tbl.columns[3].width = Inches(1.4)
    tbl.columns[4].width = Inches(4.433)

    headers = ["Tên Tác Vụ (Thread)", "Mức Ưu Tiên", "Chu Kỳ Kích Hoạt", "Stack Size", "Nhiệm Vụ Chính"]
    for c_idx, h in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        set_cell_background(cell, "0F172A")
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = 'Segoe UI'
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_WHITE

    t_data = [
        ("Task_SafetySupervisor", "High (32)", "200 ms", "1024 Bytes", "Giám sát TDS/Nhiệt độ, kích hoạt còi báo & LED Alert"),
        ("Task_DispenserControl", "AboveNormal (24)", "Event-Driven", "1024 Bytes", "Chờ Semaphore nút/bot, quay Servo xả cám & ghi EEPROM"),
        ("Task_SensorAcquisition", "Normal (16)", "1000 ms", "1024 Bytes", "Thu thập ADC1, lọc số 20 mẫu O(1), tính TDS bù nhiệt"),
        ("Task_DisplayUI", "BelowNormal (12)", "500 ms", "2048 Bytes", "Đọc giờ RTC DS3231, cập nhật 4 dòng LCD 2004 qua I2C1"),
        ("Task_Telemetry", "Low (8)", "2000 ms", "2048 Bytes", "Đóng gói JSON định khung '~' phát qua ESP32 và USB VCP")
    ]
    for r_idx, r_val in enumerate(t_data, 1):
        for c_idx, val in enumerate(r_val):
            cell = tbl.cell(r_idx, c_idx)
            set_cell_background(cell, "FFFFFF" if r_idx % 2 != 0 else "F1F5F9")
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = 'Segoe UI'
            p.font.size = Pt(9.5)
            p.font.color.rgb = COLOR_TEXT_PRIMARY
            if c_idx == 0:
                p.font.bold = True

    # Bottom Note
    c_stk = add_card(s5, Inches(0.8), Inches(5.45), Inches(11.733), Inches(1.2), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_DARK, border_width=Pt(1.2))
    add_badge(s5, Inches(0.8), Inches(5.45), Inches(11.733), Inches(0.3), "QUY ĐỊNH QUẢN LÝ BỘ NHỚ STACK TRONG CHUẨN CMSIS-RTOS V2", bg_color=COLOR_BORDER_DARK)
    tf_sk = c_stk.text_frame
    tf_sk.word_wrap = True
    tf_sk.margin_left = Inches(0.25)
    tf_sk.margin_top = Inches(0.35)
    p = tf_sk.paragraphs[0]
    p.text = "- Đơn vị Stack tính bằng BYTES: Trong CMSIS-RTOS v2, tham số .stack_size tính bằng Bytes (khác v1 tính bằng Words). Khai báo nhầm sẽ gây tràn Stack và kích hoạt lỗi HardFault khi gọi hàm snprintf().\n" \
             "- Cấp phát an toàn: 1024 Bytes cho tác vụ tính toán; 2048 Bytes cho tác vụ định dạng chuỗi hiển thị LCD và JSON."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # =========================================================================
    # SLIDE 6: Flowchart (Lưu Đồ Thuật Toán)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Phần 3: Phần Mềm & Thời Gian Thực", 
               "LƯU ĐỒ THUẬT TOÁN: CẤP DƯỠNG & XỬ LÝ TÍN HIỆU SỐ", 
               "Minh chứng lập trình phi khóa (Non-blocking) và xử lý ngắt trì hoãn an toàn")

    fc_w = Inches(5.7)

    # Column Left: Feeder Flowchart
    add_card(s6, Inches(0.8), Inches(1.8), fc_w, Inches(4.8), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s6, Inches(0.8), Inches(1.8), fc_w, Inches(0.35), "A. ĐIỀU KHIỂN CƠ CẤU CẤP DƯỠNG (EVENT-DRIVEN)", bg_color=COLOR_CARD_DARK)

    pipe_a = [
        ("1. Trạng thái chờ", "Task_DispenserControl ở trạng thái Blocked giải phóng 100% CPU"),
        ("2. Kích hoạt sự kiện", "Nhận Semaphore từ Nút bấm PC13 / Telegram / Hẹn giờ RTC"),
        ("3. Tính toán định lượng", "Đọc ADC biến trở: Dwell Time = 300ms + (Portion × 80ms)"),
        ("4. Điều khiển Servo", "PA0 phát PWM 50Hz: Quay mở 90° -> Trì hoãn Dwell -> Quay về 0°"),
        ("5. Ghi nhật ký EEPROM", "Chiếm Mutex I2C1 -> Lưu giờ & lượng ăn vào AT24C32 -> Nhả Mutex")
    ]
    for idx, (st, desc) in enumerate(pipe_a):
        sy = Inches(2.3) + idx * Inches(0.8)
        sc = add_card(s6, Inches(1.0), sy, Inches(5.3), Inches(0.68), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_LIGHT)
        stf = sc.text_frame
        stf.margin_left = Inches(0.2)
        stf.margin_top = Inches(0.08)
        p = stf.paragraphs[0]
        p.text = st
        p.font.name = 'Segoe UI'
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY
        p_d = stf.add_paragraph()
        p_d.text = desc
        p_d.font.name = 'Segoe UI'
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = COLOR_TEXT_MUTED

    # Column Right: Sensor Flowchart
    add_card(s6, Inches(6.833), Inches(1.8), fc_w, Inches(4.8), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s6, Inches(6.833), Inches(1.8), fc_w, Inches(0.35), "B. THU THẬP & XỬ LÝ CẢM BIẾN TDS (DSP)", bg_color=COLOR_CARD_DARK)

    pipe_b = [
        ("1. Định thời chính xác", "osDelayUntil(&last_wake, 1000ms) triệt tiêu hoàn toàn trôi pha"),
        ("2. Đọc kênh ADC1", "Lấy mẫu điện áp thô trên chân PA1 (Cảm biến TDS V1.0)"),
        ("3. Lọc số vòng O(1)", "Tổng chạy: Sum = Sum - RingBuf[i] + NewSample (Cửa sổ 20 mẫu)"),
        ("4. Bù nhiệt độ nước", "Đọc DS18B20: V_comp = V_adc / [1.0 + 0.02 × (T - 25.0)]"),
        ("5. Tính toán nồng độ", "Đa thức bậc 3 tính TDS (ppm) -> Ghi đè vào Length-1 Mailbox")
    ]
    for idx, (st, desc) in enumerate(pipe_b):
        sy = Inches(2.3) + idx * Inches(0.8)
        sc = add_card(s6, Inches(7.033), sy, Inches(5.3), Inches(0.68), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_LIGHT)
        stf = sc.text_frame
        stf.margin_left = Inches(0.2)
        stf.margin_top = Inches(0.08)
        p = stf.paragraphs[0]
        p.text = st
        p.font.name = 'Segoe UI'
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY
        p_d = stf.add_paragraph()
        p_d.text = desc
        p_d.font.name = 'Segoe UI'
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 7: DSP & Temperature Math (Thuật Toán Số & Bù Nhiệt)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Phần 3: Phần Mềm & Thời Gian Thực", 
               "THUẬT TOÁN LỌC SỐ O(1) & MÔ HÌNH TOÁN BÙ NHIỆT ĐỘ", 
               "Khử nhiễu biến động sóng nước và hiệu chuẩn nhiệt độ chính xác theo mô hình hóa học nước")

    col7_w = Inches(5.7)

    # Left: Filter Card
    c7_l = add_card(s7, Inches(0.8), Inches(1.8), col7_w, Inches(4.8), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s7, Inches(0.8), Inches(1.8), col7_w, Inches(0.35), "1. BỘ LỌC TRUNG BÌNH TRƯỢT VÒNG O(1)", bg_color=COLOR_CARD_DARK)
    tf7_l = c7_l.text_frame
    tf7_l.word_wrap = True
    tf7_l.margin_left = tf7_l.margin_right = Inches(0.3)
    tf7_l.margin_top = Inches(0.45)

    p = tf7_l.paragraphs[0]
    p.text = "Công thức cập nhật tổng chạy:"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # Code formula box
    f_box = add_card(s7, Inches(1.1), Inches(2.6), col7_w - Inches(0.6), Inches(1.0), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_LIGHT)
    tf_fb = f_box.text_frame
    p_fb = tf_fb.paragraphs[0]
    p_fb.text = "Sum = Sum - RingBuffer[idx] + NewSample;\nRingBuffer[idx] = NewSample;\nidx = (idx + 1) % 20;\nV_adc = (Sum / 20.0f) * 3.3f / 4095.0f;"
    p_fb.font.name = 'Consolas'
    p_fb.font.size = Pt(9)
    p_fb.font.color.rgb = COLOR_TEXT_PRIMARY

    tf7_l.margin_top = Inches(1.9)
    p = tf7_l.add_paragraph()
    p.text = "- Độ phức tạp O(1): Chỉ tốn 1 phép cộng và 1 phép trừ mỗi chu kỳ; không cần vòng lặp for duyệt 20 phần tử.\n" \
             "- Hiệu quả thực tế: Độ lệch chuẩn giảm từ ±45 ppm xuống < ±1.5 ppm, triệt tiêu hoàn toàn báo động giả do sóng nước."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_MUTED

    # Right: Temperature Math Card
    c7_r = add_card(s7, Inches(6.833), Inches(1.8), col7_w, Inches(4.8), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s7, Inches(6.833), Inches(1.8), col7_w, Inches(0.35), "2. MÔ HÌNH BÙ NHIỆT ĐỘ & ĐA THỨC TDS", bg_color=COLOR_CARD_DARK)
    tf7_r = c7_r.text_frame
    tf7_r.word_wrap = True
    tf7_r.margin_left = tf7_r.margin_right = Inches(0.3)
    tf7_r.margin_top = Inches(0.45)

    p = tf7_r.paragraphs[0]
    p.text = "Phương trình quy chuẩn về 25.0°C:"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # Math formula box
    m_box = add_card(s7, Inches(7.133), Inches(2.6), col7_w - Inches(0.6), Inches(1.0), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_LIGHT)
    tf_mb = m_box.text_frame
    p_mb = tf_mb.paragraphs[0]
    p_mb.text = "V_comp = V_adc / (1.0f + 0.02f * (T_water - 25.0f));\n\nTDS = (133.42 * V_comp^3 - 255.86 * V_comp^2\n      + 857.39 * V_comp) * 0.5f;"
    p_mb.font.name = 'Consolas'
    p_mb.font.size = Pt(9)
    p_mb.font.color.rgb = COLOR_TEXT_PRIMARY

    tf7_r.margin_top = Inches(1.9)
    p = tf7_r.add_paragraph()
    p.text = "- Hệ số bù nhiệt 2%/°C: Độ dẫn điện tăng theo nhiệt độ; nếu không bù nhiệt, nước nóng sẽ bị báo sai lệch tới 20%.\n" \
             "- Thực thi trên FPU Cortex-M4: Tính toán số thực đơn chu kỳ, thời gian thực thi < 2.5 µs."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 8: Concurrency & Priority Inheritance (Đồng Bộ IPC)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Phần 3: Phần Mềm & Thời Gian Thực", 
               "ĐỒNG BỘ IPC: LENGTH-1 MAILBOX & KẾ THỪA QUYỀN ƯU TIÊN", 
               "Giải quyết triệt để hai bài toán kinh điển: Tắc nghẽn dữ liệu và Nghịch đảo độ ưu tiên")

    col8_w = Inches(5.7)

    # Left: Mailbox Card
    c8_l = add_card(s8, Inches(0.8), Inches(1.8), col8_w, Inches(4.8), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s8, Inches(0.8), Inches(1.8), col8_w, Inches(0.35), "1. HÒM THƯ ĐƠN (LENGTH-1 MAILBOX)", bg_color=COLOR_CARD_DARK)
    tf8_l = c8_l.text_frame
    tf8_l.word_wrap = True
    tf8_l.margin_left = tf8_l.margin_right = Inches(0.3)
    tf8_l.margin_top = Inches(0.45)

    p = tf8_l.paragraphs[0]
    p.text = "- Vấn đề kỹ thuật (Data Starvation):\n" \
             "  Hàng đợi FreeRTOS có tính tiêu thụ xóa (Destructive Read). Tác vụ Supervisor (200ms) sẽ chiếm toàn bộ gói tin, khiến DisplayUI và Telemetry bị đói dữ liệu."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_MUTED

    p = tf8_l.add_paragraph()
    p.text = "- Giải pháp Length-1 Mailbox:\n" \
             "  • Producer (Sensor Task) sử dụng xQueueOverwrite() cập nhật bản tin mới nhất.\n" \
             "  • 3 Consumers đều sử dụng xQueuePeek() sao chép mà KHÔNG xóa phần tử.\n" \
             "  • Kết quả: Cả 3 tác vụ truy xuất độc lập theo chu kỳ riêng (200ms, 500ms, 2000ms), 0% mất dữ liệu."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.space_before = Pt(12)

    # Right: Priority Inheritance Card
    c8_r = add_card(s8, Inches(6.833), Inches(1.8), col8_w, Inches(4.8), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s8, Inches(6.833), Inches(1.8), col8_w, Inches(0.35), "2. KẾ THỪA QUYỀN ƯU TIÊN (PRIORITY INHERITANCE)", bg_color=COLOR_CARD_DARK)
    tf8_r = c8_r.text_frame
    tf8_r.word_wrap = True
    tf8_r.margin_left = tf8_r.margin_right = Inches(0.3)
    tf8_r.margin_top = Inches(0.45)

    p = tf8_r.paragraphs[0]
    p.text = "- Vấn đề kỹ thuật (Priority Inversion):\n" \
             "  DisplayUI (12) giữ Mutex I2C1; Dispenser (24) thức tỉnh cần ghi EEPROM. Nếu Task_Sensor (16) chiếm CPU, nó sẽ ngăn DisplayUI nhả bus, gián tiếp phong tỏa Dispenser."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_MUTED

    p = tf8_r.add_paragraph()
    p.text = "- Cơ chế Kế thừa ưu tiên:\n" \
             "  • Khi Task 24 đòi Mutex, FreeRTOS lập tức nâng ưu tiên DisplayUI từ 12 lên 24.\n" \
             "  • Task 16 không thể chen ngang, DisplayUI giải phóng Mutex trong 4.2 ms.\n" \
             "  • Task 24 lập tức chiếm bus ghi log an toàn, loại bỏ hoàn toàn nguy cơ khóa chết hệ thống."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.space_before = Pt(12)

    # =========================================================================
    # SLIDE 9: Critical Source Code (Mã Nguồn C Trọng Yếu)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Phần 3: Phần Mềm & Thời Gian Thực", 
               "PHÂN TÍCH MÃ NGUỒN C TRỌNG YẾU (SOURCE CODE ANALYSIS)", 
               "Minh chứng chất lượng lập trình nhúng STM32 HAL và ESP32 theo đúng tiêu chí Rubric (0.5đ)")

    col9_w = Inches(3.7)

    code_data = [
        ("A. DEFERRED ISR (NGẮT TRÌ HOÃN)",
         "void HAL_GPIO_EXTI_Callback(uint16_t Pin) {\n"
         "  static uint32_t last = 0;\n"
         "  if (Pin == GPIO_PIN_13) {\n"
         "    uint32_t now = HAL_GetTick();\n"
         "    if ((now - last) > 300U) {\n"
         "      last = now;\n"
         "      // Nhả Semaphore < 1us\n"
         "      osSemaphoreRelease(feedSem);\n"
         "    }\n"
         "  }\n"
         "}",
         "- Không đặt delay trong hàm ngắt ISR.\n"
         "- Thời gian ngắt < 1 µs, bàn giao xử lý nặng cho Thread."),
        ("B. TÍNH TỔNG CHẠY O(1)",
         "// Circular Buffer Moving Sum\n"
         "tds_sum -= ring_buf[buf_idx];\n"
         "tds_sum += new_raw_adc;\n"
         "ring_buf[buf_idx] = new_raw_adc;\n"
         "buf_idx = (buf_idx + 1) % 20;\n\n"
         "float v = (tds_sum/20.0f)*3.3f/4095;\n"
         "float vc = v/(1.0f+0.02f*(t-25));\n"
         "tds = (133.42*vc*vc*vc\n"
         "     - 255.86*vc*vc + 857.39*vc)*0.5f;",
         "- Không dùng vòng lặp for duyệt mảng.\n"
         "- Tối ưu hóa chu kỳ CPU và năng lượng vi điều khiển."),
        ("C. BỘ GIẢI MÃ KHUNG UART FSM",
         "// FSM Delimiter '~' Decoder\n"
         "while (SerialSTM32.available()) {\n"
         "  char c = (char)SerialSTM32.read();\n"
         "  if (c == '~') {\n"
         "    in_frame = !in_frame;\n"
         "    if (!in_frame)\n"
         "      parsePacket(rx_buf);\n"
         "    else rx_buf = \"\";\n"
         "  } else if (in_frame)\n"
         "    rx_buf += c;\n"
         "}",
         "- Loại bỏ hoàn toàn byte rác do cắm rút dây hoặc nhiễu.\n"
         "- Bảo đảm tính toàn vẹn gói tin JSON đạt 100%.")
    ]

    for i, (title, code_snip, takeaway) in enumerate(code_data):
        cx = Inches(0.8) + i * (col9_w + Inches(0.3))
        add_card(s9, cx, Inches(1.8), col9_w, Inches(4.8), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
        add_badge(s9, cx, Inches(1.8), col9_w, Inches(0.35), title, bg_color=COLOR_CARD_DARK)
        
        # Code box
        c_box = add_card(s9, cx + Inches(0.2), Inches(2.25), col9_w - Inches(0.4), Inches(3.0), bg_color=COLOR_CODE_BG, border_color=COLOR_BORDER_DARK)
        tf_c = c_box.text_frame
        tf_c.margin_left = Inches(0.2)
        tf_c.margin_top = Inches(0.15)
        p = tf_c.paragraphs[0]
        p.text = code_snip
        p.font.name = 'Consolas'
        p.font.size = Pt(8.5)
        p.font.color.rgb = COLOR_CODE_TEXT

        # Takeaway text below code box
        tf_t = s9.shapes.add_textbox(cx + Inches(0.2), Inches(5.35), col9_w - Inches(0.4), Inches(1.1)).text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
        p = tf_t.paragraphs[0]
        p.text = takeaway
        p.font.name = 'Segoe UI'
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_TEXT_PRIMARY

    # =========================================================================
    # SLIDE 10: IoT & Telegram Subsystem (Phân Hệ IoT & Telegram)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Phần 4: Phân Hệ IoT & Kiểm Thử", 
               "PHÂN HỆ IOT ESP32 & NỀN TẢNG TELEGRAM BOT", 
               "Module truyền thông không dây đạt trọn vẹn 3.0 điểm Project Complexity trong Rubric")

    # Top Framing Banner
    top_f = add_card(s10, Inches(0.8), Inches(1.8), Inches(11.733), Inches(1.2), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_DARK, border_width=Pt(1.2))
    add_badge(s10, Inches(0.8), Inches(1.8), Inches(11.733), Inches(0.3), "CẤU TRÚC ĐỊNH KHUNG UART 2 CHIỀU (BAUDRATE 115200 BPS)", bg_color=COLOR_BORDER_DARK)

    # Delimiter Start
    add_badge(s10, Inches(1.1), Inches(2.25), Inches(1.6), Inches(0.6), "BẮT ĐẦU\n'~' (0x7E)", bg_color=COLOR_CARD_DARK, text_color=COLOR_TEXT_WHITE, font_size=8.5)
    # Payload
    pld = add_card(s10, Inches(2.9), Inches(2.25), Inches(7.533), Inches(0.6), bg_color=COLOR_BG_WHITE, border_color=COLOR_BORDER_DARK)
    p = pld.text_frame.paragraphs[0]
    p.text = "DỮ LIỆU TẢI: JSON Telemetry ({\"tds\":185,\"temp\":26.5})   HOẶC   Lệnh: 'feed' / 'status'"
    p.font.name = 'Consolas'
    p.font.size = Pt(9)
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.alignment = PP_ALIGN.CENTER
    # Delimiter End
    add_badge(s10, Inches(10.633), Inches(2.25), Inches(1.6), Inches(0.6), "KẾT THÚC\n'~' (0x7E)", bg_color=COLOR_CARD_DARK, text_color=COLOR_TEXT_WHITE, font_size=8.5)

    # 2 Bottom Cards
    c10_w = Inches(5.7)

    # Left: Long Polling
    c10_l = add_card(s10, Inches(0.8), Inches(3.2), c10_w, Inches(3.4), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s10, Inches(0.8), Inches(3.2), c10_w, Inches(0.35), "1. CƠ CHẾ HTTPS LONG-POLLING", bg_color=COLOR_CARD_DARK)
    tf10_l = c10_l.text_frame
    tf10_l.word_wrap = True
    tf10_l.margin_left = tf10_l.margin_right = Inches(0.3)
    tf10_l.margin_top = Inches(0.45)
    p = tf10_l.paragraphs[0]
    p.text = "- Kết nối TLS/HTTPS Cổng 443 tới api.telegram.org qua UniversalTelegramBot.\n\n" \
             "- Xuyên Router / NAT: Chạy trên mọi mạng Wi-Fi/4G không cần IP tĩnh hay mở port.\n\n" \
             "- Chi phí 0 đồng: Tạo bot trong 30 giây qua @BotFather, API miễn phí 100%."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # Right: Commands & Push Alert
    c10_r = add_card(s10, Inches(6.833), Inches(3.2), c10_w, Inches(3.4), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s10, Inches(6.833), Inches(3.2), c10_w, Inches(0.35), "2. BỘ LỆNH & CẢNH BÁO CHỦ ĐỘNG", bg_color=COLOR_CARD_DARK)
    tf10_r = c10_r.text_frame
    tf10_r.word_wrap = True
    tf10_r.margin_left = tf10_r.margin_right = Inches(0.3)
    tf10_r.margin_top = Inches(0.45)
    p = tf10_r.paragraphs[0]
    p.text = "- Lệnh /status: Xem TDS, nhiệt độ, khẩu phần và trạng thái nước thời gian thực.\n\n" \
             "- Lệnh /feed: Phát chuỗi ~feed~ qua UART kích hoạt Servo xả đúng liều.\n\n" \
             "- Auto Push Notification: Tự động gửi tin nhắn khẩn cấp khi TDS > 500 ppm.\n\n" \
             "- Web Dashboard nội bộ: Truy cập thẳng địa chỉ IP của ESP32 từ trình duyệt."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # =========================================================================
    # SLIDE 11: Validation & Benchmarks (Kiểm Thử & Hiệu Năng)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Phần 4: Phân Hệ IoT & Kiểm Thử", 
               "KẾT QUẢ KIỂM THỬ ĐỘC LẬP & ĐO LƯỜNG THỜI GIAN THỰC", 
               "Xác thực 4 module độc lập và chứng minh đáp ứng các ràng buộc thời gian thực nghiêm ngặt")

    c11_w = Inches(5.7)

    # Left: Unit Tests
    c11_l = add_card(s11, Inches(0.8), Inches(1.8), c11_w, Inches(4.8), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s11, Inches(0.8), Inches(1.8), c11_w, Inches(0.35), "KIỂM THỬ 4 MODULE PHẦN MỀM ĐỘC LẬP", bg_color=COLOR_CARD_DARK)
    tf11_l = c11_l.text_frame
    tf11_l.word_wrap = True
    tf11_l.margin_left = tf11_l.margin_right = Inches(0.3)
    tf11_l.margin_top = Inches(0.45)

    u_tests = [
        ("test_servo_pwm.c", "PWM 50Hz, mở 90° chính xác; Dwell Time đáp ứng 380ms – 1500ms"),
        ("test_tds_filter.c", "Bộ lọc 20 mẫu O(1) giảm 96.7% phương sai sóng nước (±1.5 ppm)"),
        ("test_i2c_scanner.c", "Nhận diện đủ 3 thiết bị (0x27 LCD, 0x68 RTC, 0x57 EEPROM)"),
        ("test_uart_bridge.c", "Truyền 1,000 gói JSON liên tục @ 115200: Tỷ lệ lỗi khung 0.0%")
    ]
    for idx, (t_name, t_res) in enumerate(u_tests):
        p = tf11_l.add_paragraph() if idx > 0 else tf11_l.paragraphs[0]
        p.text = t_name
        p.font.name = 'Segoe UI'
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY
        if idx > 0:
            p.space_before = Pt(8)

        p_r = tf11_l.add_paragraph()
        p_r.text = f"  {t_res}"
        p_r.font.name = 'Segoe UI'
        p_r.font.size = Pt(9.5)
        p_r.font.color.rgb = COLOR_TEXT_MUTED

    # Right: Latency & Memory
    c11_r = add_card(s11, Inches(6.833), Inches(1.8), c11_w, Inches(4.8), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s11, Inches(6.833), Inches(1.8), c11_w, Inches(0.35), "ĐO LƯỜNG ĐỘ TRỄ & BỘ NHỚ THỰC TẾ", bg_color=COLOR_CARD_DARK)
    tf11_r = c11_r.text_frame
    tf11_r.word_wrap = True
    tf11_r.margin_left = tf11_r.margin_right = Inches(0.3)
    tf11_r.margin_top = Inches(0.45)

    p = tf11_r.paragraphs[0]
    p.text = "Thời gian đáp ứng hệ thống (Latency):"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    p = tf11_r.add_paragraph()
    p.text = "• Phát hiện vượt ngưỡng TDS: 185 ms (Tiêu chuẩn: < 300 ms)\n" \
             "• Độ trễ ngắt nút bấm EXTI: 0.85 µs (Tiêu chuẩn: < 10 µs)\n" \
             "• Thời gian nhả Mutex I2C1: 4.2 ms (Ngưỡng an toàn: < 50 ms)\n" \
             "• Độ trễ truyền gói UART: 2.8 ms (Ngưỡng cho phép: < 10 ms)"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(4)

    p = tf11_r.add_paragraph()
    p.text = "Chiếm dụng tài nguyên STM32F401RE:"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.space_before = Pt(12)

    p = tf11_r.add_paragraph()
    p.text = "• Flash ROM: 48.2 KB / 512 KB (Chiếm 9.41% – Còn dư > 90%)\n" \
             "• Static SRAM: 12.4 KB / 96 KB (Chiếm 12.92% – Còn dư > 87%)\n" \
             "• FreeRTOS Heap_4: 4096 / 8192 Bytes (50.0% an toàn)"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 12: 4-Stage Live Demonstration (Kịch Bản Trình Diễn)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Phần 5: Trình Diễn & Kết Luận", 
               "KỊCH BẢN TRÌNH DIỄN MÔ HÌNH THỰC TẾ 4 GIAI ĐOẠN", 
               "Quy trình diễn tập chuẩn mực trong vòng 2 phút đạt điểm tuyệt đối Demonstration (1.0đ)")

    coords12 = [
        (Inches(0.8), Inches(1.8)), (Inches(6.833), Inches(1.8)),
        (Inches(0.8), Inches(4.1)), (Inches(6.833), Inches(4.1))
    ]
    grid12_w = Inches(5.7)
    grid12_h = Inches(2.1)

    stages = [
        ("BƯỚC 1: KHỞI ĐỘNG (20s)", 
         "- Thao tác: Cấp nguồn Adapter 9V DC vào mạch MB102.\n"
         "- Phản hồi: LCD 2004 hiển thị 4 dòng thông số; LED xanh PA5 sáng ổn định; Rơ-le 5V đóng máy bơm nước tuần hoàn."),
        ("BƯỚC 2: CHO ĂN THỦ CÔNG (30s)", 
         "- Thao tác: Vặn biến trở PA4 (chỉnh 1g – 15g), nhấn nút PC13.\n"
         "- Phản hồi: Servo SG90 quay 90° mở nắp xả thức ăn đúng thời gian Dwell Time; ghi nhật ký vào EEPROM qua I2C."),
        ("BƯỚC 3: ĐIỀU KHIỂN TELEGRAM (30s)", 
         "- Thao tác: Gửi lệnh /status và /feed qua ứng dụng Telegram trên điện thoại.\n"
         "- Phản hồi: Bot báo cáo thông số trong < 1s; Servo chấp hành lập tức mở nắp xả thức ăn từ xa."),
        ("BƯỚC 4: MÔ PHỎNG SỰ CỐ (40s)", 
         "- Thao tác: Nhấc đầu dò TDS nhúng sang cốc nước muối (> 500 ppm).\n"
         "- Phản hồi: Trong < 200ms, còi Buzzer kêu, LED đỏ nháy 1Hz, LCD báo 'CRITICAL HAZARD', Telegram tự động bắn cảnh báo đỏ.")
    ]

    for i in range(4):
        cx, cy = coords12[i]
        title, body = stages[i]
        add_card(s12, cx, cy, grid12_w, grid12_h, bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
        add_badge(s12, cx, cy, grid12_w, Inches(0.35), title, bg_color=COLOR_CARD_DARK)
        tf = s12.shapes.add_textbox(cx + Inches(0.2), cy + Inches(0.4), grid12_w - Inches(0.4), grid12_h - Inches(0.45)).text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = body
        p.font.name = 'Segoe UI'
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_TEXT_PRIMARY

    # Bottom bar
    b_demo = add_card(s12, Inches(0.8), Inches(6.4), Inches(11.733), Inches(0.55), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_DARK, border_width=Pt(1.2))
    p = b_demo.text_frame.paragraphs[0]
    p.text = "[MÃ NGUỒN & TÀI LIỆU GỐC]: https://github.com/Nonne07/mcp201-aquatic-guardian. Nhóm 7 sẵn sàng cho phần Vấn đáp chuyên sâu (Q&A 3.0đ)!"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 13: Appendix (Phụ Lục Bộ Nhớ & Kênh Dự Phòng)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Phụ Lục Kỹ Thuật (Backup Slide)", 
               "BẢN ĐỒ BỘ NHỚ HỆ THỐNG & KÊNH VIỄN THÔNG DỰ PHÒNG FAILSAFE", 
               "Tài liệu kỹ thuật phục vụ vấn đáp chuyên sâu về quản lý tài nguyên vi điều khiển (Q&A 3.0đ)")

    col13_w = Inches(5.7)

    # Left: Memory Map
    c13_l = add_card(s13, Inches(0.8), Inches(1.8), col13_w, Inches(4.8), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s13, Inches(0.8), Inches(1.8), col13_w, Inches(0.35), "1. PHÂN BỔ BỘ NHỚ CHI TIẾT (MEMORY FOOTPRINT)", bg_color=COLOR_CARD_DARK)
    tf13_l = c13_l.text_frame
    tf13_l.word_wrap = True
    tf13_l.margin_left = tf13_l.margin_right = Inches(0.3)
    tf13_l.margin_top = Inches(0.45)

    p = tf13_l.paragraphs[0]
    p.text = "• Flash ROM (512 KB): 48.2 KB (9.41%)\n" \
             "  Bao gồm STM32 HAL Drivers, FreeRTOS Kernel, libc math routines và Task functions.\n\n" \
             "• Static RAM (96 KB): 12.4 KB (12.92%)\n" \
             "  Bao gồm biến toàn cục, Circular Buffers, DMA Descriptors và vùng nhớ .data/.bss.\n\n" \
             "• FreeRTOS Heap (Heap_4): 4096 / 8192 Bytes (50% an toàn)\n" \
             "  Cấp phát 5 TCBs, 5 Task Stacks, 2 Mutexes và 1 Semaphore.\n\n" \
             "• uxTaskGetStackHighWaterMark():\n" \
             "  Xác nhận tất cả tác vụ đều còn dư > 35% biên độ an toàn, không có nguy cơ tràn Stack."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # Right: Failsafe PC Bridge
    c13_r = add_card(s13, Inches(6.833), Inches(1.8), col13_w, Inches(4.8), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s13, Inches(6.833), Inches(1.8), col13_w, Inches(0.35), "2. KÊNH DỰ PHÒNG ST-LINK VIRTUAL COM PORT", bg_color=COLOR_CARD_DARK)
    tf13_r = c13_r.text_frame
    tf13_r.word_wrap = True
    tf13_r.margin_left = tf13_r.margin_right = Inches(0.3)
    tf13_r.margin_top = Inches(0.45)

    p = tf13_r.paragraphs[0]
    p.text = "• Nguyên lý kết nối:\n" \
             "  Cặp chân PA2/PA3 được nối cứng với chip nạp ST-LINK/V2-1 trên bo Nucleo, tự động tạo cổng USB Virtual COM Port (VCP) nối vào laptop.\n\n" \
             "• Script Python độc lập (scripts/aquatic_pc_bridge.py):\n" \
             "  Giải mã chuỗi JSON từ Task_Telemetry ở baudrate 115200 bps và vẽ đồ thị thời gian thực trên màn hình PC.\n\n" \
             "• Phương án dự phòng Failsafe:\n" \
             "  Nếu Wi-Fi phòng thi gặp sự cố, hệ thống vẫn trình diễn đầy đủ đồ thị live qua cáp USB mà không cần bất kỳ kết nối mạng nào."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # Save presentation
    out_pptx = r"E:\AntiGravityRoot\mcp201-aquatic-guardian\AQUATIC_GUARDIAN_SLIDES.pptx"
    out_alt  = r"E:\AntiGravityRoot\mcp201-aquatic-guardian\AQUATIC_GUARDIAN_SLIDES_TIENGVIET.pptx"
    out_new  = r"E:\AntiGravityRoot\mcp201-aquatic-guardian\AQUATIC_GUARDIAN_SLIDES_NEW.pptx"

    saved = False
    try:
        prs.save(out_pptx)
        print(f"[SUCCESS] Native Vietnamese slides generated at: {out_pptx}")
        saved = True
    except PermissionError:
        print(f"[WARNING] {out_pptx} is locked by PowerPoint.")

    try:
        prs.save(out_new)
        print(f"[SUCCESS] Native Vietnamese slides also saved at: {out_new}")
        saved = True
    except PermissionError:
        pass

    if not saved:
        prs.save(out_alt)
        print(f"[SUCCESS] Native Vietnamese slides saved at: {out_alt}")

if __name__ == '__main__':
    build_presentation()
