"""
=============================================================================
Script: generate_slide_assets.py
Purpose: Generates high-resolution academic monochrome diagram figures
         for embedding into the Aquatic Guardian capstone slide deck.
Style:   Strict academic monochrome (IEEE/ACM style), grayscale palette,
         high DPI (300 DPI), clean typography.
=============================================================================
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = os.path.abspath(r"E:\AntiGravityRoot\mcp201-aquatic-guardian\assets")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Common styling constants
FONT_FAMILY = 'DejaVu Sans'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Segoe UI']
plt.rcParams['axes.edgecolor'] = '#1E293B'
plt.rcParams['axes.linewidth'] = 1.2

def generate_dsp_plots():
    """Generates comparative plots for ADC raw noise vs 20-sample filter and TDS Temp Compensation."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')

    # Subplot 1: Sensor Denoising
    np.random.seed(42)
    n_samples = 120
    t = np.arange(n_samples)
    base_signal = 220.0 + 8.0 * np.sin(2 * np.pi * t / 60)
    # Add water agitation noise and random spikes
    noise = np.random.normal(0, 18.0, n_samples)
    spikes = np.zeros(n_samples)
    spikes[15] = 65.0
    spikes[45] = -55.0
    spikes[82] = 70.0
    spikes[105] = -60.0
    raw_signal = base_signal + noise + spikes

    # 20-sample moving average filter
    window = 20
    filtered_signal = np.convolve(raw_signal, np.ones(window)/window, mode='same')

    ax1.set_facecolor('#FAFAFA')
    ax1.plot(t, raw_signal, color='#94A3B8', linestyle='--', linewidth=1.2, label='Tin hieu ADC goc (Nhieu bien dong ±45 ppm)')
    ax1.plot(t[10:-10], filtered_signal[10:-10], color='#0F172A', linewidth=2.4, label='Sau bo loc Moving Average 20 mau O(1)')
    ax1.set_title('A. KET QUA KHU NHIEU TIN HIEU ADC CAM BIEN TDS', fontsize=11, fontweight='bold', pad=12, color='#0F172A')
    ax1.set_xlabel('Chi so mau thu thap (Sample Index k)', fontsize=10, fontweight='bold', color='#1E293B')
    ax1.set_ylabel('Gia tri TDS (ppm)', fontsize=10, fontweight='bold', color='#1E293B')
    ax1.legend(loc='upper right', fontsize=8.5, framealpha=0.9, edgecolor='#CBD5E1')
    ax1.grid(True, linestyle=':', alpha=0.6, color='#CBD5E1')
    ax1.set_ylim(140, 320)

    # Subplot 2: Temperature Compensation Curve
    t_water = np.linspace(15, 35, 100)
    v_raw = 1.25  # Nominal voltage at 25C
    # V_comp = V_raw / [1.0 + 0.02 * (T - 25.0)]
    v_comp = v_raw / (1.0 + 0.02 * (t_water - 25.0))
    # Relative TDS deviation if uncompensated
    tds_error_pct = (1.0 + 0.02 * (t_water - 25.0) - 1.0) * 100

    ax2.set_facecolor('#FAFAFA')
    ax2.plot(t_water, v_comp, color='#0F172A', linewidth=2.4, label='Dien ap quy chuan V_comp tai 25°C')
    ax2.axvline(25.0, color='#64748B', linestyle=':', linewidth=1.5, label='Nhiet do chuan T_ref = 25.0°C')
    ax2.set_title('B. DAC TUYEN BU NHIET DO DIEN AP TDS V1.0', fontsize=11, fontweight='bold', pad=12, color='#0F172A')
    ax2.set_xlabel('Nhiet do moi truong nuoc T (°C)', fontsize=10, fontweight='bold', color='#1E293B')
    ax2.set_ylabel('Dien ap hieu chuan V_comp (V)', fontsize=10, fontweight='bold', color='#1E293B')
    ax2.legend(loc='upper right', fontsize=8.5, framealpha=0.9, edgecolor='#CBD5E1')
    ax2.grid(True, linestyle=':', alpha=0.6, color='#CBD5E1')
    ax2.set_ylim(0.95, 1.65)

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'fig_dsp_plots.png')
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Generated {out_path}")

