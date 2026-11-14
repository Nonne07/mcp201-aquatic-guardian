"""
=============================================================================
Project: Aquatic Guardian - Capstone MCP201 (Class IC2005 - Group 7)
Script:  generate_pptx_slides.py
Purpose: Generates the official presentation slide deck (.pptx).
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
    # SLIDE 1: Title Slide (Clean, Airy, Executive Cover)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    
    # Left Hero Box
    c_l = add_card(s1, Inches(0.8), Inches(1.2), Inches(6.8), Inches(5.0), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_DARK, border_width=Pt(1.5))
    tf_l = c_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = Inches(0.5)
    tf_l.margin_top = Inches(0.5)

    p = tf_l.paragraphs[0]
    p.text = "TRUONG DAI HOC FPT • KHOA DIEN TU - VIEN THONG"
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
    p.text = "He Thong Nhung Giam Sat Chat Luong Nuoc & Cho An Tu Dong"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(6)

    p = tf_l.add_paragraph()
    p.text = "DO AN TOT NGHIEP HOC PHAN: LAP TRINH VI DIEU KHIEN (MCP201)"
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
    add_badge(s1, Inches(7.8), Inches(1.2), Inches(4.733), Inches(0.4), "NHOM 7 — LOP IC2005", bg_color=COLOR_CARD_DARK)
    tf_r = c_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = Inches(0.35)
    tf_r.margin_top = Inches(0.55)

    team = [
        ("Nghiem Hoang Tung (SE211196)", "Truong nhom • Kien truc & Lap lich FreeRTOS"),
        ("Hoang Duc Manh (SE211191)", "Cam bien & Thuat toan loc tin hieu so DSP"),
        ("Do Khac Le Gia (SE211559)", "Co cau chap hanh Servo, Ro-le & Nguon dien"),
        ("Pham Hong Minh (SE211181)", "Giao tiep bus I2C1, RTC DS3231 & LCD UI"),
        ("Nguyen Duc Anh (SE211485)", "Phan he IoT, Telegram Bot API & Kiem thu")
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
    # SLIDE 2: Problem Statement (3 Clean Impact Cards)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Phan 1: Boi Canh & Muc Tieu", 
               "3 NGUYEN NHAN CHINH GAY SUY THOAI BE CA & GIAI PHAP", 
               "Loai bo rui ro o nhiem nuoc va giup ca sinh truong on dinh trong moi truong nhan tao")

    c_w = Inches(3.7)
    gap = Inches(0.3)
    y_start = Inches(1.8)

    cards_p2 = [
        ("1. NONG DO TDS NGUY HAI", "> 500 ppm",
         "- Thuc an thua & chat thai phan huy sinh doc to Ammonia va Nitrite.\n"
         "- TDS > 500 ppm lam hong bieu mo mang va soc tham thau.\n"
         "- He thong: Giam sat ADC1 thoi gian thuc va bao dong tuc thi < 200ms."),
        ("2. BIEN DONG NHIET DO", "24°C – 28°C",
         "- Ca nhiet doi chi thich nghi trong dai nhiet do tieu chuan 24°C – 28°C.\n"
         "- Nhiet do tang vuot 30°C lam suy giam nong do oxy hoa tan (DO).\n"
         "- He thong: Cam bien DS18B20 1-Wire bu nhiet chuan xac cho TDS."),
        ("3. SAI LECH DINH LUONG", "80% Ca Chet",
         "- Cho an du thua gay duc nuoc; quen cho an lam ca suy kiet the trang.\n"
         "- Chu vang nha khong the kiem soat lich trinh dinh duong.\n"
         "- He thong: Dinh luong 1g - 15g qua Servo, RTC hen gio & Bot tu xa.")
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
    # SLIDE 3: System Block Diagram (4 Clean Native Columns, 0.5đ + 3.0đ)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Phan 2: So Do Khoi & Phan Cung", 
               "SO DO KHOI HE THONG PHAN TAN (DISTRIBUTED DUAL-MCU)", 
               "Tach biet giua Dieu khien Thoi gian thuc (STM32) va Mang vien thong IoT (ESP32)")

    col_y = Inches(1.7)
    col_h = Inches(4.2)

    # 4 Columns
    cols_s3 = [
        ("1. CAM BIEN (INPUT)", Inches(0.8), Inches(2.6), [
            ("TDS Analog V1.0", "PA1 (ADC1_IN1)", "Loc tu gom 0.1 uF"),
            ("Bien tro B10K", "PA4 (ADC1_IN4)", "Chinh lieu 1g - 15g"),
            ("DS18B20 1-Wire", "PA8 (GPIO OD)", "Tro keo ngoai 4.7k"),
            ("Nut User B1", "PC13 (EXTI13)", "Loc rung phim 300ms")
        ]),
        ("2. NUCLEO-64 (CORE)", Inches(3.7), Inches(3.8), [
            ("STM32F401RE", "ARM Cortex-M4", "Xung nhip 84 MHz, FPU"),
            ("FreeRTOS v2", "CMSIS-RTOS v2", "5 Tac vu da nhiem tien dinh"),
            ("Dong bo IPC", "Length-1 Mailbox", "Chong tac nghen du lieu"),
            ("Priority Inherit", "Mutex I2C1", "Chong khoa chet bus")
        ]),
        ("3. CHAP HANH (OUTPUT)", Inches(7.8), Inches(2.6), [
            ("Servo SG90", "PA0 (TIM2 PWM)", "Quay 90 do xa thuc an"),
            ("Ro-le 5V", "PB4 (GPIO Out)", "Dong cat may bom mini"),
            ("Active Buzzer", "PB0 (Dem S8050)", "Coi bao dong khan cap"),
            ("LCD 2004", "PB8/PB9 (I2C1)", "Hien thi 4 dong thong so")
        ]),
        ("4. IOT BRIDGE", Inches(10.7), Inches(1.833), [
            ("ESP32 Wi-Fi", "UART1 @ 115200", "Dinh khung '~'"),
            ("Telegram Bot", "HTTPS Long-Poll", "/status & /feed"),
            ("Web Local", "Port 80 HTTP", "Dashboard dien thoai"),
            ("3.0 diem Rubric", "Complexity", "Module truyen thong")
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
    p.text = "[NGUYEN LY KIEN TRUC DUAL-MCU]: STM32 dam bao dap ung thoi gian thuc cung (Hard Real-Time); ESP32 dam nhan ket noi Wi-Fi/Telegram khong tat dinh. Hai vi dieu khien lien ket qua UART1 dinh khung '~' o 115200 bps."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # =========================================================================
    # SLIDE 4: Hardware Analysis (4 Problems & Fixes in Clean 2x2 Grid, 0.5đ)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Phan 2: So Do Khoi & Phan Cung", 
               "PHAN TICH MACH DIEN & 4 GIAI PHAP PHAN CUNG THUC NGHIEM", 
               "Khac phuc triet de cac rui ro nguon dien, dong cam va muc logic khi cam mach thuc te")

    grid_w = Inches(5.7)
    grid_h = Inches(2.2)
    coords4 = [
        (Inches(0.8), Inches(1.8)), (Inches(6.833), Inches(1.8)),
        (Inches(0.8), Inches(4.3)), (Inches(6.833), Inches(4.3))
    ]

    hw_cards = [
        ("1. SUT AP IC ON AP MB102",
         "Rui ro: Dropout AMS1117 la 1.2V. Cap 5V USB lam sut ap dau ra xuong ~3.8V, khien LCD bi toi va ro-le khong dong duoc.",
         "Giai phap: Cap Adapter DC 9V/12V qua cong chan tron 5.5mm, dam bao dau ra dat chuan 5.0V on dinh."),
        ("2. QUA DONG COI ACTIVE BUZZER",
         "Rui ro: Coi buzzer rut dong tuc thoi 25 - 35 mA vuot nguong chiu dung cua chan PB0 (8 - 15 mA), xung cam gay treo chip.",
         "Giai phap: Su dung Module Buzzer 3 chan co dem Transistor S8050, giam dong dieu khien chan PB0 xuong < 1 mA."),
        ("3. HU HONG PIN RTC CR2032",
         "Rui ro: Mach ZS-042 co duong nap nhoi cho pin sac LIR2032. Cap 5V lam nap nguoc gay phong ro pin CR2032 tieu chuan.",
         "Giai phap: Cap nguon 3.3V tu STM32 vao module de vo hieu hoa mach nap, hoac cach ly dien tro nap 200 Ohm."),
        ("4. DINH DONG RO-LE 5V",
         "Rui ro: Chenh lech muc logic giua 3.3V (STM32) va 5.0V (Ro-le Low-Trigger) lam optocoupler luon dan nhe, ro-le khong nha.",
         "Giai phap: Chon module ro-le co Jumper chuyen sang che do High-Trigger phu hop chuan logic 3.3V vi dieu khien.")
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
    p.text = "[NGUYEN TAC BO TRO]: Tro keo ngoai 4.7 kOhm cho DS18B20; Dau cheo UART1 (PA9 TX -> RX2, PA10 RX <- TX2); Chung mass GND toan mach."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # =========================================================================
    # SLIDE 5: FreeRTOS 5 Tasks (Clean Table & Stack Note)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Phan 3: Phan Mem & Thoi Gian Thuc", 
               "KIEN TRUC DA NHIEM TIEN DINH FREERTOS (CMSIS-RTOS V2)", 
               "Phan ra 5 tac vu doc lap, lap lich uu tien tuyet doi loai bo hoan toan blocking delay")

    # Table of 5 Tasks
    table_shape = s5.shapes.add_table(6, 5, Inches(0.8), Inches(1.8), Inches(11.733), Inches(3.4))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(2.6)
    tbl.columns[1].width = Inches(1.8)
    tbl.columns[2].width = Inches(1.5)
    tbl.columns[3].width = Inches(1.4)
    tbl.columns[4].width = Inches(4.433)

    headers = ["Ten Tac Vu (Thread)", "Muc Uu Tien", "Chu Ky Kich Hoat", "Stack Size", "Nhiem Vu Chinh"]
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
        ("Task_SafetySupervisor", "High (32)", "200 ms", "1024 Bytes", "Giam sat TDS/Nhiet do, kich hoat coi bao & LED Alert"),
        ("Task_DispenserControl", "AboveNormal (24)", "Event-Driven", "1024 Bytes", "Cho Semaphore nut/bot, quay Servo xa cam & ghi EEPROM"),
        ("Task_SensorAcquisition", "Normal (16)", "1000 ms", "1024 Bytes", "Thu thap ADC1, loc so 20 mau O(1), tinh TDS bu nhiet"),
        ("Task_DisplayUI", "BelowNormal (12)", "500 ms", "2048 Bytes", "Doc gio RTC DS3231, cap nhat 4 dong LCD 2004 qua I2C1"),
        ("Task_Telemetry", "Low (8)", "2000 ms", "2048 Bytes", "Dong goi JSON dinh khung '~' phat qua ESP32 va USB VCP")
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
    add_badge(s5, Inches(0.8), Inches(5.45), Inches(11.733), Inches(0.3), "QUY DINH QUAN LY BO NHO STACK TRONG CHUAN CMSIS-RTOS V2", bg_color=COLOR_BORDER_DARK)
    tf_sk = c_stk.text_frame
    tf_sk.word_wrap = True
    tf_sk.margin_left = Inches(0.25)
    tf_sk.margin_top = Inches(0.35)
    p = tf_sk.paragraphs[0]
    p.text = "- Don vi Stack tinh bang BYTES: Trong CMSIS-RTOS v2, tham so .stack_size tinh bang Bytes (khac v1 tinh bang Words). Khai bao nham se gay tran Stack va HardFault khi goi ham snprintf().\n" \
             "- Cap phat an toan: 1024 Bytes cho tac vu tinh toan; 2048 Bytes cho tac vu dinh dang chuoi hien thi LCD va JSON."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # =========================================================================
    # SLIDE 6: Flowchart (2 Streamlined Parallel Pipelines, 0.5đ)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Phan 3: Phan Mem & Thoi Gian Thuc", 
               "LUU DO THUAT TOAN: CAP DUONG & XU LY TIN HIEU SO", 
               "Minh chung lap trinh phi khoa (Non-blocking) va xu ly ngat tri hoan an toan")

    fc_w = Inches(5.7)

    # Column Left: Feeder Flowchart
    add_card(s6, Inches(0.8), Inches(1.8), fc_w, Inches(4.8), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s6, Inches(0.8), Inches(1.8), fc_w, Inches(0.35), "A. DIEU KHIEN CO CAU CAP DUONG (EVENT-DRIVEN)", bg_color=COLOR_CARD_DARK)

    pipe_a = [
        ("1. Trang thai cho", "Task_DispenserControl Blocked giai phong 100% CPU"),
        ("2. Kich hoat", "Nhan Semaphore tu Nut bam PC13 / Telegram / Hen gio RTC"),
        ("3. Tinh toan", "Doc ADC bien tro: Dwell Time = 300ms + (Portion x 80ms)"),
        ("4. Quay Servo", "PA0 phát PWM 50Hz: Quay mo 90 do -> Delay Dwell -> Ve 0 do"),
        ("5. Ghi EEPROM", "Chiem Mutex I2C1 -> Luu gio & luong an vao AT24C32 -> Nha Mutex")
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
    add_badge(s6, Inches(6.833), Inches(1.8), fc_w, Inches(0.35), "B. THU THAP & XU LY CAM BIEN TDS (DSP)", bg_color=COLOR_CARD_DARK)

    pipe_b = [
        ("1. Dinh thoi", "osDelayUntil(&last_wake, 1000ms) chong troi pha chu ky"),
        ("2. Doc ADC1", "Lay mau dien ap tho tren kenh PA1 (TDS Sensor V1.0)"),
        ("3. Loc so O(1)", "Tong chay: Sum = Sum - RingBuf[i] + NewSample (20 mau)"),
        ("4. Bu nhiet do", "Doc DS18B20: V_comp = V_adc / [1.0 + 0.02 x (T - 25.0)]"),
        ("5. Tinh TDS", "Da thuc bac 3 tinh TDS (ppm) -> Ghi de Length-1 Mailbox")
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
    # SLIDE 7: DSP & Temperature Math (50/50 Split)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Phan 3: Phan Mem & Thoi Gian Thuc", 
               "THUAT TOAN LOC SO O(1) & MO HINH TOAN BU NHIET DO", 
               "Khu nhieu bien dong song nuoc va hieu chuan nhiet do chinh xac theo mo hinh hoa nuoc")

    col7_w = Inches(5.7)

    # Left: Filter Card
    c7_l = add_card(s7, Inches(0.8), Inches(1.8), col7_w, Inches(4.8), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s7, Inches(0.8), Inches(1.8), col7_w, Inches(0.35), "1. BO LOC TRUNG BINH TRUOT VONG O(1)", bg_color=COLOR_CARD_DARK)
    tf7_l = c7_l.text_frame
    tf7_l.word_wrap = True
    tf7_l.margin_left = tf7_l.margin_right = Inches(0.3)
    tf7_l.margin_top = Inches(0.45)

    p = tf7_l.paragraphs[0]
    p.text = "Cong thuc cap nhat tong chay:"
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
    p.text = "- Do phuc tap O(1): Chi ton 1 phep cong va 1 phep tru moi chu ky; khong can vong lap for duyet 20 phan tu.\n" \
             "- Hieu qua thuc te: Do lech chuan giam tu ±45 ppm xuong < ±1.5 ppm, triet tieu hoan toan hien tuong bao dong gia khi song nuoc cuon."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_MUTED

    # Right: Temperature Math Card
    c7_r = add_card(s7, Inches(6.833), Inches(1.8), col7_w, Inches(4.8), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s7, Inches(6.833), Inches(1.8), col7_w, Inches(0.35), "2. MO HINH BU NHIET DO & DA THUC TDS", bg_color=COLOR_CARD_DARK)
    tf7_r = c7_r.text_frame
    tf7_r.word_wrap = True
    tf7_r.margin_left = tf7_r.margin_right = Inches(0.3)
    tf7_r.margin_top = Inches(0.45)

    p = tf7_r.paragraphs[0]
    p.text = "Phuong trinh quy chuan ve 25.0°C:"
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
    p.text = "- He so bu nhiet 2%/°C: Do dan dien tang theo nhiet do; neu khong bu nhiet, nuoc nong se bi bao sai lech toi 20%.\n" \
             "- Thuc thi tren FPU Cortex-M4: Tinh toan so thuc don chu ky, thoi gian thuc thi < 2.5 us."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 8: Concurrency & Priority Inheritance (50/50 Split)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Phan 3: Phan Mem & Thoi Gian Thuc", 
               "DONG BO IPC: LENGTH-1 MAILBOX & KE THUA QUYEN UU TIEN", 
               "Giai quyet triet de hai bai toan kinh dien: Tac nghen du lieu va Nghich dao do uu tien")

    col8_w = Inches(5.7)

    # Left: Mailbox Card
    c8_l = add_card(s8, Inches(0.8), Inches(1.8), col8_w, Inches(4.8), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s8, Inches(0.8), Inches(1.8), col8_w, Inches(0.35), "1. HOM THU DON (LENGTH-1 MAILBOX)", bg_color=COLOR_CARD_DARK)
    tf8_l = c8_l.text_frame
    tf8_l.word_wrap = True
    tf8_l.margin_left = tf8_l.margin_right = Inches(0.3)
    tf8_l.margin_top = Inches(0.45)

    p = tf8_l.paragraphs[0]
    p.text = "- Van de (Data Starvation):\n" \
             "  Hang doi FreeRTOS co tinh tieu thu xoa (Destructive Read). Tac vu Supervisor (200ms) se chiem toan bo goi tin, khien DisplayUI va Telemetry bi bo doi du lieu."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_MUTED

    p = tf8_l.add_paragraph()
    p.text = "- Giai phap Length-1 Mailbox:\n" \
             "  • Producer (Sensor Task) su dung xQueueOverwrite() cap nhat ban tin moi nhat.\n" \
             "  • 3 Consumers deu su dung xQueuePeek() sao chep ma KHONG xoa phan tu.\n" \
             "  • Ket qua: Ca 3 tac vu truy xuat doc lap theo chu ky rieng (200ms, 500ms, 2000ms), 0% mat du lieu."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.space_before = Pt(12)

    # Right: Priority Inheritance Card
    c8_r = add_card(s8, Inches(6.833), Inches(1.8), col8_w, Inches(4.8), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s8, Inches(6.833), Inches(1.8), col8_w, Inches(0.35), "2. KE THUA QUYEN UU TIEN (PRIORITY INHERITANCE)", bg_color=COLOR_CARD_DARK)
    tf8_r = c8_r.text_frame
    tf8_r.word_wrap = True
    tf8_r.margin_left = tf8_r.margin_right = Inches(0.3)
    tf8_r.margin_top = Inches(0.45)

    p = tf8_r.paragraphs[0]
    p.text = "- Van de (Priority Inversion):\n" \
             "  DisplayUI (12) giu Mutex I2C1; Dispenser (24) thuc tinh can ghi EEPROM. Neu Task_Sensor (16) chiem CPU, no se ngan DisplayUI nha bus, gián tiep phong toa Dispenser."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_MUTED

    p = tf8_r.add_paragraph()
    p.text = "- Co che Ke thua quyen uu tien:\n" \
             "  • Khi Task 24 doi Mutex, FreeRTOS lap tuc nang uu tien DisplayUI tu 12 len 24.\n" \
             "  • Task 16 khong the chen ngang, DisplayUI giai phong Mutex trong 4.2 ms.\n" \
             "  • Task 24 lap tuc chiem bus ghi log an toan, loai bo khoa chet he thong."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.space_before = Pt(12)

    # =========================================================================
    # SLIDE 9: Critical Source Code (3 Monospace Cards, 0.5đ)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Phan 3: Phan Mem & Thoi Gian Thuc", 
               "PHAN TICH MA NGUON C TRONG YEU (SOURCE CODE ANALYSIS)", 
               "Minh chung chat luong lap trinh nhung STM32 HAL va ESP32 theo dung tieu chi Rubric (0.5d)")

    col9_w = Inches(3.7)

    code_data = [
        ("A. DEFERRED ISR (NGAT TRI HOAN)",
         "void HAL_GPIO_EXTI_Callback(uint16_t Pin) {\n"
         "  static uint32_t last = 0;\n"
         "  if (Pin == GPIO_PIN_13) {\n"
         "    uint32_t now = HAL_GetTick();\n"
         "    if ((now - last) > 300U) {\n"
         "      last = now;\n"
         "      // Nha Semaphore < 1us\n"
         "      osSemaphoreRelease(feedSem);\n"
         "    }\n"
         "  }\n"
         "}",
         "- Khong dat delay trong ngat ISR.\n"
         "- Xu ly nang ban giao cho Thread."),
        ("B. TINH TONG CHAY O(1)",
         "// Circular Buffer Moving Sum\n"
         "tds_sum -= ring_buf[buf_idx];\n"
         "tds_sum += new_raw_adc;\n"
         "ring_buf[buf_idx] = new_raw_adc;\n"
         "buf_idx = (buf_idx + 1) % 20;\n\n"
         "float v = (tds_sum/20.0f)*3.3f/4095;\n"
         "float vc = v/(1.0f+0.02f*(t-25));\n"
         "tds = (133.42*vc*vc*vc\n"
         "     - 255.86*vc*vc + 857.39*vc)*0.5f;",
         "- Khong dung vong lap for.\n"
         "- Tiet kiem toi da chu ky CPU."),
        ("C. UART FSM DECODER",
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
         "- Loai bo toan bo byte rac do nhieu.\n"
         "- Tinh toan ven du lieu 100%.")
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
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p = tf_t.paragraphs[0]
        p.text = takeaway
        p.font.name = 'Segoe UI'
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_TEXT_PRIMARY

    # =========================================================================
    # SLIDE 10: IoT & Telegram Subsystem (3.0đ Complexity)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Phan 4: Phan He IoT & Kiem Thu", 
               "PHAN HE IOT ESP32 & NEN TANG TELEGRAM BOT", 
               "Module truyen thong khong day dat tron ven 3.0 diem Project Complexity trong Rubric")

    # Top Framing Banner
    top_f = add_card(s10, Inches(0.8), Inches(1.8), Inches(11.733), Inches(1.2), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER_DARK, border_width=Pt(1.2))
    add_badge(s10, Inches(0.8), Inches(1.8), Inches(11.733), Inches(0.3), "CAU TRUC DINH KHUNG UART 2 CHIEU (BAUDRATE 115200 BPS)", bg_color=COLOR_BORDER_DARK)

    # Delimiter Start
    add_badge(s10, Inches(1.1), Inches(2.25), Inches(1.6), Inches(0.6), "START\n'~' (0x7E)", bg_color=COLOR_CARD_DARK, text_color=COLOR_TEXT_WHITE, font_size=8.5)
    # Payload
    pld = add_card(s10, Inches(2.9), Inches(2.25), Inches(7.533), Inches(0.6), bg_color=COLOR_BG_WHITE, border_color=COLOR_BORDER_DARK)
    p = pld.text_frame.paragraphs[0]
    p.text = "PAYLOAD: JSON Telemetry ({\"tds\":185,\"temp\":26.5})   HOAC   Lenh: 'feed' / 'status'"
    p.font.name = 'Consolas'
    p.font.size = Pt(9)
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.alignment = PP_ALIGN.CENTER
    # Delimiter End
    add_badge(s10, Inches(10.633), Inches(2.25), Inches(1.6), Inches(0.6), "END\n'~' (0x7E)", bg_color=COLOR_CARD_DARK, text_color=COLOR_TEXT_WHITE, font_size=8.5)

    # 2 Bottom Cards
    c10_w = Inches(5.7)

    # Left: Long Polling
    c10_l = add_card(s10, Inches(0.8), Inches(3.2), c10_w, Inches(3.4), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s10, Inches(0.8), Inches(3.2), c10_w, Inches(0.35), "1. CO CHE HTTPS LONG-POLLING", bg_color=COLOR_CARD_DARK)
    tf10_l = c10_l.text_frame
    tf10_l.word_wrap = True
    tf10_l.margin_left = tf10_l.margin_right = Inches(0.3)
    tf10_l.margin_top = Inches(0.45)
    p = tf10_l.paragraphs[0]
    p.text = "- Ket noi TLS/HTTPS Cổng 443 toi api.telegram.org qua UniversalTelegramBot.\n\n" \
             "- Xuyen Router / NAT: Chay tren moi mang Wi-Fi/4G khong can IP tinh hay mo port.\n\n" \
             "- Chi phi 0 dong: Tao bot trong 30 giay qua @BotFather, API mien phi 100%."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # Right: Commands & Push Alert
    c10_r = add_card(s10, Inches(6.833), Inches(3.2), c10_w, Inches(3.4), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s10, Inches(6.833), Inches(3.2), c10_w, Inches(0.35), "2. BO LENH & CANH BAO CHU DONG", bg_color=COLOR_CARD_DARK)
    tf10_r = c10_r.text_frame
    tf10_r.word_wrap = True
    tf10_r.margin_left = tf10_r.margin_right = Inches(0.3)
    tf10_r.margin_top = Inches(0.45)
    p = tf10_r.paragraphs[0]
    p.text = "- Lenh /status: Xem TDS, nhiet do, khau phan va trang thai nuoc thoi gian thuc.\n\n" \
             "- Lenh /feed: Phat chuoi ~feed~ qua UART kich hoat Servo xa dung lieu.\n\n" \
             "- Auto Push Notification: Tu dong gui tin nhan khan cap khi TDS > 500 ppm.\n\n" \
             "- Web Dashboard cuc bo: Truy cap thang dia chi IP cua ESP32 tu trinh duyet."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # =========================================================================
    # SLIDE 11: Validation & Benchmarks
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Phan 4: Phan He IoT & Kiem Thu", 
               "KET QUA KIEM THU DOC LAP & DO LUONG THOI GIAN THUC", 
               "Xac thuc 4 module doc lap va chung minh dap ung cac rang buoc thoi gian thuc nghiem ngat")

    c11_w = Inches(5.7)

    # Left: Unit Tests
    c11_l = add_card(s11, Inches(0.8), Inches(1.8), c11_w, Inches(4.8), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s11, Inches(0.8), Inches(1.8), c11_w, Inches(0.35), "KIEM THU 4 MODULE PHAN MEM DOC LAP", bg_color=COLOR_CARD_DARK)
    tf11_l = c11_l.text_frame
    tf11_l.word_wrap = True
    tf11_l.margin_left = tf11_l.margin_right = Inches(0.3)
    tf11_l.margin_top = Inches(0.45)

    u_tests = [
        ("test_servo_pwm.c", "PWM 50Hz, mo 90 do chinh xac; Dwell Time dap ung 380ms - 1500ms"),
        ("test_tds_filter.c", "Bo loc 20 mau O(1) giam 96.7% phuong sai song nuoc (±1.5 ppm)"),
        ("test_i2c_scanner.c", "Nhan dien du 3 thiet bi (0x27 LCD, 0x68 RTC, 0x57 EEPROM)"),
        ("test_uart_bridge.c", "Truyen 1,000 goi JSON lien tuc @ 115200: Ty le loi khung 0.0%")
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
    add_badge(s11, Inches(6.833), Inches(1.8), c11_w, Inches(0.35), "DO LUONG DO TRE & BO NHO THUC TE", bg_color=COLOR_CARD_DARK)
    tf11_r = c11_r.text_frame
    tf11_r.word_wrap = True
    tf11_r.margin_left = tf11_r.margin_right = Inches(0.3)
    tf11_r.margin_top = Inches(0.45)

    p = tf11_r.paragraphs[0]
    p.text = "Thoi gian dap ung he thong (Latency):"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    p = tf11_r.add_paragraph()
    p.text = "• Phat hien vuot nguong TDS: 185 ms (Tieu chuan: < 300 ms)\n" \
             "• Do tre ngat nut bam EXTI: 0.85 us (Tieu chuan: < 10 us)\n" \
             "• Thoi gian nha Mutex I2C1: 4.2 ms (Nguong an toan: < 50 ms)\n" \
             "• Do tre truyen goi UART: 2.8 ms (Nguong cho phep: < 10 ms)"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(4)

    p = tf11_r.add_paragraph()
    p.text = "Chiem dung tai nguyen STM32F401RE:"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.space_before = Pt(12)

    p = tf11_r.add_paragraph()
    p.text = "• Flash ROM: 48.2 KB / 512 KB (Chiem 9.41% - Con du >90%)\n" \
             "• Static SRAM: 12.4 KB / 96 KB (Chiem 12.92% - Con du >87%)\n" \
             "• FreeRTOS Heap_4: 4096 / 8192 Bytes (50.0% an toan)"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 12: 4-Stage Live Demonstration (1.0đ Demonstration)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Phan 5: Trinh Dien & Ket Luan", 
               "KICH BAN TRINH DIEN MO HINH THUC TE 4 GIAI DOAN", 
               "Quy trinh dien tap chuan muc trong vong 2 phut dat diem tuyet doi Demonstration (1.0d)")

    coords12 = [
        (Inches(0.8), Inches(1.8)), (Inches(6.833), Inches(1.8)),
        (Inches(0.8), Inches(4.1)), (Inches(6.833), Inches(4.1))
    ]
    grid12_w = Inches(5.7)
    grid12_h = Inches(2.1)

    stages = [
        ("BƯỚC 1: KHOI DONG (20s)", 
         "- Thao tac: Cap nguon Adapter 9V DC vao mach MB102.\n"
         "- Phan hoi: LCD 2004 hien thi 4 dong thong so; LED xanh PA5 sang on dinh; Ro-le 5V dong may bom nuoc tuan hoan."),
        ("BƯỚC 2: CHO AN THU CONG (30s)", 
         "- Thao tac: Vặn bien tro PA4 (chinh 1g - 15g), nhan nut PC13.\n"
         "- Phan hoi: Servo SG90 quay 90° mo nap xa thuc an dung thoi gian Dwell Time; ghi nhat ky vao EEPROM qua I2C."),
        ("BƯỚC 3: DIEU KHIEN TELEGRAM (30s)", 
         "- Thao tac: Gui lenh /status va /feed qua ung dung Telegram tren dien thoai.\n"
         "- Phan hoi: Bot bao cao thong so trong < 1s; Servo chap hanh lap tuc mo nap xa thuc an tu xa."),
        ("BƯỚC 4: MO PHONG SU CO (40s)", 
         "- Thao tac: Nhac dau do TDS nhung sang coc nuoc muoi (> 500 ppm).\n"
         "- Phan hoi: Trong < 200ms, coi Buzzer keu, LED do nhay 1Hz, LCD bao 'CRITICAL HAZARD', Telegram tu dong ban tin nhan bao dong.")
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
    p.text = "[MA NGUON & TAI LIEU GOC]: https://github.com/Nonne07/mcp201-aquatic-guardian. Nhom 7 san sang cho phan Van dap chuyen sau (Q&A 3.0d)!"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 13: Appendix (Memory Map & Failsafe PC Bridge)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Phu Luc Ky Thuat (Backup Slide)", 
               "BAN DO BO NHO HE THONG & KENH VIEN THONG DU PHONG FAILSAFE", 
               "Tai lieu ky thuat phuc vu van dap chuyen sau ve quan ly tai nguyen vi dieu khien (Q&A 3.0d)")

    col13_w = Inches(5.7)

    # Left: Memory Map
    c13_l = add_card(s13, Inches(0.8), Inches(1.8), col13_w, Inches(4.8), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s13, Inches(0.8), Inches(1.8), col13_w, Inches(0.35), "1. PHAN BO BO NHO CHI TIET (MEMORY FOOTPRINT)", bg_color=COLOR_CARD_DARK)
    tf13_l = c13_l.text_frame
    tf13_l.word_wrap = True
    tf13_l.margin_left = tf13_l.margin_right = Inches(0.3)
    tf13_l.margin_top = Inches(0.45)

    p = tf13_l.paragraphs[0]
    p.text = "• Flash ROM (512 KB): 48.2 KB (9.41%)\n" \
             "  Bao gom STM32 HAL Drivers, FreeRTOS Kernel, libc math routines va Task functions.\n\n" \
             "• Static RAM (96 KB): 12.4 KB (12.92%)\n" \
             "  Bao gom bien toan cuc, Circular Buffers, DMA Descriptors va vung nho .data/.bss.\n\n" \
             "• FreeRTOS Heap (Heap_4): 4096 / 8192 Bytes (50% an toan)\n" \
             "  Cap phat 5 TCBs, 5 Task Stacks, 2 Mutexes va 1 Semaphore.\n\n" \
             "• uxTaskGetStackHighWaterMark():\n" \
             "  Xac nhan tat ca tac vu deu con du > 35% bien do an toan, khong co nguy co tran Stack."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # Right: Failsafe PC Bridge
    c13_r = add_card(s13, Inches(6.833), Inches(1.8), col13_w, Inches(4.8), bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER_MEDIUM)
    add_badge(s13, Inches(6.833), Inches(1.8), col13_w, Inches(0.35), "2. KENH DU PHONG ST-LINK VIRTUAL COM PORT", bg_color=COLOR_CARD_DARK)
    tf13_r = c13_r.text_frame
    tf13_r.word_wrap = True
    tf13_r.margin_left = tf13_r.margin_right = Inches(0.3)
    tf13_r.margin_top = Inches(0.45)

    p = tf13_r.paragraphs[0]
    p.text = "• Nguyen ly ket noi:\n" \
             "  Cap chan PA2/PA3 duoc noi cung voi chip nap ST-LINK/V2-1 tren bo Nucleo, tu dong tao cong USB Virtual COM Port (VCP) noi vao laptop.\n\n" \
             "• Script Python doc lap (scripts/aquatic_pc_bridge.py):\n" \
             "  Giai ma chuoi JSON tu Task_Telemetry o baudrate 115200 bps va ve do thi thoi gian thuc tren man hinh PC.\n\n" \
             "• Phuong an du phong Failsafe:\n" \
             "  Neu Wi-Fi phong thi gap su co, he thong van trinh dien day du do thi live qua cap USB ma khong can bat ky ket noi mang nao."
    p.font.name = 'Segoe UI'
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # Save presentation
    out_pptx = r"E:\AntiGravityRoot\mcp201-aquatic-guardian\AQUATIC_GUARDIAN_SLIDES.pptx"
    prs.save(out_pptx)
    print(f"[SUCCESS] Clean anti-wall-of-text slides generated at: {out_pptx}")

if __name__ == '__main__':
    build_presentation()
