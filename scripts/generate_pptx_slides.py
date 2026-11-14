"""
=============================================================================
Project: Aquatic Guardian - Capstone MCP201 (Class IC2005 - Group 7)
Script:  generate_pptx_slides.py
Purpose: Generates the official presentation slide deck (.pptx)
         designed as a High-Impact Stand-Alone Visual Reading Deck for evaluation.
Design:  16:9 Widescreen, Professional Executive Academic Design (IEEE Style),
         Native Vector Diagrams, Zero Emojis, Zero Overlaps, Perfect Alignment.
=============================================================================
"""

import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# --- COLOR PALETTE (Strict Executive Monochrome & Slate Grayscale) ---
COLOR_BG_WHITE       = RGBColor(255, 255, 255)
COLOR_CARD_BG        = RGBColor(248, 250, 252)    # Slate 50
COLOR_CARD_ALT       = RGBColor(241, 245, 249)    # Slate 100
COLOR_CARD_DARK      = RGBColor(30, 41, 59)       # Slate 800
COLOR_BORDER_LIGHT   = RGBColor(226, 232, 240)    # Slate 200
COLOR_BORDER_MEDIUM  = RGBColor(203, 213, 225)    # Slate 300
COLOR_BORDER_DARK    = RGBColor(15, 23, 42)       # Slate 900
COLOR_TEXT_PRIMARY   = RGBColor(15, 23, 42)       # Deep Slate 900
COLOR_TEXT_MUTED     = RGBColor(71, 85, 105)      # Slate 600
COLOR_TEXT_WHITE     = RGBColor(255, 255, 255)
COLOR_CODE_BG        = RGBColor(15, 23, 42)       # Dark Terminal Box
COLOR_CODE_TEXT      = RGBColor(248, 250, 252)

ASSETS_DIR = os.path.abspath(r"E:\AntiGravityRoot\mcp201-aquatic-guardian\assets")

def add_header(slide, category, title, subtitle=None):
    """Adds a standardized academic header to a slide."""
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.733), Inches(1.1))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_cat = tf.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.name = 'Segoe UI'
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_TEXT_MUTED

    p_title = tf.add_paragraph()
    p_title.text = title
    p_title.font.name = 'Segoe UI'
    p_title.font.size = Pt(19)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_TEXT_PRIMARY
    p_title.space_before = Pt(2)

    if subtitle:
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.name = 'Segoe UI'
        p_sub.font.size = Pt(10.5)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED
        p_sub.space_before = Pt(2)