def generate_memory_chart():
    """Generates memory allocation breakdown chart for Flash ROM and SRAM."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')

    # Data for Flash
    flash_labels = ['Code & RTOS\n48.2 KB (9.4%)', 'Flash Trong\n463.8 KB (90.6%)']
    flash_sizes = [48.2, 463.8]
    flash_colors = ['#334155', '#E2E8F0']

    wedges1, texts1, autotexts1 = ax1.pie(flash_sizes, labels=flash_labels, autopct='%1.1f%%',
                                          startangle=140, colors=flash_colors,
                                          wedgeprops=dict(width=0.45, edgecolor='#1E293B', linewidth=1.2),
                                          textprops=dict(color='#0F172A', fontsize=9, fontweight='bold'))
    for autotext in autotexts1:
        autotext.set_color('#FFFFFF' if autotext.get_text() == '9.4%' else '#0F172A')
        autotext.set_fontsize(9)
        autotext.set_weight('bold')
    ax1.set_title('PHAN BO BO NHO FLASH (512 KB)\nSTM32F401RE ROM Footprint', fontsize=10.5, fontweight='bold', color='#0F172A', pad=10)

    # Data for SRAM
    sram_labels = ['Global/Stack/Heap\n12.4 KB (12.9%)', 'SRAM Trong\n83.6 KB (87.1%)']
    sram_sizes = [12.4, 83.6]
    sram_colors = ['#1E293B', '#F1F5F9']

    wedges2, texts2, autotexts2 = ax2.pie(sram_sizes, labels=sram_labels, autopct='%1.1f%%',
                                          startangle=140, colors=sram_colors,
                                          wedgeprops=dict(width=0.45, edgecolor='#1E293B', linewidth=1.2),
                                          textprops=dict(color='#0F172A', fontsize=9, fontweight='bold'))
    for autotext in autotexts2:
        autotext.set_color('#FFFFFF' if autotext.get_text() == '12.9%' else '#0F172A')
        autotext.set_fontsize(9)
        autotext.set_weight('bold')
    ax2.set_title('PHAN BO BO NHO SRAM (96 KB)\nSTM32F401RE RAM Footprint', fontsize=10.5, fontweight='bold', color='#0F172A', pad=10)

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'fig_memory_footprint.png')
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Generated {out_path}")

def generate_block_diagram():
    """Generates the official system architecture block diagram (monochrome academic style)."""
    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 65)
    ax.axis('off')

    def draw_box(x, y, w, h, title, items=[], bg='#F8FAFC', border='#1E293B', lw=1.2, title_size=9.5, body_size=8.0):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3",
                                      facecolor=bg, edgecolor=border, linewidth=lw)
        ax.add_patch(rect)
        ax.text(x + w/2.0, y + h - 2.8, title, ha='center', va='center',
                fontsize=title_size, fontweight='bold', color='#0F172A')
        curr_y = y + h - 5.5
        for item in items:
            ax.text(x + 1.5, curr_y, item, ha='left', va='center',
                    fontsize=body_size, color='#334155')
            curr_y -= 2.6

    # 1. Sensing Box (Left)
    draw_box(3, 30, 24, 30, "KHOI CAM BIEN (SENSORS)", [
        "[+] TDS Analog V1.0 (PA1 ADC1)",
        "[+] Bien tro xoay B10K (PA4 ADC1)",
        "[+] DS18B20 1-Wire (PA8 GPIO)",
        "[+] Nut nhan User B1 (PC13 EXTI13)",
        "[+] Tu loc nhieu 0.1 uF tai chan ADC",
        "[+] Tro keo ngoai 4.7 kOhm 1-Wire"
    ], bg='#F1F5F9', border='#334155', lw=1.5)

    # 2. Main Controller Box (Center)
    draw_box(32, 22, 54, 40, "BO XU LY TRUNG TAM: STM32 NUCLEO-64 (ARM CORTEX-M4)", [
        "Phan cung: STM32F401RE @ 84 MHz | 512 KB Flash | 96 KB SRAM | FPU & DSP",
        "He dieu hanh: FreeRTOS v2 Kernel (Preemptive Priority-Based Scheduler)",
        "-------------------------------------------------------------------------------------------------------",
        "- Task_SafetySupervisor   [Uu tien 32 - High]       : Chu ky 200 ms, phat hien vuot nguong TDS/Nhiet",
        "- Task_DispenserControl   [Uu tien 24 - AboveNorm]  : Event-Driven, nhan Semaphore tu Nut/Bot/RTC",
        "- Task_SensorAcquisition  [Uu tien 16 - Normal]     : Chu ky 1000 ms, loc so 20 mau O(1), tinh TDS bu nhiet",
        "- Task_DisplayUI          [Uu tien 12 - BelowNorm]  : Chu ky 500 ms, doc RTC DS3231, cap nhat LCD 2004",
        "- Task_Telemetry          [Uu tien 8  - Low]        : Chu ky 2000 ms, dong goi JSON va dinh khung UART",
        "Dong bo lien tac vu (IPC): Length-1 Mailbox (chong tac nghen) | Mutex I2C1 (Priority Inheritance)"
    ], bg='#FFFFFF', border='#0F172A', lw=2.0, title_size=10.5, body_size=8.0)

    # 3. Actuators Box (Right Top)
    draw_box(91, 35, 26, 25, "CO CAU CHAP HANH (ACTUATORS)", [
        "[>] Dong co Servo SG90 (PA0 PWM TIM2)",
        "[>] Ro-le 5V cach ly quang (PB4 Out)",
        "[>] Active Buzzer co dem S8050 (PB0)",
        "[>] LED Status Xanh/Do (PA5 / PB1)",
        "[>] May bom nuoc tuan hoan mini 5V"
    ], bg='#F1F5F9', border='#334155', lw=1.5)

    # 4. Bus Peripherals (Right Bottom)
    draw_box(91, 5, 26, 26, "NGOAI VI BUS I2C1 (PB8/PB9)", [
        "[=] Man hinh LCD 2004 (PCF8574, 0x27)",
        "[=] Module RTC DS3231 (Real-time, 0x68)",
        "[=] EEPROM AT24C32 (Nhat ky, 0x57)",
        "[=] Tro keo I2C 4.7 kOhm tren bus"
    ], bg='#F8FAFC', border='#64748B', lw=1.2)

    # 5. Dual-MCU IoT Co-Processor (Bottom Left-Center)
    draw_box(32, 3, 54, 16, "PHAN HE IOT DUAL-MCU: ESP32 WI-FI CO-PROCESSOR", [
        "Ket noi vi dieu khien: UART1 (PA9 TX <-> RX2 GPIO16, PA10 RX <-> TX2 GPIO17) @ 115200 bps",
        "Giao thuc dinh khung tin hieu: Frame Delimiter '~' (Bat dau '~' | Payload JSON | Ket thuc '~')",
        "Dich vu mang: HTTPS Long-Polling toi api.telegram.org | Web Server Dashboard cuc bo Port 80"
    ], bg='#F1F5F9', border='#1E293B', lw=1.5, title_size=10.0, body_size=8.0)

    # 6. User Endpoints (Far Left Bottom)
    draw_box(3, 3, 24, 23, "GIAO DIEN NGUOI DUNG", [
        "1. Ung dung Telegram (iOS/Android)",
        "   - Lenh: /status, /feed, /help",
        "   - Auto Alert khi TDS > 500 ppm",
        "2. Web Browser Dashboard (IP Local)",
        "3. Cáp ST-LINK USB VCP (PA2/PA3)",
        "   - Do thi Python PC (Kenh du phong)"
    ], bg='#FFFFFF', border='#64748B', lw=1.2)

    # Connective Arrows
    arrow_props = dict(arrowstyle='->,head_width=0.4,head_length=0.6', color='#0F172A', lw=1.5)
    arrow_bidir = dict(arrowstyle='<->,head_width=0.4,head_length=0.6', color='#0F172A', lw=1.5)

    # Sensors -> STM32
    ax.annotate('', xy=(32, 45), xytext=(27, 45), arrowprops=arrow_props)
    ax.text(29.5, 46.5, "ADC / GPIO", fontsize=7.5, fontweight='bold', ha='center', color='#334155')

    # STM32 -> Actuators
    ax.annotate('', xy=(91, 48), xytext=(86, 48), arrowprops=arrow_props)
    ax.text(88.5, 49.5, "PWM / GPIO", fontsize=7.5, fontweight='bold', ha='center', color='#334155')

    # STM32 <-> I2C1
    ax.annotate('', xy=(91, 18), xytext=(86, 25), arrowprops=arrow_bidir)
    ax.text(89.5, 23.0, "I2C1 Bus", fontsize=7.5, fontweight='bold', ha='center', color='#334155')

    # STM32 <-> ESP32 (UART1)
    ax.annotate('', xy=(59, 22), xytext=(59, 19), arrowprops=arrow_bidir)
    ax.text(64, 20.2, "UART1 (115200 bps)", fontsize=7.5, fontweight='bold', ha='center', color='#0F172A')

    # ESP32 <-> Endpoints
    ax.annotate('', xy=(27, 11), xytext=(32, 11), arrowprops=arrow_bidir)
    ax.text(29.5, 12.2, "Wi-Fi", fontsize=7.5, fontweight='bold', ha='center', color='#0F172A')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'fig_block_diagram.png')
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Generated {out_path}")

def generate_flowchart():
    """Generates the dual-pipeline flowchart (Feeder FSM and Sensor DSP) in monochrome academic style."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6.2), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')

    for ax, title in [(ax1, 'A. LUU DO CO CAU CHO AN (EVENT-DRIVEN FSM)'),
                      (ax2, 'B. LUU DO THU THAP & XU LY TIN HIEU SO TDS')]:
        ax.set_facecolor('#FFFFFF')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis('off')
        ax.text(50, 96, title, ha='center', va='center', fontsize=10.5, fontweight='bold', color='#0F172A')

    def draw_node(ax, x, y, w, h, text, shape='rect', bg='#F8FAFC', border='#1E293B'):
        if shape == 'rect':
            box = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.2",
                                         facecolor=bg, edgecolor=border, linewidth=1.2)
        elif shape == 'oval':
            box = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="circle,pad=0.1",
                                         facecolor=bg, edgecolor=border, linewidth=1.2)
        elif shape == 'diamond':
            pts = np.array([[x, y + h/2], [x + w/2, y], [x, y - h/2], [x - w/2, y]])
            box = patches.Polygon(pts, closed=True, facecolor=bg, edgecolor=border, linewidth=1.2)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=8.0, fontweight='bold', color='#0F172A')

    def draw_arrow(ax, x1, y1, x2, y2, label=None):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.55', color='#0F172A', lw=1.2))
        if label:
            ax.text((x1+x2)/2 + 2, (y1+y2)/2, label, fontsize=7.5, color='#334155', fontweight='bold')

    # Pipeline A: Feeder FSM
    draw_node(ax1, 50, 88, 70, 7, "TRANG THAI CHO (TASK IDLE / BLOCKED)\nCho Semaphore tu ISR hoac Task_Telemetry", shape='rect')
    draw_arrow(ax1, 50, 84, 50, 75)

    draw_node(ax1, 50, 71, 74, 8, "SU KIEN KICH HOAT?\nNut bam PC13 / Lenh Telegram ~feed~ / Hen gio RTC", shape='diamond', bg='#F1F5F9')
    draw_arrow(ax1, 50, 67, 50, 58, label="Co")

    draw_node(ax1, 50, 54, 70, 7, "DOC ADC BIEN TRO & TINH DINH LUONG\nDwell Time = 300 ms + (Dose_g x 80 ms)", shape='rect')
    draw_arrow(ax1, 50, 50, 50, 41)

    draw_node(ax1, 50, 37, 70, 7, "DIEU KHIEN SERVO SG90 (TIM2 PWM)\nQuay mo goc 90 do -> Delay Dwell Time -> Dong ve 0 do", shape='rect', bg='#E2E8F0')
    draw_arrow(ax1, 50, 33, 50, 24)

    draw_node(ax1, 50, 20, 70, 7, "GHI NHAT KY EEPROM AT24C32 (I2C1)\nChiem Mutex -> Luu Timestamp & Khau phan -> Nha Mutex", shape='rect')
    draw_arrow(ax1, 50, 16, 50, 8)

    draw_node(ax1, 50, 5, 70, 6, "HOAN TAT CHU KY CHO AN -> QUAY VE TRANG THAI CHO", shape='rect', bg='#F1F5F9')

    # Pipeline B: Sensor DSP
    draw_node(ax2, 50, 88, 70, 7, "KICH HOAT DINH KY (PERIODIC TIMER)\nosDelayUntil(&last_wake, 1000 ms)", shape='rect')
    draw_arrow(ax2, 50, 84, 50, 75)

    draw_node(ax2, 50, 71, 70, 7, "DOC ADC1 CHANNEL 1 (PA1 - TDS)\nLay mau gia tri dien ap tho (0 - 4095)", shape='rect')
    draw_arrow(ax2, 50, 67, 50, 58)

    draw_node(ax2, 50, 54, 74, 8, "LOC TRUNG BINH TRUOT 20 MAU O(1)\nSum = Sum - RingBuf[i] + NewSample\nV_adc = (Sum / 20) * 3.3 / 4095", shape='rect', bg='#E2E8F0')
    draw_arrow(ax2, 50, 50, 50, 41)

    draw_node(ax2, 50, 37, 74, 8, "DOC NHIET DO NUOC & BU NHIET DO\nDoc DS18B20 1-Wire -> T_water\nV_comp = V_adc / [1.0 + 0.02 * (T_water - 25.0)]", shape='rect')
    draw_arrow(ax2, 50, 33, 50, 24)

    draw_node(ax2, 50, 20, 74, 8, "TINH TOAN NONG DO TDS (DA THUC BAC 3)\nTDS = (133.42*V^3 - 255.86*V^2 + 857.39*V) * 0.5", shape='rect')
    draw_arrow(ax2, 50, 16, 50, 8)

    draw_node(ax2, 50, 5, 70, 6, "GHI DE VAO LENGTH-1 MAILBOX\nxQueueOverwrite(sensorMailbox, &telemetry)", shape='rect', bg='#F1F5F9')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'fig_flowchart.png')
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Generated {out_path}")

