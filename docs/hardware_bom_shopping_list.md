# 🛒 Aquatic Guardian — Danh Sách Linh Kiện (BOM) & 6 Lưu Ý Phần Cứng Cốt Tử
**Dự án Capstone MCP201 — Lớp IC2005 — Nhóm 7**  
*Mã tài liệu: `BOM-AQUATIC-GUARDIAN-V2.1` | Ngày cập nhật: 2026-11-04*

---

## 🚨 6 ĐIỂM SỬA CHỮA CỐT TỬ TRONG GIỎ HÀNG (TRÁNH CHÁY & LỖI MẠCH)

Trước khi gửi đơn hàng Shopee/Lazada cho nhóm, toàn bộ 6 lỗi thực tế sau đây đã được thẩm định và xử lý triệt để:

| STT | Bẫy Phần Cứng Thực Tế | Nguy Cơ Nếu Không Sửa | Giải Pháp Đã Chốt Trong BOM |
| :---: | :--- | :--- | :--- |
| **1** | **Bẫy sụt áp IC ổn áp MB102** | Mạch nguồn MB102 dùng IC AMS1117-5.0 có độ sụt áp ~1.2V. Nếu cấp 5V vào, đầu ra chỉ còn **~3.8V**, khiến màn hình LCD2004 mờ tịt và Rơ-le 5V không đóng được. | **Dùng Adapter 9V-1A (hoặc 12V-1A) chân tròn DC 5.5x2.1mm** cắm vào cổng DC của MB102 để ra chuẩn 5.0V; HOẶC mua thêm **Module Type-C ra chân rào 5V DIP** (~5.000đ) lấy thẳng 5V-2A từ củ sạc điện thoại. |
| **2** | **Nucleo không cắm được Breadboard & ESP32 38 chân quá to** | STM32 Nucleo-64 có 2 hàng chân đực Morpho ở đáy, cắm xuống Breadboard sẽ **chập toàn bộ chân**. ESP32 bản 38 chân bè ngang che hết lỗ cắm Breadboard. | **Chỉ mua ESP32 DevKit V1 bản 30 chân**. Bổ sung **1 tép dây Cái - Cái (40 sợi)** và **1 tép Đực - Cái (40 sợi)** để câu từ chân đực trên lưng Nucleo sang Breadboard. |
| **3** | **Còi Buzzer 2 chân gây quá dòng chân chip PB0** | Còi chip 2 chân ăn dòng 25mA–35mA, vượt ngưỡng 8mA–15mA của chân GPIO `PB0` trên STM32 và sinh xung ngược làm treo vi điều khiển. | **Đổi sang Module Còi Buzzer 3 chân (VCC, GND, I/O)** (~7.000đ) tích hợp sẵn Transistor kích dòng trên bo mạch. |
| **4** | **Bẫy phồng pin CR2032 trên mạch DS3231 ZS-042** | Bo ZS-042 có mạch sạc nhồi (trở 200Ω + diode) cho pin sạc LIR2032. Nếu cấp 5V mà lắp pin không sạc CR2032 (shop hay tặng kèm) sẽ làm phồng, nổ pin hoặc chảy axit. | **Cấp nguồn 3.3V cho chân VCC của DS3231** (không cấp 5V), HOẶC dùng mỏ hàn gẩy bỏ con trở 200Ω cạnh chân SCL trên bo ZS-042 trước khi lắp pin CR2032. |
| **5** | **Rơ-le 5V kích mức Thấp bị dính trạng thái ON** | Nuôi Rơ-le 5V, khi chân PB4 xuất mức High (3.3V), độ chênh áp $5\text{V} - 3.3\text{V} = 1.7\text{V}$ vẫn làm Optocoupler dẫn nhẹ khiến Rơ-le đóng suốt không ngắt được. | **Chọn mua Module Rơ-le 1 Kênh 5V có Jumper chọn High/Low** (chuyển sang kích High); HOẶC cấu hình chân PB4 ở chế độ Open-Drain (`GPIO_MODE_OUTPUT_OD`) với trở kéo lên 5V. |
| **6** | **Thiếu trở 4.7kΩ cho DS18B20 & Nối chéo UART** | Shop bán đầu dò DS18B20 lẻ thường không kèm trở kéo 4.7kΩ. Lắp sai chân UART ESP32 làm mất giao tiếp. | **Mua thêm 1 vỉ 10 điện trở 4.7kΩ (1.000đ)**. Nối chéo: STM32 `PA9` (TX1) $\to$ ESP32 `GPIO16` (RX2); STM32 `PA10` (RX1) $\to$ ESP32 `GPIO17` (TX2). |

---

## 📋 BẢNG DANH MỤC LINH KIỆN MUA SẮM CHUẨN XÁC (FINAL BOM)