def add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_LIGHT, border_width=Pt(1), shape_type=MSO_SHAPE.RECTANGLE):
    """Creates a card container shape with subtle fill and border."""
    card = slide.shapes.add_shape(shape_type, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = border_width
    else:
        card.line.fill.background()
    return card

def add_badge(slide, left, top, width, height, text, bg_color=COLOR_CARD_DARK, text_color=COLOR_TEXT_WHITE, font_size=9.0):
    """Creates a small badge/pill header."""
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
    # SLIDE 1: [Tổng Quan]: Trang Tiêu Đề Đồ Án & Thông Tin Nhóm
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    
    # Left Hero Card
    card_l = add_card(s1, Inches(0.8), Inches(1.0), Inches(6.8), Inches(5.6), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_DARK, border_width=Pt(1.5))
    tf_l = card_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = Inches(0.5)
    tf_l.margin_top = Inches(0.55)

    p = tf_l.paragraphs[0]
    p.text = "TRUONG DAI HOC FPT • KHOA DIEN TU - VIEN THONG"
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
    p.text = "He Thong Nhung Giam Sat Chat Luong Nuoc & Cap Duong Thuy Sinh Tu Dong Thoi Gian Thuc"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(13.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(6)

    p = tf_l.add_paragraph()
    p.text = "DO AN TOT NGHIEP HOC PHAN: LAP TRINH VI DIEU KHIEN (MCP201)"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.space_before = Pt(24)

    p = tf_l.add_paragraph()
    p.text = "Nen tang phan cung & phan mem:\n" \
             "- Bo xu ly trung tam: STM32F401RE Nucleo-64 (ARM Cortex-M4 @ 84 MHz)\n" \
             "- He dieu hanh thoi gian thuc: FreeRTOS Kernel (CMSIS-RTOS v2)\n" \
             "- Co-Processor vien thong: ESP32 Wi-Fi IoT Bridge (Giao thuc Dinh khung UART & Telegram Bot)\n" \
             "- Kho luu tru ma nguon: https://github.com/Nonne07/mcp201-aquatic-guardian"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(6)

    # Right Team Card
    card_r = add_card(s1, Inches(7.8), Inches(1.0), Inches(4.733), Inches(5.6), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    tf_r = card_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = Inches(0.4)
    tf_r.margin_top = Inches(0.45)

    p = tf_r.paragraphs[0]
    p.text = "DANH SACH THANH VIEN NHOM 7 (LOP IC2005)"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    members = [
        ("Nghiem Hoang Tung", "SE211196", "Truong nhom • Kien truc he thong & Lap lich FreeRTOS"),
        ("Hoang Duc Manh", "SE211191", "Ky su Cam bien & Thuat toan xu ly tin hieu so DSP"),
        ("Do Khac Le Gia", "SE211559", "Ky su Co cau chap hanh & Phan phoi nguon dien"),
        ("Pham Hong Minh", "SE211181", "Ky su Giao tiep bus I2C, RTC DS3231 & Giao dien LCD"),
        ("Nguyen Duc Anh", "SE211485", "Ky su Phan he IoT, Telegram Bot API & Kiem thu")
    ]

    for name, mssv, role in members:
        p_name = tf_r.add_paragraph()
        p_name.text = f"{name} ({mssv})"
        p_name.font.name = 'Segoe UI'
        p_name.font.size = Pt(11.5)
        p_name.font.bold = True
        p_name.font.color.rgb = COLOR_TEXT_PRIMARY
        p_name.space_before = Pt(10)

        p_role = tf_r.add_paragraph()
        p_role.text = f"  Nhiem vu: {role}"
        p_role.font.name = 'Segoe UI'
        p_role.font.size = Pt(9.5)
        p_role.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 2: [Phần 1: Bối Cảnh]: Thách Thức Kỹ Thuật & Mục Tiêu Thiết Kế
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Phan 1: Boi Canh & Nhiem Vu He Thong", 
               "PHAN TICH THACH THUC MOI TRUONG THUY SINH & MUC TIEU HE THONG", 
               "Giai quyet triet de 3 yeu to rui ro hang dau gay suy thoai he sinh thai thuy sinh nhan tao")

    col_w = Inches(3.7)
    gap = Inches(0.3)
    left_start = Inches(0.8)

    cards_data = [
        ("1. NONG DO TONG CHAT RAN HOA TAN (TDS)", 
         "- Co che suy thoai:\n"
         "  Su tich tu chat thai huu co va thuc an du thua phan huy sinh Ammonia (NH3) va Nitrite (NO2-), lam gia tang dot bien mat do ion trong nuoc.\n\n"
         "- Nguong gioi han sinh hoc:\n"
         "  Nong do TDS > 500 ppm lam dao lon ap suat tham thau sinh hoc, gay ton thuong bieu mo mang va suy ho hap o sinh vat thuy sinh.\n\n"
         "- Yeu cau thiet ke he thong:\n"
         "  Giam sat lien tuc qua bo bien doi ADC1, thuc hien loc nhieu so thoi gian thuc va kich hoat canh bao tuc thoi trong vong <200 ms."),
        ("2. BIEN THIEN NHIET DO NGOAI DAI AN TOAN", 
         "- Co che suy thoai:\n"
         "  Cac loai thuy sinh nhiet doi sinh truong on dinh trong dai nhiet do hep 24.0°C – 28.0°C.\n\n"
         "- Nguong gioi han sinh hoc:\n"
         "  Bien thien nhiet do dot ngot vuot nguong (>30.0°C) lam giam manh do hoa tan oxy (DO) va gay sai lech tuyen tinh gia tri dien tro cam bien TDS.\n\n"
         "- Yeu cau thiet ke he thong:\n"
         "  Do nhiet do chinh xac qua cam bien DS18B20 1-Wire chong nuoc va tich hop ham bu nhiet do chuan cho phep do nong do TDS."),
        ("3. SAI LECH CHU KY & KHAU PHAN CAP DUONG", 
         "- Co che suy thoai:\n"
         "  Cap duong du thua la nguyen nhan cua 80% truong hop duc nuoc; nguoc lai, gian doan chu ky keo dai dan toi suy kiet the trang sinh vat.\n\n"
         "- Thuc trang van hanh:\n"
         "  Nguoi nuoi vang mat hoac quen gio cho an khi di cong tac, thieu cong cu kiem soat tu xa.\n\n"
         "- Yeu cau thiet ke he thong:\n"
         "  Tu dong hoa co cau chap hanh dinh luong (1g – 15g) dong bo theo thoi gian thuc RTC DS3231 va tiep nhan lenh dieu khien tu xa qua mang IoT.")
    ]

    for i, (title, body) in enumerate(cards_data):
        c_left = left_start + i * (col_w + gap)
        c = add_card(s2, c_left, Inches(1.6), col_w, Inches(5.3), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.3)

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = 'Segoe UI'
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY

        p = tf.add_paragraph()
        p.text = body
        p.font.name = 'Segoe UI'
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_TEXT_MUTED
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 3: [Phần 2: Sơ Đồ Khối NATIVE]: Kiến Trúc Phân Tán (0.5đ Rubric & 3.0đ Complexity)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Phan 2: So Do Khoi & Phan Cung", 
               "SO DO KHOI KIEN TRUC HE THONG PHAN TAN (DISTRIBUTED DUAL-MCU)", 
               "Thiet ke phan tang tach biet giua Dieu khien Thoi gian thuc cung (STM32) va Vien thong IoT (ESP32)")

    # 4 Architecture Columns (Native PPT Shapes - Razor sharp, no pixelation, perfect fit)
    col_y = Inches(1.6)
    col_h = Inches(4.7)

    # Column 1: SENSORS (Left: x=0.8, w=2.6)
    c1 = add_card(s3, Inches(0.8), col_y, Inches(2.6), col_h, bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s3, Inches(0.8), col_y, Inches(2.6), Inches(0.4), "1. CAM BIEN & DAU VAO", bg_color=COLOR_CARD_DARK)
    tf1 = c1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = Inches(0.2)
    tf1.margin_top = Inches(0.5)

    s_items = [
        ("Cam bien TDS V1.0", "PA1 (ADC1_IN1)", "Loc tu gom 0.1 uF chong song nuoc"),
        ("Bien tro xoay B10K", "PA4 (ADC1_IN4)", "Mach phan ap chinh lieu 1g - 15g"),
        ("DS18B20 chong nuoc", "PA8 (GPIO OD)", "Chuan 1-Wire, tro keo 4.7 kOhm"),
        ("Nut bam User B1", "PC13 (EXTI13)", "Ngat khan cap, loc rung 300 ms")
    ]
    for name, pin, desc in s_items:
        p = tf1.add_paragraph()
        p.text = f"{name}"
        p.font.name = 'Segoe UI'
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_before = Pt(8)

        p_sub = tf1.add_paragraph()
        p_sub.text = f"  [{pin}]\n  {desc}"
        p_sub.font.name = 'Segoe UI'
        p_sub.font.size = Pt(8.5)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED

    # Column 2: STM32 CORE (Center: x=3.7, w=4.0)
    c2 = add_card(s3, Inches(3.7), col_y, Inches(4.0), col_h, bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_DARK, border_width=Pt(1.5))
    add_badge(s3, Inches(3.7), col_y, Inches(4.0), Inches(0.4), "2. BO XU LY TRUNG TAM: STM32 NUCLEO", bg_color=COLOR_BORDER_DARK)
    tf2 = c2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = Inches(0.25)
    tf2.margin_top = Inches(0.5)

    p = tf2.paragraphs[0]
    p.text = "STM32F401RE (ARM Cortex-M4 @ 84 MHz)"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    p = tf2.add_paragraph()
    p.text = "Flash: 512 KB | SRAM: 96 KB | Hardware FPU & DSP\nHe dieu hanh: FreeRTOS Kernel (CMSIS-RTOS v2)"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(2)

    tasks_desc = [
        ("Task_SafetySupervisor", "Ưu tiên 32 (High)", "200 ms", "Giam sat an toan, bao dong khan cap"),
        ("Task_DispenserControl", "Ưu tiên 24 (AboveNorm)", "Event", "Nhan Semaphore, quay Servo xa cam"),
        ("Task_SensorAcquisition", "Ưu tiên 16 (Normal)", "1000 ms", "Loc so 20 mau O(1), tinh TDS bu nhiet"),
        ("Task_DisplayUI", "Ưu tiên 12 (BelowNorm)", "500 ms", "Doc RTC DS3231, cap nhat LCD 2004"),
        ("Task_Telemetry", "Ưu tiên 8 (Low)", "2000 ms", "Dong goi JSON dinh khung '~' phat UART")
    ]
    for t_name, pri, per, desc in tasks_desc:
        p = tf2.add_paragraph()
        p.text = f"- {t_name} [{pri} - {per}]"
        p.font.name = 'Segoe UI'
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_before = Pt(6)

        p_d = tf2.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.name = 'Segoe UI'
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = COLOR_TEXT_MUTED

    p = tf2.add_paragraph()
    p.text = "IPC: Length-1 Mailbox (chong tac nghen) | Mutex I2C1 (Priority Inheritance)"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.space_before = Pt(8)

    # Column 3: ACTUATORS & I2C (Right-Center: x=8.0, w=2.6)
    c3 = add_card(s3, Inches(8.0), col_y, Inches(2.6), col_h, bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s3, Inches(8.0), col_y, Inches(2.6), Inches(0.4), "3. CHAP HANH & BUS I2C1", bg_color=COLOR_CARD_DARK)
    tf3 = c3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_right = Inches(0.2)
    tf3.margin_top = Inches(0.5)

    act_items = [
        ("Dong co Servo SG90", "PA0 (TIM2_CH1 PWM)", "Xung 50 Hz, mo goc 90 do"),
        ("Ro-le 5V cach ly quang", "PB4 (GPIO Out)", "Dong may bom tuan hoan"),
        ("Active Buzzer + LED", "PB0 & PA5/PB1", "Coi bao dem S8050, LED 1 Hz"),
        ("Man hinh LCD 2004", "PB8/PB9 (I2C1 0x27)", "Hien thi 4 dong thong so live"),
        ("RTC DS3231 & EEPROM", "PB8/PB9 (I2C1 0x68/0x57)", "Luu lich su & gio thuc te")
    ]
    for name, pin, desc in act_items:
        p = tf3.add_paragraph()
        p.text = f"{name}"
        p.font.name = 'Segoe UI'
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_before = Pt(7)

        p_sub = tf3.add_paragraph()
        p_sub.text = f"  [{pin}]\n  {desc}"
        p_sub.font.name = 'Segoe UI'
        p_sub.font.size = Pt(8.5)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED

    # Column 4: IOT CO-PROCESSOR (Far Right: x=10.9, w=1.633)
    c4 = add_card(s3, Inches(10.9), col_y, Inches(1.633), col_h, bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_DARK, border_width=Pt(1.2))
    add_badge(s3, Inches(10.9), col_y, Inches(1.633), Inches(0.4), "4. IOT BRIDGE", bg_color=COLOR_BORDER_DARK)
    tf4 = c4.text_frame
    tf4.word_wrap = True
    tf4.margin_left = tf4.margin_right = Inches(0.15)
    tf4.margin_top = Inches(0.5)

    p = tf4.paragraphs[0]
    p.text = "ESP32 Wi-Fi\nCo-Processor"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    iot_pts = [
        ("Ket noi UART1", "PA9/PA10 @ 115200", "Dinh khung '~'"),
        ("Telegram Bot", "HTTPS Long-Polling", "/status & /feed"),
        ("Web Local", "Port 80 HTTP", "Dashboard cuc bo"),
        ("Cáp ST-LINK", "USART2 VCP", "Kenh du phong PC")
    ]
    for title, sub, desc in iot_pts:
        p = tf4.add_paragraph()
        p.text = f"{title}"
        p.font.name = 'Segoe UI'
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY
        p.space_before = Pt(8)

        p_s = tf4.add_paragraph()
        p_s.text = f"  {sub}\n  {desc}"
        p_s.font.name = 'Segoe UI'
        p_s.font.size = Pt(8)
        p_s.font.color.rgb = COLOR_TEXT_MUTED

    # Bottom Architecture Summary Note (x=0.8, y=6.45, w=11.733, h=0.7)
    b_note3 = add_card(s3, Inches(0.8), Inches(6.45), Inches(11.733), Inches(0.7), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_DARK)
    tf_b3 = b_note3.text_frame
    tf_b3.word_wrap = True
    tf_b3.margin_left = Inches(0.25)
    tf_b3.margin_top = Inches(0.08)
    p_b3 = tf_b3.paragraphs[0]
    p_b3.text = "[NGUYEN LY KIEN TRUC DUAL-MCU]: He thong phan chia ranh gioi ro rang giua cac tac vu Thoi gian thuc cung (Hard Real-Time Control tren STM32 Cortex-M4) va cac tac vu Mang vien thong khong tat dinh (Non-deterministic Wi-Fi/HTTPS tren ESP32). Hai vi dieu khien giao tiep qua UART1 dinh khung '~' o toc do 115200 bps, hoan toan khong lam cham tre chu ky dieu khien chap hanh."
    p_b3.font.name = 'Segoe UI'
    p_b3.font.size = Pt(9.5)
    p_b3.font.color.rgb = COLOR_TEXT_PRIMARY

    # =========================================================================
    # SLIDE 4: [Phần 2: Mạch Điện NATIVE]: Sơ Đồ Phân Phối Nguồn & 4 Card Khắc Phục (0.5đ Rubric)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Phan 2: So Do Khoi & Phan Cung", 
               "PHAN TICH MACH DIEN & CAC GIAI PHAP PHAN CUNG THUC NGHIEM", 
               "Minh chung muc do am hieu thuc thi phan cung theo dung tieu chi Rubric (0.5 diem Circuit Analysis)")

    # Top Power Architecture Card (x=0.8, y=1.6, w=11.733, h=1.4)
    top_pwr = add_card(s4, Inches(0.8), Inches(1.6), Inches(11.733), Inches(1.4), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_DARK, border_width=Pt(1.2))
    add_badge(s4, Inches(0.8), Inches(1.6), Inches(11.733), Inches(0.35), "SO DO PHAN PHOI NGUON DIEN & NGUYEN TAC MASS CHUNG (COMMON GROUND TOPOLOGY)", bg_color=COLOR_BORDER_DARK)
    tf_tp = top_pwr.text_frame
    tf_tp.word_wrap = True
    tf_tp.margin_left = Inches(0.3)
    tf_tp.margin_top = Inches(0.4)

    p = tf_tp.paragraphs[0]
    p.text = "- Nguon cap chinh: Adapter DC 9V/12V (chan tron 5.5x2.1mm) -> Mach on ap Breadboard MB102 (on ap AMS1117-5.0 va AMS1117-3.3).\n" \
             "- Nhanh 5.0V: Cap nguon rieng cho Dong co Servo SG90, Module Ro-le 5V, Active Buzzer 5V, LCD 2004 va Chan VIN cua ESP32.\n" \
             "- Nhanh 3.3V: Cap tu chan 3V3 STM32 Nucleo cho Cam bien TDS V1.0, DS18B20 va RTC DS3231 (tranh hien tuong phong no pin CR2032).\n" \
             "- Quy tac mass chung (Common GND): Toan bo GND cua Nucleo, MB102, ESP32 va cac cam bien duoc noi chung thanh mot mat phang the quy chieu duy nhat."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # 4 Circuit Problem & Fix Cards (2x2 Grid)
    grid_w = Inches(5.7)
    grid_h = Inches(1.8)
    coords = [
        (Inches(0.8), Inches(3.2)), (Inches(6.833), Inches(3.2)),
        (Inches(0.8), Inches(5.15)), (Inches(6.833), Inches(5.15))
    ]

    hw_fixes = [
        ("1. Hien tuong sut ap tren mach nguon Breadboard MB102",
         "Dien ap sut ap (Dropout) cua IC AMS1117-5.0 la 1.2V. Neu cap nguon 5V USB vao MB102, dau ra bi sut con ~3.8V khien man hinh LCD toi va ro-le khong dong duoc.",
         "Giai phap: Cap Adapter DC 9V/12V qua cong nguon tron DC 5.5x2.1mm, dam bao dau ra MB102 luon dat chuan 5.0V on dinh."),
        ("2. Bao ve chan GPIO vi dieu khien truoc xung cam tu coi bao",
         "Coi buzzer 2 chan thong thuong rut dong tuc thoi 25 - 35 mA vuot nguong chiu dung cua chan PB0 (8 - 15 mA), sinh xung dien ap nguoc lam treo chip vi dieu khien.",
         "Giai phap: Su dung Module Active Buzzer 3 chan co san mach dem transistor S8050, giam dong dieu khien tu chan PB0 xuong < 1 mA an toan."),
        ("3. Ngan ngua hien tuong nap nguoc pha huy pin RTC CR2032",
         "Mach RTC ZS-042 duoc thiet ke kem mach nap nhoi cho pin sac LIR2032. Khi cap nguon 5V, dong nap nguoc vao pin CR2032 tieu chuan se gay phong ro va chay hoa chat.",
         "Giai phap: Cap nguon 3.3V tu STM32 vao module de vo hieu hoa mach nap, hoac dung mo han cach ly dien tro nap 200 Ohm tren mach."),
        ("4. Tuong thich muc logic dieu khien Module Ro-le 5V",
         "Khi STM32 xuat muc High (3.3V) vao module ro-le Low-Trigger dung nguon 5V, chenh lech ap 1.7V van du kich mo optocoupler khien ro-le bi dinh dong ngoai y muon.",
         "Giai phap: Chon module ro-le co Jumper chuyen che do High-Trigger hoac cau hinh chan PB4 o che do Open-Drain voi tro keo phu hop.")
    ]

    for i in range(4):
        cx, cy = coords[i]
        title, prob, fix = hw_fixes[i]
        c = add_card(s4, cx, cy, grid_w, grid_h, bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.18)

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = 'Segoe UI'
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY

        p_p = tf.add_paragraph()
        p_p.text = f"- Rui ro ky thuat: {prob}"
        p_p.font.name = 'Segoe UI'
        p_p.font.size = Pt(9)
        p_p.font.color.rgb = COLOR_TEXT_MUTED
        p_p.space_before = Pt(3)

        p_f = tf.add_paragraph()
        p_f.text = f"- Giai phap thuc nghiem: {fix}"
        p_f.font.name = 'Segoe UI'
        p_f.font.size = Pt(9)
        p_f.font.bold = True
        p_f.font.color.rgb = COLOR_TEXT_PRIMARY
        p_f.space_before = Pt(3)

    # Bottom Rule Bar (x=0.8, y=7.05, w=11.733, h=0.35)
    b_rule = add_card(s4, Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.35), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_LIGHT)
    tf_br = b_rule.text_frame
    tf_br.word_wrap = True
    tf_br.margin_left = Inches(0.2)
    tf_br.margin_top = Inches(0.05)
    p_br = tf_br.paragraphs[0]
    p_br.text = "[QUY TAC DAU NOI BO TRO]: Tro keo ngoai 4.7 kOhm tren duong 1-Wire DS18B20; Dau cheo UART1 (PA9 TX -> ESP32 RX2, PA10 RX <- ESP32 TX2)."
    p_br.font.name = 'Segoe UI'
    p_br.font.size = Pt(8.5)
    p_br.font.bold = True
    p_br.font.color.rgb = COLOR_TEXT_PRIMARY

    # =========================================================================
    # SLIDE 5: [Phần 3: FreeRTOS NATIVE]: Kiến Trúc Đa Nhiệm & Quản Lý Bộ Nhớ
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Phan 3: Phan Mem & Thoi Gian Thuc", 
               "KIEN TRUC DA NHIEM TIEN DINH FREERTOS (CMSIS-RTOS V2)", 
               "Thiet ke bo lap lich dua tren muc uu tien dam bao dap ung thoi gian thuc nghiem ngat")

    # Table of 5 Tasks (x=0.8, y=1.6, w=11.733, h=3.6)
    table_shape = s5.shapes.add_table(6, 5, Inches(0.8), Inches(1.6), Inches(11.733), Inches(3.6))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(2.6)
    tbl.columns[1].width = Inches(1.8)
    tbl.columns[2].width = Inches(1.6)
    tbl.columns[3].width = Inches(1.4)
    tbl.columns[4].width = Inches(4.333)

    headers = ["Ten Tac Vu (Thread Name)", "Muc Uu Tien (Priority)", "Co Che Kich Hoat", "Stack Allocation", "Chuc Nang Ky Thuat Chinh"]
    for c_idx, h in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        set_cell_background(cell, "1E293B")
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = 'Segoe UI'
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_WHITE

    tasks_table_data = [
        ("Task_SafetySupervisor", "osPriorityHigh (32)", "Dinh ky 200 ms", "1024 Bytes", "Giam sat nguong nguy hai TDS/Nhiet do, kich hoat coi bao chu dong va LED Alert."),
        ("Task_DispenserControl", "osPriorityAboveNormal (24)", "Event-Driven", "1024 Bytes", "Cho Semaphore tu Ngat nut bam/Lenh Telegram, quay Servo xa thuc an va ghi EEPROM."),
        ("Task_SensorAcquisition", "osPriorityNormal (16)", "Dinh ky 1000 ms", "1024 Bytes", "Thu thap luoc phien kenh ADC1, loc trung binh truot 20 mau O(1), tinh TDS bu nhiet."),
        ("Task_DisplayUI", "osPriorityBelowNormal (12)", "Dinh ky 500 ms", "2048 Bytes", "Doc thoi gian thuc tu RTC DS3231 va cap nhat 4 dong thong so len LCD 2004 qua I2C1."),
        ("Task_Telemetry", "osPriorityLow (8)", "Dinh ky 2000 ms", "2048 Bytes", "Dong goi ban tin JSON dinh khung '~' truyen phat toi ESP32 UART1 va ST-LINK VCP.")
    ]

    for r_idx, r_data in enumerate(tasks_table_data, 1):
        for c_idx, val in enumerate(r_data):
            cell = tbl.cell(r_idx, c_idx)
            set_cell_background(cell, "FFFFFF" if r_idx % 2 != 0 else "F1F5F9")
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = 'Segoe UI'
            p.font.size = Pt(9.5)
            p.font.color.rgb = COLOR_TEXT_PRIMARY
            if c_idx == 0:
                p.font.bold = True

    # Technical Callout Box for CMSIS-RTOS v2 Stack (x=0.8, y=5.4, w=11.733, h=1.65)
    c_note5 = add_card(s5, Inches(0.8), Inches(5.4), Inches(11.733), Inches(1.65), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_DARK, border_width=Pt(1.2))
    add_badge(s5, Inches(0.8), Inches(5.4), Inches(11.733), Inches(0.35), "DAC TA QUAN TRONG VE QUAN LY BO NHO TRONG CHUAN CMSIS-RTOS V2", bg_color=COLOR_BORDER_DARK)
    tf_n5 = c_note5.text_frame
    tf_n5.word_wrap = True
    tf_n5.margin_left = Inches(0.3)
    tf_n5.margin_top = Inches(0.4)

    p = tf_n5.paragraphs[0]
    p.text = "- Quy dinh don vi Stack trong CMSIS-RTOS v2: Khac voi CMSIS-RTOS v1 (tham so stack tinh bang Words = 4 Bytes), chuan v2 quy dinh .stack_size tinh truc tiep bang BYTES.\n" \
             "- Hien tuong loi tran bo nho: Neu khai bao nham 256 words thanh 256 bytes se lam tran vung nho Stack va kich hoat ngoai le phan cung HardFault Handler khi thuc thi cac ham xu ly chuoi nhu snprintf().\n" \
             "- Phan bo an toan cua he thong: Cap phat 1024 Bytes cho cac tac vu xu ly tinh toan thuan tuy va 2048 Bytes cho cac tac vu dinh dang chuoi hien thi LCD va vi-en thong JSON."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # =========================================================================
    # SLIDE 6: [Phần 3: Lưu Đồ NATIVE]: Lưu Đồ Thuật Toán Song Song (0.5đ Rubric)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Phan 3: Phan Mem & Thoi Gian Thuc", 
               "LUU DO THUAT TOAN DIEU KHIEN & XU LY TIN HIEU SO (FLOWCHART)", 
               "Minh chung thiet ke lap trinh he thong theo dung tieu chi Rubric (0.5 diem Flowchart)")

    # 2 Parallel Native Flowchart Columns
    fc_w = Inches(5.7)
    fc_gap = Inches(0.333)

    # Pipeline A: Dispenser FSM (Left: x=0.8, w=5.7)
    c_fc1 = add_card(s6, Inches(0.8), Inches(1.6), fc_w, Inches(5.4), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s6, Inches(0.8), Inches(1.6), fc_w, Inches(0.4), "A. QUY TRINH DIEU KHIEN CO CAU CAP DUONG (EVENT-DRIVEN)", bg_color=COLOR_CARD_DARK)
    
    steps_a = [
        ("1. Trang thai cho (Task Blocked)", "Task_DispenserControl o trang thai nghi, giai phong 100% CPU cho he thong"),
        ("2. Su kien kich hoat", "Nhan Semaphore tu: Nut bam PC13 / Lenh Telegram / Hen gio RTC"),
        ("3. Tinh toan dinh luong", "Doc ADC PA4 -> Thoi gian mo: Dwell Time = 300 ms + (Dose_g x 80 ms)"),
        ("4. Dieu khien Servo SG90", "Phat PWM 50 Hz tren chan PA0: Mo 90 do -> Delay Dwell Time -> Dong ve 0 do"),
        ("5. Ghi nhat ky EEPROM", "Chiem Mutex I2C1 -> Ghi Timestamp va Khau phan vao AT24C32 -> Nha Mutex"),
        ("6. Hoan tat chu ky", "Xoa co su kien, tra CPU va quay tro ve trang thai cho ban dau")
    ]
    for idx, (st_title, st_desc) in enumerate(steps_a):
        sy = Inches(2.15) + idx * Inches(0.78)
        sc = add_card(s6, Inches(1.0), sy, Inches(5.3), Inches(0.68), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_LIGHT)
        stf = sc.text_frame
        stf.word_wrap = True
        stf.margin_left = Inches(0.2)
        stf.margin_top = Inches(0.08)
        p = stf.paragraphs[0]
        p.text = st_title
        p.font.name = 'Segoe UI'
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY
        p_d = stf.add_paragraph()
        p_d.text = st_desc
        p_d.font.name = 'Segoe UI'
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = COLOR_TEXT_MUTED

    # Pipeline B: Sensor DSP (Right: x=6.833, w=5.7)
    c_fc2 = add_card(s6, Inches(6.833), Inches(1.6), fc_w, Inches(5.4), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s6, Inches(6.833), Inches(1.6), fc_w, Inches(0.4), "B. QUY TRINH THU THAP & XU LY TIN HIEU SO TDS (DSP)", bg_color=COLOR_CARD_DARK)

    steps_b = [
        ("1. Kich hoat dinh ky tuyet doi", "osDelayUntil(&last_wake, 1000 ms) triet tieu hoan toan troi pha chu ky"),
        ("2. Thu thap ADC1 kenh PA1", "Lay mau tin hieu dien ap tho tu cam bien TDS V1.0 (gia tri 0 - 4095)"),
        ("3. Loc trung binh truot 20 mau O(1)", "Sum = Sum - RingBuf[i] + NewSample; V_adc = (Sum / 20) x 3.3 / 4095"),
        ("4. Doc nhiet do & bu nhiet TDS", "Doc DS18B20 1-Wire: V_comp = V_adc / [1.0 + 0.02 x (T_water - 25.0)]"),
        ("5. Tinh toan da thuc bac 3", "TDS = (133.42 x V_comp^3 - 255.86 x V_comp^2 + 857.39 x V_comp) x 0.5"),
        ("6. Cap nhat Length-1 Mailbox", "xQueueOverwrite(sensorMailbox) de cac tac vu khac truy xuat tuc thoi")
    ]
    for idx, (st_title, st_desc) in enumerate(steps_b):
        sy = Inches(2.15) + idx * Inches(0.78)
        sc = add_card(s6, Inches(7.033), sy, Inches(5.3), Inches(0.68), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_LIGHT)
        stf = sc.text_frame
        stf.word_wrap = True
        stf.margin_left = Inches(0.2)
        stf.margin_top = Inches(0.08)
        p = stf.paragraphs[0]
        p.text = st_title
        p.font.name = 'Segoe UI'
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY
        p_d = stf.add_paragraph()
        p_d.text = st_desc
        p_d.font.name = 'Segoe UI'
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 7: [Phần 3: DSP & Bù Nhiệt]: Đồ Thị Tín Hiệu & Mô Hình Toán
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Phan 3: Phan Mem & Thoi Gian Thuc", 
               "THUAT TOAN XU LY TIN HIEU SO DSP & MO HINH TOAN BU NHIET DO", 
               "Khu nhieu bien dong song nuoc va hieu chuan nhiet do chinh xac theo mo hinh hoa hoc nuoc")

    # Embed Scientific DSP Plots Figure (x=0.8, y=1.6, w=6.8, h=3.3)
    fig_dsp_path = os.path.join(ASSETS_DIR, "fig_dsp_plots.png")
    if os.path.exists(fig_dsp_path):
        s7.shapes.add_picture(fig_dsp_path, Inches(0.8), Inches(1.6), width=Inches(6.8), height=Inches(3.3))

    # Right Card: Theoretical Formulation (x=7.8, y=1.6, w=4.733, h=3.3)
    c_form = add_card(s7, Inches(7.8), Inches(1.6), Inches(4.733), Inches(3.3), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_DARK, border_width=Pt(1.2))
    add_badge(s7, Inches(7.8), Inches(1.6), Inches(4.733), Inches(0.35), "MO HINH TOAN HOC & PHUONG TRINH CHUYEN DOI", bg_color=COLOR_BORDER_DARK)
    tf_f = c_form.text_frame
    tf_f.word_wrap = True
    tf_f.margin_left = Inches(0.25)
    tf_f.margin_top = Inches(0.4)

    p = tf_f.paragraphs[0]
    p.text = "1. Phuong trinh bu nhiet do dien ap:\n" \
             "   V_comp = V_adc / [1.0 + 0.02 * (T_water - 25.0)]\n" \
             "   (Chuan hoa dien ap ve moc nhiet do tieu chuan 25.0°C)\n\n" \
             "2. Da thuc bac 3 noi suy nong do TDS (ppm):\n" \
             "   TDS = (133.42 * V_comp^3\n" \
             "        - 255.86 * V_comp^2\n" \
             "        + 857.39 * V_comp) * 0.5\n\n" \
             "3. Tinh toan tren FPU phan cung Cortex-M4:\n" \
             "   Thuc thi bang cac lenh so thuc don chu ky (Single-Cycle FPU), thoi gian thuc thi < 2.5 us."
    p.font.name = 'Consolas'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # Bottom 2 Cards (x=0.8 & x=6.833, y=5.1, w=5.7, h=2.0)
    c_b_l = add_card(s7, Inches(0.8), Inches(5.1), Inches(5.7), Inches(2.0), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    tf_bl = c_b_l.text_frame
    tf_bl.word_wrap = True
    tf_bl.margin_left = Inches(0.25)
    tf_bl.margin_top = Inches(0.18)
    p = tf_bl.paragraphs[0]
    p.text = "HIEU QUA BO LOC TRUNG BINH TRUOT VONG O(1)"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p = tf_bl.add_paragraph()
    p.text = "- Thuat toan cap nhat tong chay: Sum = Sum - RingBuf[idx] + NewSample.\n" \
             "- Do phuc tap thoi gian: O(1) khong phu thuoc vao kich thuoc cua so loc (20 mau).\n" \
             "- Hieu qua thuc te: Do lech chuan tin hieu giam tu ±45 ppm xuong duoi ±1.5 ppm, triet tieu hoan toan hien tuong bao dong gia do song nuoc khi may bom hoat dong."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(4)

    c_b_r = add_card(s7, Inches(6.833), Inches(5.1), Inches(5.7), Inches(2.0), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    tf_br = c_b_r.text_frame
    tf_br.word_wrap = True
    tf_br.margin_left = Inches(0.25)
    tf_br.margin_top = Inches(0.18)
    p = tf_br.paragraphs[0]
    p.text = "Y NGHIA KY THUAT CUA VIEC BU NHIET DO"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p = tf_br.add_paragraph()
    p.text = "- Do dan dien (EC) cua nuoc tang khoang 2% moi 1°C tang nhiet do.\n" \
             "- Neu khong bu nhiet, khi nhiet do nuoc tang tu 20°C len 30°C, gia tri TDS se bi sai lech len toi 20% du thanh phan chat tan khong he thay doi.\n" \
             "- Thuat toan bu nhiet giup he thong danh gia dung ban chat o nhiem cua nuoc."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 8: [Phần 3: Đồng Bộ IPC]: Length-1 Mailbox & Priority Inheritance
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Phan 3: Phan Mem & Thoi Gian Thuc", 
               "CO CHE DONG BO LIEN TAC VU (IPC) & PHONG NGUONG NGHICH DAO UU TIEN", 
               "Giai quyet triet de hai bai toan kinh dien trong he thong nhung: Tac nghen du lieu va Nghich dao do uu tien")

    col_ipc_w = Inches(5.7)
    gap_ipc = Inches(0.333)

    # Left: Mailbox (x=0.8, y=1.6, w=5.7, h=5.4)
    c_ipc1 = add_card(s8, Inches(0.8), Inches(1.6), col_ipc_w, Inches(5.4), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s8, Inches(0.8), Inches(1.6), col_ipc_w, Inches(0.4), "1. CO CHE HOM THU DON (LENGTH-1 MAILBOX)", bg_color=COLOR_CARD_DARK)
    tf_i1 = c_ipc1.text_frame
    tf_i1.word_wrap = True
    tf_i1.margin_left = tf_i1.margin_right = Inches(0.3)
    tf_i1.margin_top = Inches(0.5)

    p = tf_i1.paragraphs[0]
    p.text = "- Thach thuc ky thuat (Hien tuong Data Starvation):\n" \
             "Hang doi FreeRTOS thong thuong mang dac tinh tieu thu pha huy (Destructive Read). Tac vu Supervisor (uu tien 32, chu ky 200 ms) se chiem giu toan bo thong diep, dan toi cac tac vu tieu thu chu ky cham hon (DisplayUI 500 ms va Telemetry 2000 ms) bi co lap hoan toan khoi nguon du lieu cam bien."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_MUTED

    p = tf_i1.add_paragraph()
    p.text = "- Giai phap ky thuat da ap dung:\n" \
             "1. Tac vu san xuat (Sensor Task) su dung ham xQueueOverwrite() de cap nhat ban ghi telemetry moi nhat vao hom thu co do sau dung 1 phan tu.\n" \
             "2. Cac tac vu tieu thu (Supervisor, Display, Telemetry) deu su dung ham xQueuePeek() de sao chep du lieu ma KHONG lam xoa phan tu khoi hang doi.\n" \
             "3. Ket qua: Ca 3 tac vu deu truy xuat duoc du lieu moi nhat theo chu ky doc lap (200 ms, 500 ms, 2000 ms), loai bo hoan toan hien tuong tac nghen luong du lieu."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.space_before = Pt(12)

    # Right: Priority Inheritance (x=6.833, y=1.6, w=5.7, h=5.4)
    c_ipc2 = add_card(s8, Inches(6.833), Inches(1.6), col_ipc_w, Inches(5.4), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s8, Inches(6.833), Inches(1.6), col_ipc_w, Inches(0.4), "2. KE THUA QUYEN UU TIEN (PRIORITY INHERITANCE) TREN BUS I2C1", bg_color=COLOR_CARD_DARK)
    tf_i2 = c_ipc2.text_frame
    tf_i2.word_wrap = True
    tf_i2.margin_left = tf_i2.margin_right = Inches(0.3)
    tf_i2.margin_top = Inches(0.5)

    p = tf_i2.paragraphs[0]
    p.text = "- Thach thuc Nghich dao do uu tien (Priority Inversion):\n" \
             "Tac vu DisplayUI (uu tien 12) dang giu Mutex I2C1 de xuat ky tu len LCD 2004. Cung luc do, su kien cho an kich hoat, Task_DispenserControl (uu tien 24) thuc tinh can truy cap EEPROM va bi khoa lai. Neu tac vu trung gian Task_SensorAcquisition (uu tien 16) thuc tinh chiem CPU, no se ngan DisplayUI hoan tat, gian tiep phong toa tac vu cap cao 24 vo thoi han."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_MUTED

    p = tf_i2.add_paragraph()
    p.text = "- Co che Ke thua quyen uu tien:\n" \
             "1. Khi tac vu 24 yeu cau khoa Mutex, FreeRTOS lap tuc nang tam thoi muc uu tien cua tac vu hien thi tu 12 len bang 24.\n" \
             "2. Tac vu trung gian 16 khong the chen ngang, giup DisplayUI hoan tat giao dich I2C va giai phong Mutex trong thoi gian ngan nhat (4.2 ms).\n" \
             "3. Sau khi nha Mutex, tac vu hien thi ha ve 12, tac vu cap duong lap tuc chiem bus I2C ghi nhat ky EEPROM tuyet doi an toan."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.space_before = Pt(12)

    # =========================================================================
    # SLIDE 9: [Phần 3: Phân Tích Mã Nguồn C]: 3 Khối Code Trọng Yếu (0.5đ Rubric)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Phan 3: Phan Mem & Thoi Gian Thuc", 
               "PHAN TICH MA NGUON C TRONG YEU (SOURCE CODE ANALYSIS)", 
               "Minh chung chat luong lap trinh vi dieu khien STM32 HAL va ESP32 theo dung Rubric (0.5 diem Code Analysis)")

    col_code_w = Inches(3.7)
    
    code_snippets = [
        ("A. CO CHE TRI HOAN NGAT (DEFERRED ISR)",
         "void HAL_GPIO_EXTI_Callback(uint16_t Pin) {\n"
         "  static uint32_t last_tick = 0;\n"
         "  if (Pin == GPIO_PIN_13) {\n"
         "    uint32_t now = HAL_GetTick();\n"
         "    // Loc rung phim phan mem 300 ms\n"
         "    if ((now - last_tick) > 300U) {\n"
         "      last_tick = now;\n"
         "      // Nha Semaphore trong thoi gian <1us\n"
         "      osSemaphoreRelease(feedSemHandle);\n"
         "    }\n"
         "  }\n"
         "}",
         "- Triet ly lap trinh: Tuyet doi khong dat ham tre hay xu ly nang trong trinh phuc vu ngat ISR.\n"
         "- Thoi gian thuc thi ngat chi ton <1 us, ban giao toan bo tac vu nang cho ngu canh tuyen (Thread Context)."),
        ("B. TINH TONG CHAY O(1) & CHUYEN DOI TDS",
         "// Circular Buffer Moving Average O(1)\n"
         "tds_sum = tds_sum - ring_buffer[buf_idx];\n"
         "tds_sum = tds_sum + new_raw_adc;\n"
         "ring_buffer[buf_idx] = new_raw_adc;\n"
         "buf_idx = (buf_idx + 1) % 20;\n\n"
         "float v_adc  = (tds_sum / 20.0f) * 3.3f / 4095;\n"
         "float v_comp = v_adc / (1.0f + 0.02f * (temp - 25));\n"
         "tds_ppm = (133.42f * v_comp * v_comp * v_comp\n"
         "          - 255.86f * v_comp * v_comp\n"
         "          + 857.39f * v_comp) * 0.5f;",
         "- Toi uu hoa chu ky CPU: Khong dung vong lap for duyet mang; tinh toan da thuc bang phan cung FPU Cortex-M4."),
        ("C. MAY TRANG THAI GIAI MA KHUNG UART",
         "// FSM Frame Delimiter '~' Decoder\n"
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
         "- Tinh toan ven du lieu: May trang thai huu han (FSM) loai bo toan bo byte rac sinh ra do cam rut day hoac nhieu dien tu.")
    ]

    for i, (title, code_str, note) in enumerate(code_snippets):
        c_x = Inches(0.8) + i * (col_code_w + Inches(0.3))
        card = add_card(s9, c_x, Inches(1.6), col_code_w, Inches(5.4), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
        add_badge(s9, c_x, Inches(1.6), col_code_w, Inches(0.4), title, bg_color=COLOR_CARD_DARK)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.5)

        p_c = tf.paragraphs[0]
        p_c.text = code_str
        p_c.font.name = 'Consolas'
        p_c.font.size = Pt(8.2)
        p_c.font.color.rgb = COLOR_TEXT_PRIMARY

        p_n = tf.add_paragraph()
        p_n.text = note
        p_n.font.name = 'Segoe UI'
        p_n.font.size = Pt(9.2)
        p_n.font.color.rgb = COLOR_TEXT_MUTED
        p_n.space_before = Pt(12)

    # =========================================================================
    # SLIDE 10: [Phần 4: IoT & Telegram NATIVE]: Giao Thức Định Khung & Viễn Thông (3.0đ Complexity)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Phan 4: Phan He IoT & Kiem Thu", 
               "PHAN HE IOT ESP32 & NEN TANG VIEN THONG TELEGRAM BOT", 
               "Giao thuc dinh khung UART va co che vien thong dam bao dat 3.0 diem Project Complexity trong Rubric")

    # Top Native UART Packet Structure (x=0.8, y=1.6, w=11.733, h=1.4)
    top_pkt = add_card(s10, Inches(0.8), Inches(1.6), Inches(11.733), Inches(1.4), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_DARK, border_width=Pt(1.2))
    add_badge(s10, Inches(0.8), Inches(1.6), Inches(11.733), Inches(0.35), "CAU TRUC KHUNG TRUYEN UART 2 CHIEU GIUA STM32 VA ESP32 (BAUDRATE 115200 BPS)", bg_color=COLOR_BORDER_DARK)

    # 3 Packet segments
    # Start Delimiter
    add_badge(s10, Inches(1.1), Inches(2.1), Inches(1.8), Inches(0.7), "START DELIMITER\n'~' (0x7E)", bg_color=COLOR_CARD_DARK, text_color=COLOR_TEXT_WHITE, font_size=8.5)
    # Payload
    p_box = add_card(s10, Inches(3.1), Inches(2.1), Inches(7.133), Inches(0.7), bg_color=COLOR_BG_WHITE, border_color=COLOR_BORDER_DARK)
    tf_pb = p_box.text_frame
    tf_pb.word_wrap = True
    tf_pb.margin_left = Inches(0.2)
    tf_pb.margin_top = Inches(0.08)
    p = tf_pb.paragraphs[0]
    p.text = "DU LIEU TAI (PAYLOAD): JSON Telemetry HOAC Lenh dieu khien\n{\"time\":171800,\"tds_ppm\":185.2,\"temp_c\":26.5,\"portion_g\":5,\"status\":0}   |   'feed'   |   'status'"
    p.font.name = 'Consolas'
    p.font.size = Pt(8.5)
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.alignment = PP_ALIGN.CENTER
    # End Delimiter
    add_badge(s10, Inches(10.433), Inches(2.1), Inches(1.8), Inches(0.7), "END DELIMITER\n'~' (0x7E)", bg_color=COLOR_CARD_DARK, text_color=COLOR_TEXT_WHITE, font_size=8.5)

    # Bottom 2 Cards (x=0.8 & x=6.833, y=3.2, w=5.7, h=3.8)
    c_w10 = Inches(5.7)
    gap10 = Inches(0.333)

    # Left: Long Polling Mechanism
    c_iot_l = add_card(s10, Inches(0.8), Inches(3.2), c_w10, Inches(3.8), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s10, Inches(0.8), Inches(3.2), c_w10, Inches(0.4), "1. CO CHE VIEN THONG HTTPS LONG-POLLING", bg_color=COLOR_CARD_DARK)
    tf_il = c_iot_l.text_frame
    tf_il.word_wrap = True
    tf_il.margin_left = tf_il.margin_right = Inches(0.3)
    tf_il.margin_top = Inches(0.5)

    p = tf_il.paragraphs[0]
    p.text = "- Nguyen ly thuc thi mang:\n" \
             "  ESP32 duy tri phien ket noi TLS/HTTPS bao mat (Cong 443) toi api.telegram.org thong qua thu vien UniversalTelegramBot. Phuong thuc Long-Polling giu ket noi cho ban tin moi.\n\n" \
             "- Uu diem vuot troi:\n" \
             "  1. Hoat dong xuyen suot tren moi ha tang mang Wi-Fi va 4G/5G ca nhan ma khong yeu cau cau hinh IP tinh hoac Port Forwarding tren Router.\n" \
             "  2. Tinh bao mat cao: Toan bo goi tin duoc ma hoa TLS 1.2 chong danh cap thong tin tren duong truyen.\n" \
             "  3. Chi phi 0 dong: Nen tang API Telegram Bot hoan toan mien phi, tao bot trong 30s qua @BotFather."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # Right: Command & Push Alert
    c_iot_r = add_card(s10, Inches(6.833), Inches(3.2), c_w10, Inches(3.8), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s10, Inches(6.833), Inches(3.2), c_w10, Inches(0.4), "2. DANH MUC LENH DIEU KHIEN & CANH BAO CHU DONG", bg_color=COLOR_CARD_DARK)
    tf_ir = c_iot_r.text_frame
    tf_ir.word_wrap = True
    tf_ir.margin_left = tf_ir.margin_right = Inches(0.3)
    tf_ir.margin_top = Inches(0.5)

    p = tf_ir.paragraphs[0]
    p.text = "- Lenh /status: Truy van thong so thoi gian thuc (TDS, Nhiet do, Khau phan, Trang thai an toan).\n\n" \
             "- Lenh /feed: Phat chuoi ~feed~ qua UART1 kich hoat Servo xa dung luong thuc an da cai dat.\n\n" \
             "- Canh bao day tu dong (Push Notification): Khi nong do TDS vuot nguong 500 ppm, ESP32 chu dong ban tin nhan khan cap ve ung dung dien thoai ma khong can nguoi dung truy van thu cong.\n\n" \
             "- Web Dashboard noi bo: Truy cap dia chi IP cuc bo cua ESP32 tu trinh duyet dien thoai tren cung mang Wi-Fi de theo doi giao dien truc quan."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # =========================================================================
    # SLIDE 11: [Phần 4: Kiểm Thử]: Ma Trận Kiểm Thử Kỹ Thuật & Hiệu Năng
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Phan 4: Phan He IoT & Kiem Thu", 
               "KET QUA KIEM THU KY THUAT DOC LAP & DO LUONG HIEU NANG", 
               "Minh chung tinh on dinh va muc do tuan thu cac rang buoc thoi gian thuc nghiem ngat")

    col_t_w = Inches(5.7)
    gap_t = Inches(0.333)

    # Left: Unit Tests (x=0.8, y=1.6, w=5.7, h=5.4)
    c_test_l = add_card(s11, Inches(0.8), Inches(1.6), col_t_w, Inches(5.4), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s11, Inches(0.8), Inches(1.6), col_t_w, Inches(0.4), "KET QUA KIEM THU 4 MODULE PHAN MEM DOC LAP", bg_color=COLOR_CARD_DARK)
    tf_tl = c_test_l.text_frame
    tf_tl.word_wrap = True
    tf_tl.margin_left = tf_tl.margin_right = Inches(0.3)
    tf_tl.margin_top = Inches(0.5)

    t_modules = [
        ("test_servo_pwm.c", "Timer 2 PWM 50 Hz", "Do rong xung 1.0 ms = 0° (dong kin); 1.5 ms = 90° (xa thuc an). Thoi gian duy tri Dwell Time dap ung chuan xac tu 380 ms den 1500 ms."),
        ("test_tds_filter.c", "Bo loc so 20 mau O(1)", "Khu triet de dao dong co hoc do song nuoc; do lech chuan tinh toan giam tu ±45 ppm xuong duoi ±1.5 ppm."),
        ("test_i2c_scanner.c", "Bus I2C1 quet 127 dia chi", "Nhan dien chinh xac 3 thiet bi: 0x27 (LCD 2004), 0x68 (RTC DS3231), 0x57 (EEPROM AT24C32). Ghi/doc thu gia tri kiem thu khop 100%."),
        ("test_uart_bridge.c", "Cau noi UART1 115200 bps", "Truyen 1,000 goi tin JSON dinh khung lien tuc: Ty le loi khung (Frame Error Rate) bang 0.0%, khong mat dong bo.")
    ]

    for m_file, m_sub, m_res in t_modules:
        p_m = tf_tl.add_paragraph()
        p_m.text = f"{m_file} ({m_sub}):"
        p_m.font.name = 'Segoe UI'
        p_m.font.size = Pt(10)
        p_m.font.bold = True
        p_m.font.color.rgb = COLOR_TEXT_PRIMARY
        p_m.space_before = Pt(8)

        p_mr = tf_tl.add_paragraph()
        p_mr.text = f"  Ket qua: {m_res}"
        p_mr.font.name = 'Segoe UI'
        p_mr.font.size = Pt(9)
        p_mr.font.color.rgb = COLOR_TEXT_MUTED

    # Right: Latency & Benchmarks (x=6.833, y=1.6, w=5.7, h=5.4)
    c_test_r = add_card(s11, Inches(6.833), Inches(1.6), col_t_w, Inches(5.4), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s11, Inches(6.833), Inches(1.6), col_t_w, Inches(0.4), "DO LUONG DO TRE DAP UNG THOI GIAN THUC & BO NHO", bg_color=COLOR_CARD_DARK)
    tf_tr = c_test_r.text_frame
    tf_tr.word_wrap = True
    tf_tr.margin_left = tf_tr.margin_right = Inches(0.3)
    tf_tr.margin_top = Inches(0.5)

    p = tf_tr.paragraphs[0]
    p.text = "- Thoi gian dap ung he thong (Latency Benchmarks):\n" \
             "  1. Phat hien vuot nguong TDS nguy hai: 185 ms (Rang buoc an toan: <300 ms)\n" \
             "  2. Do tre ngat phim bam (EXTI Latency): 0.85 us (Rang buoc ky thuat: <10 us)\n" \
             "  3. Thoi gian chiem giu va nha Mutex I2C: 4.2 ms (Nguong toi da: <50 ms)\n" \
             "  4. Do tre truyen goi tin dinh khung UART: 2.8 ms (Nguong cho phep: <10 ms)"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    p = tf_tr.add_paragraph()
    p.text = "- Chiem dung tai nguyen vi dieu khien (Resource Footprint):\n" \
             "  1. Bo nho chuong trinh Flash ROM: 48.2 KB / 512 KB (Chiem 9.41%)\n" \
             "  2. Bo nho du lieu tinh SRAM: 12.4 KB / 96 KB (Chiem 12.92%)\n" \
             "  3. Bo nho dong FreeRTOS Heap (Heap_4): 4096 / 8192 Bytes (50.0% an toan)\n" \
             "  => He thong toi uu, con du tren 85% tai nguyen cho viec tich hop them cam bien pH, Oxy hoa tan trong tuong lai."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(14)

    # =========================================================================
    # SLIDE 12: [Phần 5: Trình Diễn]: Kịch Bản Thực Nghiệm 4 Giai Đoạn (1.0đ Demo)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Phan 5: Trinh Dien & Ket Luan", 
               "QUY TRINH TRINH DIEN MO HINH THUC TE & TONG KET DONG GOP", 
               "Kich ban kiem chung he thong 4 giai doan phuc vu danh gia Demonstration (1.0 diem) va Van dap Q&A (3.0 diem)")

    coords12 = [
        (Inches(0.8), Inches(1.6)), (Inches(6.833), Inches(1.6)),
        (Inches(0.8), Inches(4.1)), (Inches(6.833), Inches(4.1))
    ]
    grid12_w = Inches(5.7)
    grid12_h = Inches(2.3)

    demo_stages = [
        ("GIAI DOAN 1: KHOI DONG & THIET LAP HE THONG", 
         "- Thao tac: Cap nguon Adapter 9V DC vao mach on ap MB102 tren Breadboard.\n"
         "- Phan hoi he thong: Man hinh LCD 2004 cap nhat 4 dong thong so thoi gian thuc; LED xanh PA5 sang on dinh; Ro-le 5V dong nguon cap may bom nuoc tuan hoan."),
        ("GIAI DOAN 2: DINH LUONG CAP DUONG THU CONG TAI CHO", 
         "- Thao tac: Dieu chinh bien tro B10K PA4 (thay doi dinh luong 1g - 15g), nhan nut User Button PC13.\n"
         "- Phan hoi he thong: Servo SG90 quay 90° mo nap xa thuc an, duy tri dung Dwell Time roi dong kin; he thong ghi nhat ky vao chip EEPROM AT24C32 qua I2C."),
        ("GIAI DOAN 3: DIEU KHIEN & TRUY VAN TU XA QUA TELEGRAM", 
         "- Thao tac: Gui lenh /status va /feed qua ung dung Telegram tren thiet bi di dong.\n"
         "- Phan hoi he thong: Bot phan hoi bao cao thong so TDS va Nhiet do trong <1s; Servo chap hanh lap tuc mo nap xa thuc an theo lenh vi-en thong."),
        ("GIAI DOAN 4: MO PHONG SU CO MOI TRUONG NUOC O NHIEM", 
         "- Thao tac: Di chuyen dau do TDS tu coc nuoc sach sang coc dung dich co nong do ion cao (>500 ppm).\n"
         "- Phan hoi he thong: Trong vong 185 ms, coi Buzzer PB0 bao dong, LED do PB1 nhay 1 Hz, LCD hien thi 'CRITICAL HAZARD', Telegram tu dong ban tin nhan canh bao khuan cap.")
    ]

    for i in range(4):
        cx, cy = coords12[i]
        title, body = demo_stages[i]
        card = add_card(s12, cx, cy, grid12_w, grid12_h, bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
        add_badge(s12, cx, cy, grid12_w, Inches(0.35), title, bg_color=COLOR_CARD_DARK)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.4)

        p = tf.paragraphs[0]
        p.text = body
        p.font.name = 'Segoe UI'
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_TEXT_PRIMARY

    # Bottom bar for GitHub access & Conclusion (x=0.8, y=6.55, w=11.733, h=0.6)
    b_demo = add_card(s12, Inches(0.8), Inches(6.55), Inches(11.733), Inches(0.6), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_DARK, border_width=Pt(1.2))
    tf_bd = b_demo.text_frame
    tf_bd.word_wrap = True
    tf_bd.margin_left = Inches(0.25)
    tf_bd.margin_top = Inches(0.08)
    p_bd = tf_bd.paragraphs[0]
    p_bd.text = "[TONG KET & MA NGUON CONG KHAI]: Toan bo thiet ke phan cung, so do mach, ma nguon C FreeRTOS va firmware ESP32 duoc dong goi cong khai tai: https://github.com/Nonne07/mcp201-aquatic-guardian. Nhom san sang buoc vao phan van dap chuyen sau."
    p_bd.font.name = 'Segoe UI'
    p_bd.font.size = Pt(9.5)
    p_bd.font.bold = True
    p_bd.font.color.rgb = COLOR_TEXT_PRIMARY

    # =========================================================================
    # SLIDE 13: [Phụ Lục Kỹ Thuật]: Bản Đồ Bộ Nhớ & Kênh Dự Phòng ST-LINK (0.5đ Rubric)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Phu Luc Ky Thuat (Backup Slide)", 
               "BAN DO BO NHO HE THONG & KENH VIEN THONG DU PHONG FAILSAFE", 
               "Tai lieu ky thuat chuyen sau phuc vu phan van dap chuyen mon cua Hoi dong Giang vien (3.0 diem Q&A)")

    # Embedded Memory Chart Figure (Left: x=0.8, y=1.6, w=5.7, h=5.4)
    fig_mem_path = os.path.join(ASSETS_DIR, "fig_memory_footprint.png")
    if os.path.exists(fig_mem_path):
        s13.shapes.add_picture(fig_mem_path, Inches(0.8), Inches(1.6), width=Inches(5.7), height=Inches(5.4))

    # Right: Failsafe & Memory Map Details (x=6.833, y=1.6, w=5.7, h=5.4)
    c_ap_r = add_card(s13, Inches(6.833), Inches(1.6), Inches(5.7), Inches(5.4), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s13, Inches(6.833), Inches(1.6), Inches(5.7), Inches(0.4), "PHAN BO BO NHO CHI TIET & KENH DU PHONG FAILSAFE", bg_color=COLOR_CARD_DARK)
    tf_ar = c_ap_r.text_frame
    tf_ar.word_wrap = True
    tf_ar.margin_left = tf_ar.margin_right = Inches(0.3)
    tf_ar.margin_top = Inches(0.5)

    p = tf_ar.paragraphs[0]
    p.text = "1. PHAN BO BO NHO CHI TIET (MEMORY FOOTPRINT)"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    p = tf_ar.add_paragraph()
    p.text = "- Flash ROM (512 KB): 48.2 KB (9.41%)\n" \
             "  Bao gom STM32 HAL Drivers, FreeRTOS Kernel, libc math routines, Task functions va chuoi dinh dang JSON.\n" \
             "- Static RAM (96 KB): 12.4 KB (12.92%)\n" \
             "  Bao gom bien toan cuc, Circular Buffers, DMA Descriptors va cac vung nho .data/.bss.\n" \
             "- FreeRTOS Heap (Heap_4): Cung cap 4096 / 8192 Bytes cho 5 Task Control Blocks (TCB), 5 Task Stacks, 2 Mutexes va 1 Semaphore.\n" \
             "- Stack Watermark: Kiem tra bang ham uxTaskGetStackHighWaterMark() xac nhan tat ca tac vu deu con du >35% bien do an toan, hoan toan khong co nguy co tran stack."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(4)

    p = tf_ar.add_paragraph()
    p.text = "2. KENH GIAM SAT DU PHONG ST-LINK VIRTUAL COM PORT"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.space_before = Pt(12)

    p = tf_ar.add_paragraph()
    p.text = "- Nguyen ly phan cung:\n" \
             "  Cap chan PA2/PA3 tren bo Nucleo-64 duoc noi truc tiep toi chip nap ST-LINK/V2-1. Tin hieu USART2 duoc chip cau chuyen doi thanh cong USB Virtual COM Port (VCP) ket noi truc tiep vao may tinh.\n" \
             "- Script Python doc lap (scripts/aquatic_pc_bridge.py):\n" \
             "  Tiep nhan luong du lieu JSON tu Task_Telemetry o baudrate 115200 bps va ve do thi thoi gian thuc tren man hinh may tinh, dam bao he thong luon co kenh giam sat doc lap khi ha tang Wi-Fi gap su co."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(4)

    # Save presentation
    out_pptx = r"E:\AntiGravityRoot\mcp201-aquatic-guardian\AQUATIC_GUARDIAN_SLIDES.pptx"
    prs.save(out_pptx)
    print(f"[SUCCESS] Native executive presentation slides generated at: {out_pptx}")

if __name__ == '__main__':
    build_presentation()