def generate_iot_protocol_diagram():
    """Generates the Telegram Bot & UART Framing protocol sequence diagram."""
    fig, ax = plt.subplots(figsize=(11, 4.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis('off')

    # Top: Protocol Framing Box
    rect_hdr = patches.FancyBboxPatch((5, 33), 90, 14, boxstyle="round,pad=0.2",
                                      facecolor='#F8FAFC', edgecolor='#1E293B', linewidth=1.2)
    ax.add_patch(rect_hdr)
    ax.text(50, 44.5, "CAU TRUC KHUNG TRUYEN UART 2 CHIEU GIUA STM32 VA ESP32", ha='center', va='center',
            fontsize=9.5, fontweight='bold', color='#0F172A')

    # Frame blocks
    # Delimiter Start
    p1 = patches.Rectangle((8, 35.5), 10, 6.5, facecolor='#E2E8F0', edgecolor='#1E293B', lw=1.2)
    ax.add_patch(p1)
    ax.text(13, 38.8, "START\n'~' (0x7E)", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#0F172A')

    # Payload
    p2 = patches.Rectangle((20, 35.5), 60, 6.5, facecolor='#FFFFFF', edgecolor='#1E293B', lw=1.2)
    ax.add_patch(p2)
    ax.text(50, 39.5, "DULIEU TAI (PAYLOAD):\nLenh dieu khien: 'feed' / 'status'   HOAC   Ban tin JSON Telemetry: {\"tds_ppm\":185.2, ...}",
            ha='center', va='center', fontsize=7.5, color='#0F172A')

    # Delimiter End
    p3 = patches.Rectangle((82, 35.5), 10, 6.5, facecolor='#E2E8F0', edgecolor='#1E293B', lw=1.2)
    ax.add_patch(p3)
    ax.text(87, 38.8, "END\n'~' (0x7E)", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#0F172A')

    # Bottom: Communication Sequence
    # Lifelines
    entities = [
        (15, "TELEGRAM APP\n(Mobile User)"),
        (45, "TELEGRAM CLOUD\n(api.telegram.org)"),
        (72, "ESP32 IOT BRIDGE\n(FreeRTOS Co-Proc)"),
        (92, "STM32 NUCLEO\n(Core Controller)")
    ]

    for x, label in entities:
        ax.text(x, 26, label, ha='center', va='center', fontsize=8.0, fontweight='bold', color='#0F172A')
        ax.plot([x, x], [4, 22], color='#94A3B8', linestyle='--', lw=1.0)

    # Sequence Messages
    seq_msgs = [
        (15, 45, 19, "1. Gui lenh /feed", '#0F172A', '->'),
        (72, 45, 15, "2. HTTPS Long-Polling (Port 443)", '#334155', '->'),
        (72, 92, 11, "3. UART1: ~feed~ (115200 bps)", '#0F172A', '->'),
        (92, 72, 7, "4. Telemetry JSON cap nhat", '#334155', '->'),
        (72, 15, 3, "5. Xac nhan cho an da thuc hien", '#0F172A', '->')
    ]

    for x1, x2, y, text, col, style in seq_msgs:
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle=f'{style},head_width=0.3,head_length=0.45', color=col, lw=1.2))
        mid_x = (x1 + x2) / 2
        ax.text(mid_x, y + 1.2, text, ha='center', va='center', fontsize=7.2, fontweight='bold', color=col)

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'fig_iot_protocol.png')
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Generated {out_path}")

def generate_hardware_schematic():
    """Generates the hardware connection topology & protection circuit schematic."""
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 65)
    ax.axis('off')

    def draw_box(x, y, w, h, title, items=[], bg='#F8FAFC', border='#1E293B', lw=1.2, title_size=9.0, body_size=7.5):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.25",
                                      facecolor=bg, edgecolor=border, linewidth=lw)
        ax.add_patch(rect)
        ax.text(x + w/2.0, y + h - 2.5, title, ha='center', va='center',
                fontsize=title_size, fontweight='bold', color='#0F172A')
        curr_y = y + h - 5.0
        for item in items:
            ax.text(x + 1.2, curr_y, item, ha='left', va='center',
                    fontsize=body_size, color='#334155')
            curr_y -= 2.4

    # Top banner: Power Distribution
    draw_box(4, 50, 112, 13, "SO DO PHAN PHOI NGUON DIEN & CACH LY MAT DAT (COMMON GROUND TOPOLOGY)", [
        "Nguon chinh: Adapter 9V/12V DC (Chan tron 5.5x2.1mm) -> Module on ap Breadboard MB102 (AMS1117-5.0 & AMS1117-3.3)",
        "Duong nguon 5.0V: Cap cho Servo SG90, Module Ro-le 5V, Active Buzzer 5V, LCD 2004 va Chan VIN cua ESP32",
        "Duong nguon 3.3V: Cap tu chan 3V3 STM32 Nucleo cho Cam bien TDS V1.0, DS18B20, RTC DS3231 (tranh phong no pin CR2032)",
        "Quy tac song con: TOAN BO HE THONG NOI CHUNG MASS (GND) -> Dong nhat the quy chieu, triet tieu nhieu dien ap troi"
    ], bg='#F1F5F9', border='#0F172A', lw=1.5, title_size=10.0, body_size=8.0)

    # 4 Circuit Sections
    # 1. Analog & Inputs
    draw_box(4, 5, 26, 42, "1. NGO VAO ANALOG & EXT", [
        "[PA1 - ADC1_IN1]",
        "  -> Cam bien TDS Analog",
        "  -> Mac tu loc gom 0.1 uF",
        "  -> Mach loc nhieu gon song",
        "",
        "[PA4 - ADC1_IN4]",
        "  -> Bien tro xoay B10K",
        "  -> Mach chia ap tuyen tinh",
        "  -> Chinh khau phan 1g - 15g",
        "",
        "[PC13 - EXTI13]",
        "  -> Nut nhan User Button",
        "  -> Loc rung phan mem 300ms",
        "  -> Kich hoat ngat trong <1us"
    ], bg='#FFFFFF', border='#334155', lw=1.2)

    # 2. 1-Wire & I2C Bus
    draw_box(33, 5, 26, 42, "2. CHUAN BUS 1-WIRE & I2C", [
        "[PA8 - GPIO Open-Drain]",
        "  -> Cam bien DS18B20",
        "  -> Tro keo ngoai 4.7 kOhm",
        "  -> Giao thuc 1-Wire bit-bang",
        "",
        "[PB8/PB9 - I2C1 SCL/SDA]",
        "  -> Tro keo bus 4.7 kOhm",
        "  -> Man hinh LCD (0x27)",
        "  -> Module RTC (0x68)",
        "  -> EEPROM AT24C32 (0x57)",
        "  -> Chieu dung Mutex khoa bus"
    ], bg='#FFFFFF', border='#334155', lw=1.2)

    # 3. Actuator Outputs
    draw_box(62, 5, 26, 42, "3. CO CAU CHAP HANH", [
        "[PA0 - TIM2_CH1 PWM]",
        "  -> Dong co Servo SG90",
        "  -> Xung 50Hz (1.0ms - 1.5ms)",
        "  -> Quay 90 do mo cua xa cam",
        "",
        "[PB4 - GPIO Output]",
        "  -> Module Ro-le 1 kenh 5V",
        "  -> Jumper chon High Trigger",
        "  -> Dieu khien may bom nuoc",
        "",
        "[PB0 - GPIO Output]",
        "  -> Active Buzzer co dem S8050",
        "  -> Dong tieu thu chan < 1mA"
    ], bg='#FFFFFF', border='#334155', lw=1.2)

    # 4. Telemetry & Dual MCU
    draw_box(91, 5, 25, 42, "4. VIEN THONG DUAL-MCU", [
        "[PA9/PA10 - USART1]",
        "  -> Dau cheo UART1:",
        "     STM32 TX -> ESP32 RX2",
        "     STM32 RX <- ESP32 TX2",
        "  -> Baudrate: 115200 bps",
        "  -> Dinh khung: ~payload~",
        "",
        "[PA2/PA3 - USART2]",
        "  -> Cau ST-LINK USB VCP",
        "  -> Truy xuat PC Laptop",
        "  -> Kenh du phong Failsafe",
        "  -> Xuat do thi Python live"
    ], bg='#FFFFFF', border='#334155', lw=1.2)

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'fig_hardware_schematic.png')
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Generated {out_path}")

if __name__ == '__main__':
    generate_block_diagram()
    generate_hardware_schematic()
    generate_flowchart()
    generate_iot_protocol_diagram()
    generate_dsp_plots()
    generate_memory_chart()