### Nhóm 1: Vi Điều Khiển & Cảm Biến Ngoại Vi
| STT | Tên Linh Kiện Chi Tiết | Từ Khóa Tìm Kiếm Chuẩn Trên Shopee / Lazada | Số Lượng | Đơn Giá Ước Tính | Mục Đích Sử Dụng |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **1** | **Mạch ESP32 DevKit V1 30 Chân** | `ESP32 DevKit V1 30 chân MicroUSB Type-C` | 1 cái | ~75.000đ – 85.000đ | IoT Wi-Fi Telegram Bot, nối `PA9`/`PA10` |
| **2** | **Cảm biến TDS Analog V1.0** | `Cảm biến TDS Analog V1.0 đo chất lượng nước` | 1 bộ | ~65.000đ – 80.000đ | Đo nồng độ chất thải/muối nối chân `PA1` |
| **3** | **Cảm biến nhiệt độ DS18B20 chống nước** | `Cảm biến nhiệt độ DS18B20 dây bọc kim loại 1m` | 1 cái | ~25.000đ – 30.000đ | Đo nhiệt độ nước bể cá nối chân `PA8` |
| **4** | **Vỉ điện trở 4.7kΩ (1/4W)** | `Điện trở 4.7k 1/4W 1% gói 10 con` | 1 gói (10c) | ~1.000đ – 2.000đ | Điện trở kéo lên (Pull-up) cho 1-Wire DS18B20 |
| **5** | **Mô-đun RTC DS3231 ZS-042 (Kèm AT24C32)** | `Mô-đun thời gian thực DS3231 AT24C32 ZS-042` | 1 cái | ~32.000đ – 40.000đ | Giờ thực RTC (`0x68`) + EEPROM lưu lịch sử (`0x57`) |
| **6** | **Pin cúc áo CR2032 (3V)** | `Pin Maxell CR2032 3V` | 1 viên | ~5.000đ – 8.000đ | Lắp cho mạch RTC DS3231 duy trì giờ khi mất điện |

### Nhóm 2: Cơ Cấu Chấp Hành & Hiển Thị
| STT | Tên Linh Kiện Chi Tiết | Từ Khóa Tìm Kiếm Chuẩn Trên Shopee / Lazada | Số Lượng | Đơn Giá Ước Tính | Mục Đích Sử Dụng |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **7** | **Màn hình LCD 2004 ĐÃ HÀN SẴN I2C** | `Màn hình LCD 2004 20x4 I2C PCF8574 xanh lá` | 1 cái | ~75.000đ – 95.000đ | Hiển thị 4 dòng thông số, chung bus I2C1 `PB8`/`PB9` |
| **8** | **Động cơ Servo SG90 (180 độ)** | `Động cơ Servo SG90 9g TowerPro kèm cánh tay` | 1 cái | ~20.000đ – 26.000đ | Gạt nắp thức ăn đóng mở nối chân `PA0` PWM |
| **9** | **Module Rơ-le 1 Kênh 5V (Có Jumper H/L)** | `Module Relay 1 kênh 5V có jumper chọn High Low` | 1 cái | ~12.000đ – 18.000đ | Đóng ngắt máy bơm nước an toàn nối chân `PB4` |
| **10**| **Module Còi Buzzer Chủ Động 3 Chân** | `Module Còi Buzzer 5V 3 chân VCC GND IO` | 1 cái | ~6.000đ – 8.000đ | Có sẵn transistor kích dòng, nối chân `PB0` an toàn |
| **11**| **Biến trở xoay 10kΩ (B10K) kèm núm** | `Biến trở đơn B10K 10k 3 chân kèm núm vặn` | 1 cái | ~3.000đ – 5.000đ | Núm vặn chỉnh định lượng thức ăn nối chân `PA4` |
| **12**| **Gói LED 5mm + Điện trở 220Ω** | `Gói 5 LED đỏ 5mm + 5 trở 220R` | 1 gói | ~3.000đ – 5.000đ | LED đỏ cảnh báo nối chân `PB1` |

