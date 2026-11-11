"""
==============================================================================
Project: Aquatic Guardian (Smart Fish Tank Controller & Feeder)
Subsystem: PC Terminal & ST-LINK Virtual COM Port Companion Bridge
Author: Group 7 (Class IC2005 - MCP201 Capstone)
Target: Laptop / PC over USB ST-LINK Virtual COM Port (USART2 PA2/PA3)
==============================================================================

PURPOSE & STRATEGY:
1. Primary Demo: The physical ESP32 runs Wi-Fi + Telegram Bot on USART1 (PA9/PA10)
   to secure the teacher's bonus points.
2. Failsafe / Backup Demo: If university campus Wi-Fi drops or blocks ports,
   this Python script runs on the laptop connected to the STM32 via USB ST-LINK.
   It displays a rich, live console/dashboard so the defense NEVER fails!

REQUIREMENTS:
    pip install pyserial colorama
"""

import sys
import time
import json
import serial
import serial.tools.list_ports

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    # Fallback if colorama is not installed
    class Fore:
        GREEN = RED = YELLOW = CYAN = MAGENTA = WHITE = BLUE = RESET = ""
    class Style:
        BRIGHT = RESET_ALL = ""

FRAME_DELIMITER = b'~'
DEFAULT_BAUD = 115200

def find_stlink_port():
    """Automatically detects ST-LINK Virtual COM Port."""
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        desc = (p.description or "").lower()
        mfg = (p.manufacturer or "").lower()
        if "stlink" in desc or "stmicroelectronics" in mfg or "stm" in desc:
            return p.device
    if ports:
        return ports[0].device
    return None

def parse_and_display(json_str):
    try:
        data = json.loads(json_str)
        t_sec = data.get("time", 0)
        tds = data.get("tds_ppm", 0.0)
        portion = data.get("portion_g", 0)
        temp = data.get("temp_c", 0.0)
        status = data.get("status", 0)

        if status == 0:
            st_text = f"{Fore.GREEN}[PRISTINE - IDEAL]{Style.RESET_ALL}"
        elif status == 1:
            st_text = f"{Fore.YELLOW}[ACCEPTABLE]{Style.RESET_ALL}"
        else:
            st_text = f"{Fore.RED}{Style.BRIGHT}[CRITICAL HAZARD - OVERHEAT / POLLUTED]{Style.RESET_ALL}"

        print(f"\r{Fore.CYAN}[Uptime: {t_sec:4d}s]{Style.RESET_ALL} | "
              f"TDS: {Fore.WHITE}{Style.BRIGHT}{tds:5.1f} ppm{Style.RESET_ALL} | "
              f"Temp: {Fore.YELLOW}{temp:4.1f}°C{Style.RESET_ALL} | "
              f"Portion: {portion:2d}g | Status: {st_text}", flush=True)

    except json.JSONDecodeError:
        pass

def main():
    print(f"{Fore.CYAN}{Style.BRIGHT}===================================================={Style.RESET_ALL}")
    print(f"{Fore.CYAN}{Style.BRIGHT}   AQUATIC GUARDIAN - PC TELEMETRY & BACKUP BRIDGE  {Style.RESET_ALL}")
    print(f"{Fore.WHITE}   Group 7 - MCP201 Capstone Defense Failsafe Suite   {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{Style.BRIGHT}===================================================={Style.RESET_ALL}\n")

    port = find_stlink_port()
    if not port:
        print(f"{Fore.RED}No COM ports detected! Please connect Nucleo USB cable.{Style.RESET_ALL}")
        sys.exit(1)

    print(f"{Fore.GREEN}Detected Port:{Style.RESET_ALL} {port} @ {DEFAULT_BAUD} bps")
    print(f"{Fore.YELLOW}Press 'F' + Enter to manually trigger food dispensing over USART2.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Listening for '~' framed telemetry packets...\n{Style.RESET_ALL}")

    try:
        ser = serial.Serial(port, DEFAULT_BAUD, timeout=0.1)
    except Exception as e:
        print(f"{Fore.RED}Failed to open {port}: {e}{Style.RESET_ALL}")
        sys.exit(1)

    buffer = bytearray()
    in_frame = False

    try:
        while True:
            # Non-blocking read
            raw_bytes = ser.read(64)
            if raw_bytes:
                for b in raw_bytes:
                    char_byte = bytes([b])
                    if char_byte == FRAME_DELIMITER:
                        if not in_frame:
                            in_frame = True
                            buffer.clear()
                        else:
                            in_frame = False
                            try:
                                payload = buffer.decode('utf-8', errors='ignore').strip()
                                parse_and_display(payload)
                            except Exception:
                                pass
                            buffer.clear()
                    elif in_frame:
                        if len(buffer) < 256:
                            buffer.append(b)
                        else:
                            in_frame = False
                            buffer.clear()

            time.sleep(0.01)

    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Closing serial connection... Goodbye!{Style.RESET_ALL}")
        ser.close()

if __name__ == "__main__":
    main()