### Nhóm 3: Bo Mạch Thử Nghiệm, Nguồn Cấp & Dây Cắm
| STT | Tên Linh Kiện Chi Tiết | Từ Khóa Tìm Kiếm Chuẩn Trên Shopee / Lazada | Số Lượng | Đơn Giá Ước Tính | Mục Đích Sử Dụng |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **13**| **Breadboard MB-102 (830 lỗ)** | `Breadboard MB102 830 lỗ loại tốt` | 1 cái | ~25.000đ – 32.000đ | Cắm linh kiện thử nghiệm |
| **14**| **Dây cắm Breadboard Cái - Cái (40 sợi, 20cm)** | `Dây cắm breadboard Cái Cái 20cm vỉ 40 sợi` | 1 tép (40s) | ~12.000đ – 15.000đ | **Bắt buộc**: Cắm từ chân đực Morpho của STM32 ra ngoài |
| **15**| **Dây cắm Breadboard Đực - Cái (40 sợi, 20cm)** | `Dây cắm breadboard Đực Cái 20cm vỉ 40 sợi` | 1 tép (40s) | ~12.000đ – 15.000đ | Nối giữa chân STM32/ESP32 sang lỗ cắm Breadboard |
| **16**| **Dây cắm Breadboard Đực - Đực (40 sợi, 20cm)** | `Dây cắm breadboard Đực Đực 20cm vỉ 40 sợi` | 1 tép (40s) | ~12.000đ – 15.000đ | Nối cầu giữa các hàng trên Breadboard |
| **17**| **Mạch Nguồn MB102 3.3V/5V cắm Breadboard** | `Mạch nguồn Breadboard MB102 3.3V 5V` | 1 cái | ~18.000đ – 22.000đ | Ổn áp cấp cho 2 thanh nguồn Breadboard |
| **18**| **Adapter Nguồn 9V-1A (hoặc 12V-1A) Jack DC 5.5x2.1mm** | `Adapter 9V 1A jack tròn DC 5.5x2.1mm` | 1 cái | ~30.000đ – 40.000đ | **Tránh sụt áp**: Cấp đủ áp cho MB102 xuất chuẩn 5.0V |
| *(Phụ)*| **Module Lấy Nguồn USB Type-C sang DIP 5V** | `Module Type-C DIP 5V cấp nguồn breadboard` | 1 cái | ~4.000đ – 6.000đ | Phương án thay thế: Lấy trực tiếp 5V 2A từ sạc điện thoại |

---

## 💰 TỔNG HỢP CHI PHÍ & CHIA ĐỀU CHO NHÓM

* **Tổng giá trị đơn hàng linh kiện đầy đủ**: **~390.000đ – 450.000đ**
* **Số lượng thành viên**: 5 người (Tùng, Mạnh, Gia, Minh, Đức Anh).
* **Mỗi người đóng**: **~80.000đ – 90.000đ** *(Bằng 2 cốc trà sữa, đảm bảo có đầy đủ đồ nghề chất lượng cao, không bị cháy hỏng)*.

---

## 📲 NỘI DUNG COPY GỬI NHANH VÀO NHÓM ZALO CHO BẠN MUA LINH KIỆN

```text
Anh em ơi, chốt danh sách linh kiện chuẩn của đồ án Aquatic Guardian (đã qua thẩm định kỹ thuật, tránh cháy chip và sụt áp). Nhờ Gia (hoặc bạn nào nhận mua) lên Shopee gom trong 1-2 shop lớn (như Linh Kiện Điện Tử 3M, Nshop, Hshop, Linh Kiện Cầu Giấy) để tiết kiệm tiền ship nhé:

1. ESP32 DevKit V1 (LƯU Ý: Chọn đúng bản 30 CHÂN, không lấy bản 38 chân) - 1 cái
2. Cảm biến TDS Analog V1.0 (kèm que đo + mạch giải mã) - 1 bộ
3. Cảm biến nhiệt độ DS18B20 chống nước dây dài 1m - 1 cái
4. Vỉ 10 điện trở 4.7kΩ (1/4W) - 1 vỉ (1k)
5. Mô-đun RTC DS3231 ZS-042 (đã có sẵn chip nhớ AT24C32) + 1 viên pin CR2032 - 1 bộ
6. Màn hình LCD 2004 (LƯU Ý: Chọn loại ĐÃ HÀN SẴN MODULE I2C PCF8574) - 1 cái
7. Động cơ Servo SG90 9g (180 độ) - 1 cái
8. Module Rơ-le 1 kênh 5V (LƯU Ý: Chọn loại có Jumper chỉnh High/Low) - 1 cái
9. Module Còi Buzzer Chủ Động 5V LOẠI 3 CHÂN (VCC, GND, IO) - 1 cái
10. Biến trở xoay B10K 10kΩ có núm vặn - 1 cái
11. Gói 5 LED đỏ 5mm + 5 trở 220Ω - 1 gói
12. Breadboard MB-102 (830 lỗ) - 1 cái
13. Mạch nguồn Breadboard MB-102 (3.3V/5V) - 1 cái
14. Adapter 9V-1A (hoặc 12V-1A) đầu cắm DC 5.5x2.1mm (để cấp cho mạch nguồn MB102 ra đủ 5V) - 1 cái
15. Dây cắm Breadboard:
   - 1 tép Cái - Cái (40 sợi)
   - 1 tép Đực - Cái (40 sợi)
   - 1 tép Đực - Đực (40 sợi)

Tổng thiệt hại khoảng 400k, chia 5 mỗi người ~80k. Đồ về anh em ráp mạch là chạy bon bon luôn!
```

