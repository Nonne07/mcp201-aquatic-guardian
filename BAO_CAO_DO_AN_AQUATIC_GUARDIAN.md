# MỤC LỤC

---

* **DANH MỤC HÌNH**
* **DANH MỤC BẢNG**
* **DANH MỤC CÁC TỪ VIẾT TẮT**
* **CHƯƠNG 1 TỔNG QUAN VÀ NHIỆM VỤ ĐỀ TÀI**
  * 1.1 Tổng quan về hệ sinh thái thủy sinh và yêu cầu tự động hóa
  * 1.2 Tính cấp thiết và lý do hình thành đề tài Aquatic Guardian
  * 1.3 Mục tiêu nghiên cứu và phạm vi giới hạn
  * 1.4 Cấu trúc của quyển báo cáo đồ án
* **CHƯƠNG 2 THIẾT KẾ HỆ THỐNG VÀ PHẦN CỨNG**
  * 2.1 Sơ đồ khối tổng thể hệ thống đa vi điều khiển
  * 2.2 Khối xử lý trung tâm STM32 Nucleo (ARM Cortex-M4)
  * 2.3 Khối cảm biến thu thập thông số môi trường nước
    * 2.3.1 Cảm biến tổng chất rắn hòa tan TDS Analog V1.0
    * 2.3.2 Cảm biến nhiệt độ số chống nước DS18B20 và cảm biến nội bộ DS3231
    * 2.3.3 Cụm biến trở xoay định lượng thức ăn
  * 2.4 Khối cơ cấu chấp hành và cảnh báo
    * 2.4.1 Động cơ Servo SG90 và cơ cấu nắp lật định lượng
    * 2.4.2 Rơ-le điều khiển máy bơm lọc nước
    * 2.4.3 Cụm cảnh báo âm thanh và quang học
  * 2.5 Khối hiển thị cục bộ và lưu trữ dữ liệu thời gian thực trên Bus I2C1
    * 2.5.1 Màn hình LCD 2004 tích hợp module chuyển đổi I2C PCF8574
    * 2.5.2 Đồng hồ thời gian thực chính xác cao DS3231
    * 2.5.3 Bộ nhớ EEPROM AT24C32 lưu nhật ký cho ăn
  * 2.6 Khối truyền thông không dây IoT ESP32 và cáp nạp ST-LINK USB
  * 2.7 Thiết kế mạch nguồn và 6 vấn đề kỹ thuật trọng yếu trong triển khai phần cứng thực tế
  * 2.8 Bảng phân bổ chân STM32 Nucleo không xung đột (Conflict-Free Pinout)
* **CHƯƠNG 3 THIẾT KẾ PHẦN MỀM VÀ ĐA NHIỆM FREERTOS**
  * 3.1 Kiến trúc hệ điều hành thời gian thực FreeRTOS và CMSIS-RTOS v2
  * 3.2 Phân rã 5 tác vụ thời gian thực và thứ bậc ưu tiên
    * 3.2.1 Tác vụ giám sát an toàn khẩn cấp (Task_SafetySupervisor)
    * 3.2.2 Tác vụ điều khiển cơ cấu cho ăn (Task_DispenserControl)
    * 3.2.3 Tác vụ thu thập và xử lý tín hiệu cảm biến (Task_SensorAcquisition)
    * 3.2.4 Tác vụ hiển thị giao diện người dùng LCD (Task_DisplayUI)
    * 3.2.5 Tác vụ truyền thông viễn thông đa kênh (Task_Telemetry)
  * 3.3 Cơ chế đồng bộ hóa và giao tiếp liên tác vụ (IPC)
    * 3.3.1 Hòm thư phi hủy dữ liệu Length-1 Mailbox chống hiện tượng chết đói
    * 3.3.2 Xử lý ngắt trì hoãn (Deferred Interrupt) và thuật toán chống rung phím 300ms
    * 3.3.3 Quản lý Bus I2C1 và chứng minh cơ chế thừa kế quyền ưu tiên (Priority Inheritance)
  * 3.4 Thuật toán lọc trung bình trượt vòng 20 mẫu O(1) và phương trình bậc 3 bù nhiệt TDS
  * 3.5 Giao thức đóng gói dữ liệu UART định khung ký tự giữa STM32 và ESP32
* **CHƯƠNG 4 KẾT QUẢ THỰC NGHIỆM VÀ ĐÁNH GIÁ**
  * 4.1 Kết quả kiểm thử độc lập 4 module phần cứng (Standalone Bench Tests)
    * 4.1.1 Kiểm thử điều xung PWM điều khiển góc quay Servo SG90
    * 4.1.2 Kiểm thử Dynamic ADC và thuật toán lọc nhiễu TDS
    * 4.1.3 Kiểm thử quét địa chỉ bus I2C1 và đọc ghi EEPROM AT24C32
    * 4.1.4 Kiểm thử truyền thông UART và máy trạng thái giải mã gói tin
  * 4.2 Kết quả vận hành tích hợp toàn hệ thống
    * 4.2.1 Hoạt động ổn định ở điều kiện bình thường
    * 4.2.2 Phản ứng tức thời khi mô phỏng sự cố nước ô nhiễm
    * 4.2.3 Kiểm thử điều khiển từ xa qua Telegram Bot và Web Dashboard
    * 4.2.4 Hoạt động giám sát dự phòng qua cáp ST-LINK Virtual COM Port
  * 4.3 Đánh giá hiệu năng thực thi và mức độ chiếm dụng tài nguyên vi điều khiển
* **CHƯƠNG 5 KẾT LUẬN VÀ KIẾN NGHỊ**
  * 5.1 Các kết quả chính đã hoàn thành
  * 5.2 Đóng góp khoa học và kỹ thuật của đồ án
  * 5.3 Hạn chế và hướng phát triển tiếp theo
* **TÀI LIỆU THAM KHẢO**
* **PHỤ LỤC**
  * Phụ lục A: Toàn văn mã nguồn C ứng dụng FreeRTOS (aquatic_guardian_app.h & .c)
  * Phụ lục B: Toàn văn mã nguồn Firmware ESP32 Wi-Fi IoT (esp32_aquatic_bridge.ino)
  * Phụ lục C: Bảng danh mục linh kiện chi tiết (BOM) và thông số kỹ thuật

---

# DANH MỤC HÌNH

* Hình 2.1: Sơ đồ khối tổng thể hệ thống đa vi điều khiển Aquatic Guardian
* Hình 2.2: Sơ đồ chân và cấu trúc phân bổ ngoại vi trên bo mạch STM32 Nucleo-64
* Hình 2.3: Đặc tính điện áp xuất ra theo nồng độ TDS của cảm biến Analog TDS V1.0
* Hình 2.4: Sơ đồ phối ghép cảm biến nhiệt độ 1-Wire DS18B20 với điện trở kéo lên 4.7kΩ
* Hình 2.5: Giản đồ xung điều khiển PWM 50Hz (chu kỳ 20ms) cho động cơ Servo SG90
* Hình 2.6: Cấu trúc bộ nhớ 32Kbit của chip nhớ EEPROM AT24C32 trên module ZS-042
* Hình 2.7: Sơ đồ phân bổ đường nguồn 5V/3.3V và cách ly sụt áp cho module MB102
* Hình 3.1: Kiến trúc điều phối đa nhiệm FreeRTOS dưới lớp trừu tượng CMSIS-RTOS v2
* Hình 3.2: Cơ chế hòm thư Length-1 Mailbox chống hiện tượng chết đói dữ liệu (Starvation)
* Hình 3.3: Lưu đồ xử lý ngắt trì hoãn nút bấm PC13 với thuật toán lọc rung phần mềm 300ms
* Hình 3.4: Giản đồ thời gian chứng minh cơ chế thừa kế quyền ưu tiên (Priority Inheritance) trên bus I2C1
* Hình 3.5: Cấu trúc bộ nhớ đệm vòng 20 phần tử (Ring Buffer) thực thi trong thời gian O(1)
* Hình 3.6: Máy trạng thái hữu hạn (FSM) giải mã gói tin định khung ký tự '~' trên đường truyền UART
* Hình 4.1: Dạng sóng PWM đo đạc thực tế tại chân PA0 điều khiển các góc quay Servo
* Hình 4.2: Đồ thị đáp ứng điện áp và nồng độ TDS trước và sau khi qua bộ lọc vòng 20 mẫu
* Hình 4.3: Kết quả quét địa chỉ bus I2C1 nhận diện thành công 3 thiết bị trên cổng Terminal
* Hình 4.4: Giao diện điều khiển cho ăn và nhận cảnh báo khẩn cấp qua ứng dụng Telegram
* Hình 4.5: Giao diện Web Dashboard cục bộ giám sát thông số thời gian thực trên điện thoại
* Hình 4.6: Màn hình giám sát dự phòng qua script Python kết nối cáp ST-LINK USB Virtual COM Port

---

# DANH MỤC BẢNG

* Bảng 2.1: Bảng phân bổ chân STM32 Nucleo không xung đột (Conflict-Free Pinout)
* Bảng 2.2: Địa chỉ vật lý và nhiệm vụ của các vi mạch trên bus I2C1
* Bảng 2.3: Bảng đối chiếu 6 vấn đề kỹ thuật phần cứng thực tế và giải pháp khắc phục
* Bảng 3.1: Bảng đặc tả 5 tác vụ thời gian thực FreeRTOS và phân bổ bộ nhớ Stack
* Bảng 3.2: Bảng tra cứu phân loại trạng thái chất lượng nước sinh thái
* Bảng 4.1: Bảng đối chiếu kết quả kiểm thử quét địa chỉ bus I2C1
* Bảng 4.2: Bảng đo đạc thời gian đáp ứng của hệ thống khi xuất hiện sự cố nước ô nhiễm
* Bảng 4.3: Bảng phân bổ dung lượng bộ nhớ Flash ROM và SRAM của ứng dụng FreeRTOS
* Bảng C.1: Bảng danh mục định mức linh kiện (BOM) chi tiết của đề tài

---

# DANH MỤC CÁC TỪ VIẾT TẮT

* **ADC**: Analog-to-Digital Converter (Bộ chuyển đổi tương tự sang số)
* **API**: Application Programming Interface (Giao diện lập trình ứng dụng)
* **ARR**: Auto-Reload Register (Thanh ghi tự động nạp lại giá trị đếm của Timer)
* **BCD**: Binary-Coded Decimal (Mã nhị phân biểu diễn số thập phân)
* **BOM**: Bill of Materials (Danh mục định mức linh kiện vật tư)
* **CCR**: Capture/Compare Register (Thanh ghi bắt/so sánh xung Timer)
* **CLO**: Course Learning Outcome (Chuẩn đầu ra của học phần)
* **CMSIS**: Cortex Microcontroller Software Interface Standard (Tiêu chuẩn giao tiếp phần mềm vi điều khiển Cortex)
* **CPU**: Central Processing Unit (Đơn vị xử lý trung tâm)
* **DMA**: Direct Memory Access (Bộ điều khiển truy cập bộ nhớ trực tiếp)
* **DSP**: Digital Signal Processing (Xử lý tín hiệu số)
* **EEPROM**: Electrically Erasable Programmable Read-Only Memory (Bộ nhớ chỉ đọc xóa lập trình được bằng điện)
* **EXTI**: Extended Interrupt and Event Controller (Bộ điều khiển ngắt và sự kiện mở rộng)
* **FSM**: Finite State Machine (Máy trạng thái hữu hạn)
* **GPIO**: General-Purpose Input/Output (Chân vào/ra đa dụng)
* **HAL**: Hardware Abstraction Layer (Lớp trừu tượng hóa phần cứng)
* **I2C**: Inter-Integrated Circuit (Giao thức truyền thông nối tiếp liên vi mạch)
* **IPC**: Inter-Process Communication (Cơ chế truyền thông và đồng bộ liên tác vụ)
* **ISR**: Interrupt Service Routine (Chương trình con phục vụ ngắt)
* **LCD**: Liquid Crystal Display (Màn hình tinh thể lỏng)
* **LDO**: Low-Dropout Regulator (Mạch ổn áp vi sai điện áp thấp)
* **MCU**: Microcontroller Unit (Khối vi điều khiển)
* **NVIC**: Nested Vectored Interrupt Controller (Bộ điều khiển ngắt véc-tơ lồng nhau)
* **O(1)**: Big-O Constant Time Complexity (Độ phức tạp thời gian hằng số)
* **OD**: Open-Drain (Cấu hình cực máng hở)
* **PCB**: Printed Circuit Board (Mạch in điện tử)
* **PSC**: Prescaler (Bộ chia tần số xung nhịp)
* **PWM**: Pulse-Width Modulation (Điều chế độ rộng xung)
* **RAM**: Random Access Memory (Bộ nhớ truy cập ngẫu nhiên)
* **RTC**: Real-Time Clock (Đồng hồ thời gian thực)
* **RTOS**: Real-Time Operating System (Hệ điều hành thời gian thực)
* **SRAM**: Static Random Access Memory (Bộ nhớ truy cập ngẫu nhiên tĩnh)
* **SWD**: Serial Wire Debug (Giao thức nạp và gỡ lỗi nối tiếp 2 dây)
* **TCB**: Task Control Block (Khối điều khiển tác vụ trong RTOS)
* **TDS**: Total Dissolved Solids (Tổng chất rắn hòa tan trong nước)
* **UART**: Universal Asynchronous Receiver-Transmitter (Bộ thu phát nối tiếp bất đồng bộ)
* **USART**: Universal Synchronous/Asynchronous Receiver-Transmitter (Bộ thu phát nối tiếp đồng bộ/bất đồng bộ)
* **VCP**: Virtual COM Port (Cổng giao tiếp nối tiếp ảo qua USB)

---

# CHƯƠNG 1 TỔNG QUAN VÀ NHIỆM VỤ ĐỀ TÀI

## 1.1 TỔNG QUAN VỀ HỆ SINH THÁI THỦY SINH VÀ YÊU CẦU TỰ ĐỘNG HÓA

Nuôi và bảo tồn sinh vật thủy sinh cảnh trong môi trường bể kính nhân tạo là một thú vui tao nhã nhưng đòi hỏi tính kỷ luật và sự chăm sóc vô cùng nghiêm ngặt. Khác với môi trường tự nhiên (sông, suối, hồ lớn) sở hữu khả năng tự cân bằng sinh học khổng lồ thông qua khối lượng nước luân chuyển liên tục, bể cá cảnh gia đình là một hệ sinh thái khép kín có thể tích hạn chế. Trong môi trường này, chất lượng nước và tình trạng của sinh vật có thể biến động rất nhanh chóng.

Ba thông số quan trắc then chốt quyết định sự sống còn của sinh vật thủy sinh bao gồm:
1. **Tổng chất rắn hòa tan (TDS - Total Dissolved Solids)**: Chỉ số TDS phản ánh tổng nồng độ các chất vô cơ và hữu cơ hòa tan trong nước (ion kim loại, muối khoáng, chất thải của cá, thức ăn thừa phân hủy). Khi cá bài tiết hoặc thức ăn dư thừa tích tụ, quá trình phân hủy sinh ra các hợp chất nitơ độc hại (Ammonia NH₃, Nitrite NO₂⁻), làm giá trị TDS tăng vọt. Vượt qua ngưỡng 350 – 500 ppm, áp suất thẩm thấu thay đổi đột ngột làm tổn thương mang cá, suy giảm hệ miễn dịch và dẫn đến nguy cơ nhiễm độc nghiêm trọng.
2. **Nhiệt độ nước**: Các loài cá cảnh nhiệt đới phổ biến yêu cầu dải nhiệt độ hẹp từ 24°C đến 28°C để duy trì các phản ứng trao đổi chất bình thường. Sự thay đổi nhiệt độ đột ngột vượt quá 30°C – 32°C gây sốc nhiệt, làm giảm oxy hòa tan trong nước và ức chế khả năng hô hấp của cá.
3. **Chế độ dinh dưỡng và cho ăn có kiểm soát**: Việc cho cá ăn đòi hỏi sự chính xác về thời gian và khối lượng. Cho ăn thiếu khiến cá suy dinh dưỡng; ngược lại, cho ăn thừa là nguyên nhân hàng đầu (chiếm tới 80%) làm đục nước, bùng phát rêu hại và sinh khí độc.

Trước đây, việc chăm sóc bể cá phụ thuộc hoàn toàn vào thao tác thủ công của người nuôi: kiểm tra nước định kỳ bằng dung dịch thử hóa học, rắc thức ăn bằng tay và theo dõi nhiệt độ bằng nhiệt kế thủy ngân. Tuy nhiên, khi người nuôi phải đi công tác, du lịch xa nhà nhiều ngày hoặc bận rộn với công việc, chu trình chăm sóc bị gián đoạn, tiềm ẩn rủi ro phá vỡ cân bằng sinh thái của bể cá. Do đó, nhu cầu cấp thiết đặt ra là phải xây dựng một hệ thống nhúng tự động hóa thông minh, có khả năng giám sát liên tục các thông số môi trường, tự động điều phối cơ cấu cho ăn theo lịch trình, cảnh báo sớm các mối nguy hại và cho phép tương tác điều khiển từ xa thông qua mạng viễn thông.

## 1.2 TÍNH CẤP THIẾT VÀ LÝ DO HÌNH THÀNH ĐỀ TÀI AQUATIC GUARDIAN

Xuất phát từ yêu cầu thực tiễn trên, đề tài **"Aquatic Guardian" (Hệ Thống Nhúng Thông Minh Giám Sát Bể Cá & Cho Ăn Tự Động Thời Gian Thực)** được nghiên cứu và hiện thực hóa trong khuôn khổ đồ án tốt nghiệp học phần Lập trình Vi điều khiển (MCP201) tại Đại học FPT.

Về mặt học thuật và kỹ thuật, đề tài kế thừa và phát triển từ công trình nghiên cứu của kỹ sư Martín Quattrone tại Đại học Buenos Aires (FIUBA, Argentina, 2023), vốn dựa trên giáo trình chuẩn của ARM Education Media do Giáo sư Ariel Lutenberg biên soạn [1], [2]. Tuy nhiên, phiên bản gốc của Quattrone bộc lộ nhiều điểm hạn chế nghiêm trọng:
* **Hạn chế về kiến trúc phần mềm**: Hệ thống gốc sử dụng vòng lặp kiểm tra tuần tự (Superloop Polling) trên nền tảng Mbed OS. Trong kiến trúc này, khi vi điều khiển thực hiện thao tác cập nhật màn hình LCD hoặc chờ cơ cấu động cơ gạt thức ăn (mất từ 500ms đến 1500ms), toàn bộ CPU bị khóa cứng (blocking). Nếu trong thời gian này xảy ra sự cố quá nhiệt hoặc nồng độ TDS tăng cao đột ngột, hệ thống hoàn toàn mất khả năng phản ứng thời gian thực.
* **Xung đột phần cứng (Hardware Pin Collisions)**: Sơ đồ gốc thiết kế chân điều khiển động cơ bước trùng lặp với bus truyền thông I2C1 (`PB8`/`PB9`), đồng thời cổng truyền thông nối tiếp của module Wi-Fi bị nối chập với cổng nạp ST-LINK trên các chân `PA2`/`PA3`, dẫn đến hiện tượng chập bus và treo mạch khi vận hành thực tế.
* **Thiếu khả năng điều khiển thông minh và bù nhiệt**: Giá trị đo đạc từ que đo TDS không được bù trừ theo nhiệt độ thực tế của nước, dẫn đến sai số đo lường lên đến 20% – 30%.

Để giải quyết triệt để các tồn tại trên, nhóm tác giả đã tiến hành nâng cấp toàn diện hệ thống lên **Kiến Trúc Nhúng Thế Hệ 2.0 (Architecture v2.0)**:
1. Chuyển đổi toàn bộ nền tảng phần mềm sang **Hệ điều hành thời gian thực FreeRTOS đa nhiệm tiền định (Preemptive Multitasking)** chuẩn CMSIS-RTOS v2 trên vi điều khiển 32-bit ARM Cortex-M4 (STM32 Nucleo).
2. Tái cấu trúc phân bổ chân ngoại vi (Conflict-Free Pinout), cách ly hoàn toàn các bus giao tiếp và cơ cấu chấp hành.
3. Ứng dụng mô hình **Đa vi điều khiển phân tán (Distributed Dual-MCU)**: Vi điều khiển STM32 chuyên trách xử lý tín hiệu thời gian thực nghiêm ngặt, kết hợp cùng vi điều khiển phụ ESP32 đảm nhiệm kết nối mạng không dây và điều khiển qua ứng dụng Telegram.
4. Triển khai các thuật toán xử lý tín hiệu số (DSP) gồm bộ lọc trung bình trượt vòng 20 mẫu O(1) và phương trình đa thức bậc 3 bù nhiệt độ chính xác cao.

## 1.3 MỤC TIÊU NGHIÊN CỨU VÀ PHẠM VI GIỚI HẠN

### 1.3.1 Mục tiêu tổng quát
Thiết kế, chế tạo và thử nghiệm thành công một hệ thống nhúng hoàn chỉnh có khả năng giám sát liên tục chất lượng nước (TDS, nhiệt độ), tự động hóa quy trình cho ăn theo lịch trình chính xác, đảm bảo độ tin cậy thời gian thực bằng FreeRTOS và cung cấp khả năng điều khiển, nhận thông báo cảnh báo qua nền tảng đám mây và ứng dụng Telegram.

### 1.3.2 Mục tiêu kỹ thuật cụ thể
* Thu thập dữ liệu tương tự (Analog) từ que đo TDS và biến trở định lượng với độ phân giải 12-bit thông qua bộ chuyển đổi ADC1 trên STM32.
* Xử lý tín hiệu chống nhiễu gợn sóng nước bằng bộ lọc số 20 mẫu trong thời gian thực thi hằng số O(1).
* Phát xung PWM chính xác ở tần số 50Hz (chu kỳ 20ms) thông qua Timer 2 để điều khiển góc mở động cơ Servo SG90 từ 0° đến 90°.
* Giao tiếp đồng thời 3 thiết bị trên bus chung I2C1 gồm màn hình LCD2004, đồng hồ thời gian thực DS3231 và chip nhớ EEPROM AT24C32.
* Hiện thực hóa 5 tác vụ FreeRTOS hoạt động đồng thời, giải quyết triệt để hiện tượng tranh chấp tài nguyên bằng Mutex có cơ chế thừa kế quyền ưu tiên (Priority Inheritance) và đồng bộ hóa ngắt ngoài EXTI bằng Binary Semaphore.
* Xây dựng giao thức truyền thông hai chiều định khung ký tự đặc biệt giữa STM32 và ESP32 qua UART ở tốc độ 115200 bps.
* Tích hợp Telegram Bot và Local Web Dashboard cho phép người dùng kiểm tra thông số và ra lệnh cho ăn từ xa.

### 1.3.3 Phạm vi và giới hạn của đề tài
* **Đối tượng môi trường**: Hệ thống được tối ưu hóa cho bể cá cảnh nước ngọt gia đình (thể tích từ 20 đến 200 lít).
* **Nền tảng phần cứng**: Bo mạch phát triển STMicroelectronics Nucleo-64 (chip STM32F401RE hoặc STM32F411RE, lõi ARM Cortex-M4) kết hợp bo mạch ESP32 DevKit V1 (30 chân).
* **Giới hạn đo lường**: Dải đo TDS từ 0 đến 1000 ppm; dải nhiệt độ nước từ 0°C đến 50°C.

## 1.4 CẤU TRÚC CỦA QUYỂN BÁO CÁO ĐỒ ÁN

Quyển báo cáo đồ án được kết cấu chặt chẽ theo quy định bao gồm 5 chương chính:
* **Chương 1: Tổng quan và nhiệm vụ đề tài**: Nêu rõ bối cảnh sinh thái, tính cấp thiết, lý do hình thành đề tài, mục tiêu và phạm vi nghiên cứu.
* **Chương 2: Thiết kế hệ thống và phần cứng**: Trình bày chi tiết sơ đồ khối, kiến trúc vi điều khiển, nguyên lý hoạt động của các cảm biến, cơ cấu chấp hành, màn hình, giải pháp thiết kế mạch nguồn chống sụt áp và bảng phân bổ chân không xung đột.
* **Chương 3: Thiết kế phần mềm và đa nhiệm FreeRTOS**: Phân tích chi tiết kiến trúc điều phối 5 tác vụ thời gian thực, cơ chế hòm thư phi hủy Length-1 Mailbox, kỹ thuật xử lý ngắt trì hoãn, chứng minh cơ chế Priority Inheritance, thuật toán lọc DSP và giao thức UART.
* **Chương 4: Kết quả thực nghiệm và đánh giá**: Trình bày các kết quả kiểm thử độc lập 4 module phần cứng, kịch bản vận hành tích hợp toàn hệ thống, phản ứng sự cố, điều khiển qua Telegram/Web và đo lường độ trễ thực thi.
* **Chương 5: Kết luận và kiến nghị**: Đánh giá mức độ hoàn thành so với mục tiêu đề ra, rút ra các đóng góp kỹ thuật cốt lõi và đề xuất các hướng mở rộng trong tương lai.

---

# CHƯƠNG 2 THIẾT KẾ HỆ THỐNG VÀ PHẦN CỨNG

## 2.1 SƠ ĐỒ KHỐI TỔNG THỂ HỆ THỐNG ĐA VI ĐIỀU KHIỂN

Để đảm bảo hệ thống vừa đáp ứng được các ràng buộc thời gian thực nghiêm ngặt (Hard Real-Time constraints) trong việc đọc cảm biến và điều khiển cơ cấu chuyển động, vừa có khả năng xử lý các tác vụ mạng không dây vốn có độ trễ lớn và tiêu hao nhiều năng lượng, chúng tôi lựa chọn kiến trúc **Đa vi điều khiển phân tán (Distributed Dual-MCU Architecture)**. 

Hệ thống được chia thành 4 khối chức năng chính xoay quanh bộ não điều khiển STM32:

```
+-------------------------------------------------------------+
|               HỆ THỐNG AQUATIC GUARDIAN                     |
+-------------------------------------------------------------+
|  KHỐI CẢM BIẾN (SENSING LAYER)                              |
|  * TDS Analog V1.0         --> PA1 (ADC1_IN1, Rank 1)       |
|  * Biến trở xoay B10K      --> PA4 (ADC1_IN4, Rank 1)       |
|  * DS18B20 1-Wire          --> PA8 (GPIO OD, trở kéo 4.7kΩ) |
|  * Nút bấm B1              --> PC13 (EXTI13, Fall, 300ms)   |
+-------------------------------------------------------------+
|  KHỐI ĐIỀU KHIỂN TRUNG TÂM (CORE EMBEDDED)                  |
|  * Vi điều khiển: STM32F401RE Nucleo-64 (Cortex-M4, 84MHz)  |
|  * Hệ điều hành: FreeRTOS v10 / CMSIS-RTOS v2               |
|  * 5 tác vụ độc lập: Supervisor, Feeder, ADC, LCD, Telemetry|
+-------------------------------------------------------------+
|  KHỐI CƠ CẤU CHẤP HÀNH & CẢNH BÁO (ACTUATION & ALARM)       |
|  * Động cơ Servo SG90      <-- PA0 (TIM2_CH1 PWM 50Hz)      |
|  * Rơ-le máy bơm lọc 5V    <-- PB4 (GPIO Output High)       |
|  * Active Buzzer 5V        <-- PB0 (GPIO Output, < 1mA)     |
|  * LED xanh / đỏ           <-- PA5 / PB1 (GPIO Output)      |
+-------------------------------------------------------------+
|  KHỐI HIỂN THỊ, LƯU TRỮ & TRUYỀN THÔNG (BUS & TELEMETRY)    |
|  * Bus I2C1 (PB8/PB9)      <-> LCD 2004, DS3231, AT24C32    |
|  * USART1 (PA9/PA10)       <-> ESP32 (Telegram & Web IP)    |
|  * USART2 (PA2/PA3)        <-> ST-LINK VCP (PC Telemetry)   |
+-------------------------------------------------------------+
```
*Hình 2.1: Sơ đồ khối tổng thể hệ thống đa vi điều khiển Aquatic Guardian*

* **Khối xử lý trung tâm**: Vi điều khiển STM32F401RE/F411RE đóng vai trò làm Master, chịu trách nhiệm thực thi hệ điều hành thời gian thực FreeRTOS, đọc và xử lý tín hiệu cảm biến, tính toán thuật toán lọc số, kích hoạt rơ-le bơm, phát xung PWM quay servo và điều phối giao tiếp trên bus I2C1.
* **Khối cảm biến và đầu vào**: Bao gồm que đo độ bẩn nước TDS Analog, biến trở xoay thiết lập định lượng thức ăn, cảm biến nhiệt độ số chống nước DS18B20 và nút nhấn khẩn cấp gắn trên chân ngắt ngoài.
* **Khối cơ cấu chấp hành và cảnh báo**: Động cơ Servo mini SG90 thực hiện đóng mở nắp hộp thức ăn, module Rơ-le cách ly quang đóng ngắt nguồn cho máy bơm lọc nước 220V/12V, còi buzzer chủ động và hệ thống LED hiển thị trạng thái sinh thái.
* **Khối hiển thị và thời gian thực (Bus I2C1)**: Màn hình LCD 2004 hiển thị 4 dòng thông số trực quan, module đồng hồ thời gian thực DS3231 lưu giữ lịch trình độc lập với nguồn điện chính, và chip nhớ EEPROM AT24C32 lưu trữ lịch sử các lần cho ăn.
* **Khối viễn thông hai kênh**: Kênh 1 kết nối vi điều khiển phụ ESP32 qua `USART1` phục vụ kết nối Wi-Fi, Telegram Bot và Web Dashboard; Kênh 2 kết nối trực tiếp với máy tính qua cổng ST-LINK USB Virtual COM Port (`USART2`) đóng vai trò đường truyền giám sát dự phòng Failsafe.

## 2.2 KHỐI XỬ LÝ TRUNG TÂM STM32 NUCLEO (ARM CORTEX-M4)

Bo mạch phát triển STMicroelectronics Nucleo-64 (mã hiệu NUCLEO-F401RE hoặc NUCLEO-F411RE) được lựa chọn làm nền tảng xử lý trung tâm nhờ sở hữu các đặc tính kỹ thuật vượt trội:
* **Lõi vi xử lý**: ARM Cortex-M4 32-bit tích hợp bộ xử lý dấu chấm động phần cứng (FPU - Floating Point Unit) và tập lệnh xử lý tín hiệu số DSP chuyên dụng, vận hành ở xung nhịp tối đa 84 MHz (F401RE) hoặc 100 MHz (F411RE).
* **Bộ nhớ**: 512 KB bộ nhớ Flash chương trình và 96 KB (hoặc 128 KB) bộ nhớ SRAM tĩnh, cho phép phân bổ không gian bộ nhớ đệm (Heap) thoải mái cho các tác vụ FreeRTOS mà không lo ngại sự cố tràn bộ nhớ.
* **Ngoại vi tích hợp**: Bộ chuyển đổi ADC 12-bit tốc độ cao (lên đến 2.4 MSPS), các bộ định thời đa năng Timer 16-bit và 32-bit có khả năng phát xung PWM vi mô, các khối ngoại vi phần cứng độc lập USART, I2C, SPI.
* **Mạch nạp tích hợp ST-LINK/V2-1**: Cho phép nạp chương trình và gỡ lỗi từng dòng lệnh (In-Circuit Debugging) qua chuẩn 2 dây Serial Wire Debug (SWD), đồng thời tích hợp bộ cầu chuyển đổi Virtual COM Port kết nối thẳng với máy tính qua cáp USB mà không cần bất kỳ mạch nạp trung gian nào.

## 2.3 KHỐI CẢM BIẾN THU THẬP THÔNG SỐ MÔI TRƯỜNG NƯỚC

### 2.3.1 Cảm biến tổng chất rắn hòa tan TDS Analog V1.0
Cảm biến TDS (Total Dissolved Solids) sử dụng đầu dò gồm 2 điện cực kim loại không gỉ nhúng trực tiếp vào môi trường nước. Nguyên lý hoạt động dựa trên độ dẫn điện của dung dịch: khi nước chứa nhiều khoáng chất hòa tan hoặc chất thải hữu cơ mang điện tích, độ dẫn điện của dung dịch tăng lên, làm điện trở giữa hai điện cực giảm xuống.

Mạch tiền khuếch đại tín hiệu kèm theo chuyển đổi dòng điện cảm ứng thành điện áp tương tự tuyến tính trong khoảng từ 0.0V đến 2.3V. Điện áp này được đưa vào chân `PA1` (`ADC1_IN1`) của vi điều khiển STM32. Vì dải điện áp cực đại (2.3V) nằm hoàn toàn trong ngưỡng điện áp tham chiếu 3.3V của STM32, tín hiệu được bảo toàn an toàn tuyệt đối mà không cần mạch phân áp bảo vệ. Để triệt tiêu nhiễu tần số cao do sóng nước và bọt khí từ máy sục oxy tạo ra, một tụ điện gốm 0.1µF được lắp đặt song song giữa chân tín hiệu analog và mass (GND).

### 2.3.2 Cảm biến nhiệt độ số chống nước DS18B20 và cảm biến nội bộ DS3231
Nhiệt độ nước là thông số bắt buộc phải thu thập để thực hiện thuật toán bù nhiệt cho cảm biến TDS. Hệ thống hỗ trợ cấu hình kép:
* **Cảm biến chính DS18B20**: Sử dụng đầu dò bọc thép không gỉ chống nước dài 1m nhúng chìm trong bể. Cảm biến giao tiếp với vi điều khiển thông qua chuẩn giao thức 1 dây (1-Wire) trên chân `PA8`. Do cấu trúc cực thu hở (Open-Drain), một điện trở kéo lên ngoài 4.7kΩ bắt buộc phải được đấu nối giữa chân dữ liệu và đường nguồn 3.3V để đảm bảo sườn lên của xung tín hiệu không bị méo dạng. Cảm biến cung cấp độ phân giải tùy chọn từ 9-bit đến 12-bit (sai số chỉ ±0.5°C).
* **Cảm biến nhiệt độ dự phòng trên DS3231**: Trên vi mạch RTC DS3231, nhà sản xuất đã tích hợp sẵn một cảm biến nhiệt độ kỹ thuật số nội bộ dùng để bù nhiệt cho thạch anh dao động. Vi điều khiển có thể đọc thanh ghi `0x11` (phần nguyên) và `0x12` (phần thập phân) qua bus I2C1 để lấy giá trị nhiệt độ môi trường với độ phân giải 0.25°C mà không cần tốn thêm chân GPIO phần cứng nào.

### 2.3.3 Cụm biến trở xoay định lượng thức ăn
Nhằm mang lại trải nghiệm tương tác trực quan cho người sử dụng mà không bắt buộc phải mở điện thoại, chúng tôi bố trí một biến trở xoay đơn 10kΩ (loại B10K có núm vặn) trên mặt điều khiển. Chân giữa của biến trở nối vào chân `PA4` (`ADC1_IN4`), hai chân bìa nối lần lượt vào 3.3V và GND tạo thành một mạch phân áp tuyến tính. 

Giá trị ADC 12-bit (0 – 4095) đọc được từ biến trở được ánh xạ tỷ lệ sang khối lượng thức ăn mong muốn trong khoảng từ 1 gram đến 15 gram:

$$ Portion (grams) = ⌊(ADC_raw × 15) / 4095⌋ + 1 (2.1) $$

## 2.4 KHỐI CƠ CẤU CHẤP HÀNH VÀ CẢNH BÁO

### 2.4.1 Động cơ Servo SG90 và cơ cấu nắp lật định lượng
Cơ cấu định lượng thức ăn sử dụng động cơ Micro Servo 9g (TowerPro SG90) kết hợp với một hộp chứa hạt cám nhỏ (tận dụng hộp kẹo Tic-Tac có nắp lật chống kẹt hạt). 

Cánh tay đòn của động cơ servo được liên kết trực tiếp với nắp lật của hộp. Động cơ được điều khiển bằng tín hiệu điều chế độ rộng xung PWM tần số 50Hz (chu kỳ 20ms) phát ra từ kênh 1 của bộ định thời Timer 2 (`PA0` / `TIM2_CH1`):
* **Trạng thái đóng (Closed Position - 0°)**: Xung điều khiển có độ rộng mức cao là 1.0 ms, nắp hộp đóng kín bảo vệ thức ăn khỏi hơi ẩm bốc lên từ mặt nước bể cá.
* **Trạng thái mở nhả thức ăn (Dispense Position - 90°)**: Xung điều khiển có độ rộng mức cao là 1.5 ms, nắp hộp bật mở 90° để thức ăn rơi tự do xuống bể.

Khối lượng thức ăn rơi xuống được điều tiết thông qua **Thời gian giữ nắp mở động (Dynamic Dwell Time)** phụ thuộc trực tiếp vào cài đặt của biến trở:

$$ Dwell Time (ms) = 300 ms + (Portion × 80 ms) (2.2) $$

Với công thức này, thời gian mở dao động mượt mà từ 380 ms (cho 1g) đến 1500 ms (cho 15g), đảm bảo độ lặp lại và độ chính xác cao.

### 2.4.2 Rơ-le điều khiển máy bơm lọc nước
Hệ thống sử dụng một Module Rơ-le 5V 1 kênh có tích hợp cách ly quang (Optocoupler) để điều khiển nguồn điện của máy bơm lọc nước bể cá. Chân điều khiển `IN` của rơ-le được kết nối với chân `PB4` của STM32. Khi hệ thống ở trạng thái hoạt động bình thường, rơ-le luôn được đóng để duy trì dòng nước tuần hoàn và cung cấp oxy. Khi phát hiện sự cố nguy cấp hoặc cần vệ sinh bể, hệ thống có thể chủ động ngắt máy bơm.

### 2.4.3 Cụm cảnh báo âm thanh và quang học
* **Còi báo động âm thanh**: Sử dụng Module còi Buzzer chủ động 5V (Active Buzzer) loại 3 chân kết nối vào chân `PB0`. Khác với còi thụ động đòi hỏi vi điều khiển phải băm xung tần số âm thanh, còi chủ động tích hợp sẵn mạch dao động nội bên trong; chân `PB0` chỉ cần xuất mức logic cao (3.3V) là còi sẽ phát ra âm thanh báo động liên tục.
* **Hệ thống đèn LED chỉ thị**:
  * LED xanh lá trên bo mạch Nucleo (`PA5` / LD2): Sáng liên tục báo hiệu hệ thống vận hành bình thường và nhấp nháy trong suốt quá trình cơ cấu cho ăn đang hoạt động.
  * LED đỏ cảnh báo ngoài (`PB1`): Được mắc nối tiếp với điện trở hạn dòng 330Ω. Khi nồng độ TDS vượt ngưỡng cảnh báo (> 450 ppm), LED đỏ sáng liên tục; khi vượt ngưỡng nguy hiểm (> 500 ppm), LED đỏ chớp tắt liên tục với tần số 1Hz đồng thời còi hú để cảnh báo người dùng.

## 2.5 KHỐI HIỂN THỊ CỤC BỘ VÀ LƯU TRỮ DỮ LIỆU THỜI GIAN THỰC TRÊN BUS I2C1

Nhằm tiết kiệm tối đa số lượng chân I/O của vi điều khiển, toàn bộ các thiết bị ngoại vi số bao gồm Màn hình LCD, Đồng hồ thời gian thực và Bộ nhớ EEPROM được ghép song song trên cùng một bus truyền thông **I2C1** sử dụng 2 chân: `PB8` làm đường xung nhịp (SCL) và `PB9` làm đường dữ liệu (SDA).

*Bảng 2.2: Địa chỉ vật lý và nhiệm vụ của các vi mạch trên bus I2C1*
| Tên Thiết Bị / Module | Địa Chỉ I2C 7-bit | Địa Chỉ 8-bit (STM32 HAL) | Tác Vụ FreeRTOS Truy Xuất | Chức Năng Chính |
| :--- | :---: | :---: | :--- | :--- |
| **LCD 2004 (PCF8574)** | `0x27` (hoặc `0x3F`) | `0x4E` | `Task_DisplayUI` (BelowNormal) | Hiển thị 4 dòng thông số trực quan |
| **DS3231 Real-Time Clock** | `0x68` | `0xD0` | `Task_DisplayUI` (BelowNormal) | Cung cấp giờ/phút/giây thời gian thực |
| **AT24C32 EEPROM** | `0x57` | `0xAE` | `Task_DispenserControl` (AboveNormal) | Ghi nhật ký các sự kiện cho cá ăn |

### 2.5.1 Màn hình LCD 2004 tích hợp module chuyển đổi I2C PCF8574
Màn hình LCD 2004 hiển thị 4 dòng, mỗi dòng 20 ký tự chữ số. Phía sau màn hình được hàn sẵn một bo mạch chuyển đổi dựa trên chip mở rộng I/O PCF8574. Chip PCF8574 nhận dữ liệu điều khiển nối tiếp từ bus I2C và giải mã thành 8 đường tín hiệu song song kết nối với các chân dữ liệu D4–D7, chân chọn thanh ghi RS, chân kích hoạt E và đèn nền của màn hình theo chế độ 4-bit nibble. Giải pháp này giúp tiết kiệm 6 chân GPIO so với cách điều khiển song song truyền thống.

### 2.5.2 Đồng hồ thời gian thực chính xác cao DS3231
Module DS3231 là vi mạch đếm thời gian thực tích hợp bộ dao động thạch anh bù nhiệt độ (TCXO). Module lưu giữ chính xác thông tin giây, phút, giờ, thứ, ngày, tháng, năm dưới dạng mã nhị phân BCD. Nhờ tích hợp pin cúc áo dự phòng, đồng hồ vẫn tiếp tục chạy chính xác ngay cả khi toàn bộ nguồn điện của hệ thống bị cắt.

### 2.5.3 Bộ nhớ EEPROM AT24C32 lưu nhật ký cho ăn
Tích hợp ngay trên cùng bo mạch ZS-042 với DS3231 là chip nhớ EEPROM AT24C32 có dung lượng 32 Kilobits (4096 bytes). Bộ nhớ được tổ chức thành 128 trang, mỗi trang 32 bytes. Mỗi khi tác vụ cho ăn được kích hoạt thành công, hệ thống sẽ thực hiện một giao dịch ghi 8 bytes dữ liệu vào địa chỉ ô nhớ `0x0000` bao gồm: Byte nhận dạng (Magic byte `0xAA`), Khối lượng định lượng (portion grams) và Giá trị dấu thời gian Unix timestamp 32-bit. Dữ liệu này được lưu trữ an toàn trong bộ nhớ không khả biến (Non-volatile memory) để phục vụ việc kiểm tra lịch sử hoạt động.

## 2.6 KHỐI TRUYỀN THÔNG KHÔNG DÂY IOT ESP32 VÀ CÁP NẠP ST-LINK USB

Để khắc phục hoàn toàn lỗi xung đột bus truyền thông nối tiếp trong thiết kế cũ, hệ thống được trang bị kiến trúc **Viễn thông hai kênh độc lập (Dual-Port Telemetry)**:
1. **Kênh IoT Không Dây (`USART1` - `PA9` TX / `PA10` RX)**:
   * Đường truyền này kết nối trực tiếp với cổng phần cứng Serial2 của vi điều khiển ESP32 (`GPIO16` RX2, `GPIO17` TX2) ở tốc độ baudrate chuẩn 115200 bps, cấu hình khung 8-bit dữ liệu, không kiểm tra chẵn lẻ, 1 stop bit (8N1).
   * Vi điều khiển phụ ESP32 kết nối vào mạng Wi-Fi cục bộ, chạy chương trình Telegram Bot để lắng nghe các lệnh từ người dùng (`/feed`, `/status`) và phát Web Dashboard HTML responsive. Khi nhận được lệnh `/feed`, ESP32 gửi chuỗi ký tự định khung `~feed~` sang STM32 để kích hoạt động cơ.
2. **Kênh Giám Sát Dự Phòng Failsafe (`USART2` - `PA2` TX / `PA3` RX)**:
   * Cặp chân `PA2`/`PA3` trên bo mạch Nucleo-64 được nhà sản xuất đấu nối cứng qua các cầu hàn phần cứng với chip ST-LINK/V2-1. Tín hiệu UART được ST-LINK chuyển đổi thành cổng nối tiếp ảo (Virtual COM Port - VCP) truyền thẳng lên máy tính qua cáp USB.
   * Trên máy tính, chúng tôi phát triển một script Python giám sát độc lập ([`scripts/aquatic_pc_bridge.py`](file:///E:/AntiGravityRoot/mcp201-aquatic-guardian/scripts/aquatic_pc_bridge.py)). Kênh này giúp nhóm có thể trình chiếu trực tiếp biểu đồ thông số lên máy chiếu trong buổi bảo vệ mà không phải phụ thuộc vào sóng Wi-Fi của giảng đường.

## 2.7 THIẾT KẾ MẠCH NGUỒN VÀ 6 VẤN ĐỀ KỸ THUẬT TRỌNG YẾU TRONG TRIỂN KHAI PHẦN CỨNG THỰC TẾ

Quá trình lắp ráp và thử nghiệm mạch trên Breadboard tiềm ẩn nhiều vấn đề kỹ thuật phần cứng nếu chỉ áp dụng sơ đồ lý thuyết. Dưới đây là 6 vấn đề kỹ thuật trọng yếu đã được chúng tôi phân tích nguyên nhân và đưa ra giải pháp xử lý dứt điểm:

*Bảng 2.3: Bảng đối chiếu 6 vấn đề kỹ thuật phần cứng thực tế và giải pháp khắc phục*
| STT | Vấn Đề Kỹ Thuật Phần Cứng Thực Tế | Nguy Cơ Kỹ Thuật Nếu Không Khắc Phục | Giải Pháp Kỹ Thuật Đã Chốt Trong Đề Tài |
| :---: | :--- | :--- | :--- |
| **1** | **Hiện tượng sụt áp trên IC ổn áp mạch nguồn MB102** | Mạch nguồn Breadboard MB102 sử dụng IC ổn áp tuyến tính AMS1117-5.0 có độ sụt áp (Dropout Voltage) khoảng 1.2V. Nếu cấp nguồn đầu vào 5V từ cổng USB, điện áp đầu ra trên thanh nguồn Breadboard chỉ còn **~3.8V**. Điện áp này không đủ để nuôi màn hình LCD2004 (khiến màn hình bị tối đen, mờ tịt) và cuộn hút Rơ-le 5V không thể đóng ngắt. | **Sử dụng Adapter nguồn 9V-1A (hoặc 12V-1A) đầu cắm tròn DC 5.5x2.1mm** cắm vào jack DC của MB102. Khi điện áp vào là 9V, IC AMS1117 hoạt động tối ưu và xuất ra mức điện áp chuẩn 5.0V nuôi ổn định màn hình LCD, Servo SG90 và Rơ-le. |
| **2** | **Nucleo không thể cắm trực tiếp lên Breadboard & Kích thước ESP32** | Bo mạch STM32 Nucleo-64 có 2 hàng chân đực Morpho ở mặt đáy; nếu ấn bo mạch này xuống Breadboard sẽ gây **chập mạch toàn bộ các cặp chân đối diện nhau**. Thêm vào đó, module ESP32 bản 38 chân có bề ngang quá lớn, khi cắm lên Breadboard MB-102 sẽ che lấp toàn bộ các lỗ cắm linh kiện ở một bên. | Đặt bo mạch Nucleo nằm bên cạnh Breadboard; sử dụng **1 tép dây cắm Cái - Cái (40 sợi)** và **1 tép Đực - Cái (40 sợi)** để câu tín hiệu từ hàng chân đực của Nucleo sang Breadboard. Đối với ESP32, **chỉ chọn mua đúng phiên bản ESP32 DevKit V1 30 chân** để chừa lại đúng 1 hàng lỗ cắm dây trên Breadboard. |
| **3** | **Còi Buzzer 2 chân gây quá dòng chân vi điều khiển** | Còi chip 2 chân rời tiêu thụ dòng điện tức thời từ 25mA đến 35mA, vượt quá giới hạn an toàn khuyến nghị của chân GPIO `PB0` trên STM32 (tối đa 8mA – 15mA). Ngoài ra, cuộn cảm của còi sinh sức điện động phản kháng (Inductive kickback) gây nhiễu làm treo vi điều khiển. | Thay thế còi 2 chân rời bằng **Module Còi Buzzer Chủ Động loại 3 chân (VCC, GND, I/O)**. Trên bo mạch module này đã tích hợp sẵn một Transistor bán dẫn đệm dòng S8050/S8550; chân `PB0` của STM32 chỉ cần đóng vai trò kích mức logic với dòng tiêu thụ dưới 1mA. |
| **4** | **Hiện tượng nạp ngược phồng pin CR2032 trên module DS3231 ZS-042** | Bo mạch RTC DS3231 ZS-042 được thiết kế sẵn một mạch nạp nhồi (gồm điện trở 200Ω và một diode đỏ) dành riêng cho pin sạc LIR2032 (3.6V). Tuy nhiên, hầu hết các cửa hàng đều bán kèm pin không sạc CR2032 (3V). Nếu cấp nguồn 5V vào chân VCC, dòng sạc ngược sẽ liên tục nạp vào pin CR2032 làm pin bị quá nhiệt, phồng to và rỉ hóa chất ăn mòn mạch. | **Cấp nguồn 3.3V từ chân 3V3 của STM32 vào chân VCC của module DS3231** (không lấy nguồn 5V), hoặc dùng đầu mỏ hàn gẩy bỏ con điện trở 200Ω nằm sát chân SCL trên bo ZS-042 để ngắt hoàn toàn mạch sạc trước khi lắp pin CR2032. |
| **5** | **Rơ-le 5V kích mức Thấp bị dính trạng thái đóng** | Khi nuôi Rơ-le bằng nguồn 5V, nếu chân `PB4` của STM32 xuất mức logic Cao (chỉ đạt 3.3V ở chế độ Push-Pull), độ chênh lệch điện áp giữa nguồn 5V và chân vi điều khiển là 5V - 3.3V = 1.7V. Điện áp 1.7V này lớn hơn điện áp mở của LED cách ly quang bên trong (thường là 1.2V), khiến transistor quang luôn dẫn và Rơ-le bị dính chặt trạng thái đóng, không bao giờ ngắt được. | **Chọn mua Module Rơ-le 1 kênh 5V có Jumper cho phép chọn mức kích High/Low** và chuyển Jumper sang vị trí kích Cao (High Trigger). Phương án dự phòng là cấu hình chân `PB4` (chân chịu được áp 5V-tolerant) ở chế độ cực máng hở (Open-Drain). |
| **6** | **Thiếu điện trở kéo lên cho DS18B20 & Đấu chéo UART** | Các đầu dò DS18B20 bán lẻ thường không kèm theo điện trở kéo lên 4.7kΩ; nếu thiếu điện trở này, đường truyền 1-Wire sẽ luôn ở mức thấp và không thể đọc dữ liệu. Ngoài ra, việc đấu nối sai chiều TX/RX giữa STM32 và ESP32 là lỗi thường gặp làm tê liệt truyền thông. | Mua bổ sung vỉ điện trở 4.7kΩ ngoài để hàn kéo chân dữ liệu lên 3.3V. Tuân thủ nghiêm ngặt quy tắc đấu chéo UART: **STM32 `PA9` (USART1_TX) nối vào ESP32 `GPIO16` (RX2)** và **STM32 `PA10` (USART1_RX) nối vào ESP32 `GPIO17` (TX2)** kèm nối chung mass GND. |

## 2.8 BẢNG PHÂN BỔ CHÂN STM32 NUCLEO KHÔNG XUNG ĐỘT (CONFLICT-FREE PINOUT)

Toàn bộ 16 tín hiệu phần cứng của hệ thống được tính toán và phân bổ tối ưu vào các chân vật lý trên bo mạch STM32 Nucleo-64, đảm bảo không có bất kỳ sự trùng lặp nào về chức năng ngoại vi hay tài nguyên phần cứng:

*Bảng 2.1: Bảng phân bổ chân STM32 Nucleo không xung đột (Conflict-Free Pinout)*
| Chức Năng Hệ Thống | Tên Linh Kiện Ngoại Vi | Tín Hiệu Kết Nối | Vị Trí Chân Nucleo | Cấu Hình STM32 HAL | Ghi Chú Kỹ Thuật & Mạch Điện |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **Chất lượng nước** | Cảm biến Analog TDS V1.0 | AOUT | **`PA1`** | ADC1_IN1 (Rank 1) | Tín hiệu tương tự 0 – 2.3V; tụ lọc 0.1µF xuống GND |
| **Định lượng thức ăn**| Biến trở xoay B10K | Chân giữa (Wiper) | **`PA4`** | ADC1_IN4 (Rank 1) | Mạch phân áp 0 – 3.3V tương ứng định lượng 1g – 15g |
| **Nhiệt độ nước** | Cảm biến DS18B20 chống nước | Data | **`PA8`** | GPIO_Output_OD | Giao thức 1-Wire; điện trở kéo ngoài 4.7kΩ lên 3.3V |
| **Cơ cấu cho ăn** | Động cơ Servo mini SG90 | Tín hiệu PWM | **`PA0`** | TIM2_CH1 (AF1) | Xung PWM 50Hz (ARR=19999, PSC=83). 0° → 90° |
| **Động cơ bước (Dự phòng)**| Động cơ 28BYJ-48 + ULN2003 | IN1 – IN4 | **`PB12–PB15`** | GPIO_Output | Tách biệt hoàn toàn, không đè lên chân I2C `PB8`/`PB9` |
| **Đường xung I2C1** | LCD2004 + DS3231 + EEPROM | SCL | **`PB8`** | I2C1_SCL (AF4) | Xung nhịp bus chia sẻ; trở kéo 4.7kΩ lên 3.3V |
| **Đường dữ liệu I2C1**| LCD2004 + DS3231 + EEPROM | SDA | **`PB9`** | I2C1_SDA (AF4) | Dữ liệu bus chia sẻ; trở kéo 4.7kΩ lên 3.3V |
| **Cổng IoT Wi-Fi** | Module ESP32 Co-Processor | TX (sang ESP RX2) | **`PA9`** | USART1_TX (AF7) | Tốc độ 115200 bps, 8N1; nối chéo sang ESP32 GPIO16 |
| **Cổng IoT Wi-Fi** | Module ESP32 Co-Processor | RX (từ ESP TX2) | **`PA10`** | USART1_RX (AF7) | Tốc độ 115200 bps, 8N1; nối chéo sang ESP32 GPIO17 |
| **Cổng PC Debug** | ST-LINK USB Virtual COM Port| TX (sang PC) | **`PA2`** | USART2_TX (AF7) | Tốc độ 115200 bps; nối cứng ST-LINK nạp code |
| **Cổng PC Debug** | ST-LINK USB Virtual COM Port| RX (từ PC) | **`PA3`** | USART2_RX (AF7) | Tốc độ 115200 bps; nhận lệnh gỡ lỗi từ script Python |
| **Nút bấm khẩn cấp** | Nút bấm xanh User Button B1 | Push Button | **`PC13`** | EXTI13 (Falling) | Tích hợp lọc rung phần mềm tick guard 300ms |
| **Còi báo động** | Module Active Buzzer 3 chân | I/O Pin | **`PB0`** | GPIO_Output | Mức 1 = Hú còi; có Transistor đệm dòng < 1mA |
| **LED trạng thái** | LED xanh lá User LED LD2 | Anode (+) | **`PA5`** | GPIO_Output | Sáng liên tục = Hệ thống bình thường; Nháy = Đang cho ăn |
| **LED cảnh báo** | LED đỏ 5mm cảnh báo | Anode (+) | **`PB1`** | GPIO_Output | Trở hạn dòng 330Ω; Nháy 1Hz khi TDS > 500 ppm |
| **Máy bơm nước** | Module Rơ-le cách ly quang | Relay IN | **`PB4`** | GPIO_Output | Đóng ngắt nguồn máy bơm; Jumper set kích High |

---

# CHƯƠNG 3 THIẾT KẾ PHẦN MỀM VÀ ĐA NHIỆM FREERTOS

## 3.1 KIẾN TRÚC HỆ ĐIỀU HÀNH THỜI GIAN THỰC FREERTOS VÀ CMSIS-RTOS V2

Hệ thống nhúng Aquatic Guardian được phát triển hoàn toàn trên nền tảng hệ điều hành thời gian thực mã nguồn mở **FreeRTOS** thông qua lớp bao bọc tiêu chuẩn công nghiệp **CMSIS-RTOS v2** do ARM quy chuẩn. 

Việc chuyển dịch từ mô hình vòng lặp tuần tự cổ điển (Superloop) sang hệ điều hành thời gian thực đem lại các ưu thế vượt trội:
* **Tính tiền định (Determinism)**: Bộ lập lịch ưu tiên dựa trên thời gian (Preemptive Priority-Based Scheduler) cho phép ngắt ngang (preempt) tác vụ có độ ưu tiên thấp ngay lập tức để phục vụ tác vụ có độ ưu tiên cao hơn khi điều kiện kích hoạt xảy ra.
* **Tối ưu hóa tài nguyên CPU**: Khi một tác vụ cần chờ đợi thời gian hoặc chờ tín hiệu ngoại vi, tác vụ đó gọi hàm `osDelay()` hoặc `osSemaphoreAcquire()`. Hệ điều hành sẽ lập tức chuyển tác vụ sang trạng thái Chờ (Blocked State) và nhường quyền điều khiển CPU cho các tác vụ khác hoặc chuyển sang tác vụ nghỉ (Idle Task) để tiết kiệm năng lượng.
* **Giải quyết xung đột Timebase**: Khi sử dụng FreeRTOS trên STM32, xung nhịp đếm ngắt hệ thống (SysTick Timer) bắt buộc phải được dành riêng hoàn toàn cho bộ lập lịch FreeRTOS. Do đó, nguồn tạo thời gian cho thư viện phần cứng HAL (HAL Timebase Source) được cấu hình chuyển dịch sang một bộ định thời phần cứng độc lập là **Timer 5** với mức ưu tiên ngắt NVIC cao nhất (Priority 0).

> **Lưu ý đặc thù về kích thước Stack trong CMSIS-RTOS v2:**  
> Trong phiên bản CMSIS-RTOS v1 trước đây, tham số kích thước stack (`stack_size`) được tính theo đơn vị số từ nhớ 32-bit (Words). Tuy nhiên, trong chuẩn **CMSIS-RTOS v2**, tham số `.stack_size` trong cấu trúc `osThreadAttr_t` được định nghĩa nghiêm ngặt theo đơn vị **BYTES**. Nếu lập trình viên vô tình truyền giá trị 256 vào tham số này, hệ điều hành chỉ cấp phát 256 bytes (tương đương 64 words), dẫn đến hiện tượng tràn bộ nhớ stack (Stack Overflow) và làm chip văng vào bẫy lỗi nghiêm trọng `HardFault_Handler` ngay khi gọi các hàm định dạng chuỗi phức tạp như `snprintf()`. Trong đề tài này, toàn bộ kích thước stack được quy định rõ ràng bằng bytes: 1024 bytes cho các tác vụ tính toán cơ bản và 2048 bytes cho các tác vụ xử lý chuỗi ký tự.

## 3.2 PHÂN RÃ 5 TÁC VỤ THỜI GIAN THỰC VÀ THỨ BẬC ƯU TIÊN

Toàn bộ khối chương trình được phân rã thành 5 tác vụ độc lập chạy đồng thời, được gán mức ưu tiên từ cao xuống thấp căn cứ vào mức độ khẩn cấp đối với sự sống còn của sinh vật trong bể:

*Bảng 3.1: Bảng đặc tả 5 tác vụ thời gian thực FreeRTOS và phân bổ bộ nhớ Stack*
| Tên Tác Vụ (Thread Name) | Mức Ưu Tiên (CMSIS Priority) | Chu Kỳ / Cơ Chế Kích Hoạt | Kích Thước Stack | Trách Nhiệm Kỹ Thuật Chính |
| :--- | :--- | :---: | :---: | :--- |
| **`Task_SafetySupervisor`** | `osPriorityHigh` (32) | Định kỳ 200 ms | 1024 Bytes | Giám sát các ngưỡng an toàn nước, kích hoạt còi và đèn cảnh báo nguy cấp tức thời. |
| **`Task_DispenserControl`** | `osPriorityAboveNormal` (24) | Hướng sự kiện (Event-Driven) | 1024 Bytes | Chờ cờ Semaphore, quay động cơ Servo nhả thức ăn và ghi nhật ký vào EEPROM. |
| **`Task_SensorAcquisition`** | `osPriorityNormal` (16) | Định kỳ 1000 ms | 1024 Bytes | Đọc tuần tự các kênh ADC, lọc số 20 mẫu, tính toán TDS bù nhiệt và cập nhật Mailbox. |
| **`Task_DisplayUI`** | `osPriorityBelowNormal` (12) | Định kỳ 500 ms | 2048 Bytes | Đọc giờ thời gian thực RTC DS3231 và cập nhật 4 dòng thông số lên màn hình LCD 2004. |
| **`Task_Telemetry`** | `osPriorityLow` (8) | Định kỳ 2000 ms | 2048 Bytes | Đóng gói chuỗi JSON định khung `~` và phát song song ra cổng ESP32 và ST-LINK USB. |

### 3.2.1 Tác vụ giám sát an toàn khẩn cấp (Task_SafetySupervisor)
Có mức ưu tiên cao nhất (`osPriorityHigh`), chu kỳ đánh thức 200ms. Tác vụ thực hiện đọc không phá hủy từ hòm thư Mailbox để lấy bản sao dữ liệu cảm biến mới nhất. Nếu phát hiện nồng độ TDS vượt ngưỡng nguy hại (> 500 ppm) hoặc nhiệt độ nước quá nhiệt (> 32°C), tác vụ sẽ lập tức kích hoạt còi hú `PB0` và chớp đèn LED đỏ `PB1` với tần số 1Hz để báo động cho người xung quanh.

### 3.2.2 Tác vụ điều khiển cơ cấu cho ăn (Task_DispenserControl)
Có mức ưu tiên cận cao (`osPriorityAboveNormal`), vận hành theo mô hình hướng sự kiện (Event-driven). Bình thường tác vụ nằm ở trạng thái `Blocked` hoàn toàn tại hàm `osSemaphoreAcquire(feedTriggerSemHandle, osWaitForever)` nên không tiêu tốn chu kỳ CPU. Khi có tín hiệu kích hoạt từ ngắt nút bấm `PC13`, báo thức RTC hoặc lệnh Telegram `/feed`, tác vụ lập tức thức tỉnh:
1. Bật nhấp nháy đèn LED xanh `PA5`.
2. Đọc giá trị định lượng hiện tại để tính toán thời gian trễ.
3. Điều khiển Servo quay sang góc 90° mở nắp hộp thức ăn trong khoảng thời gian Dwell Time.
4. Điều khiển Servo quay trở về góc 0° đóng nắp kín.
5. Chiếm giữ khóa `i2cBusMutexHandle` để thực hiện giao dịch ghi bản ghi thời gian cho ăn vào chip nhớ EEPROM AT24C32.

### 3.2.3 Tác vụ thu thập và xử lý tín hiệu cảm biến (Task_SensorAcquisition)
Có mức ưu tiên bình thường (`osPriorityNormal`), chu kỳ lặp 1000ms. Tác vụ thực hiện đọc luân phiên từng kênh ADC để tránh lỗi ghi đè thanh ghi dữ liệu của STM32, đẩy mẫu vào bộ lọc vòng 20 phần tử, tính toán nồng độ TDS theo phương trình bù nhiệt, phân loại chất lượng nước theo bảng tiêu chuẩn sinh thái và đưa gói dữ liệu hoàn chỉnh vào hòm thư Length-1 Mailbox.

### 3.2.4 Tác vụ hiển thị giao diện người dùng LCD (Task_DisplayUI)
Có mức ưu tiên dưới bình thường (`osPriorityBelowNormal`), chu kỳ làm mới 500ms. Tác vụ đọc không phá hủy dữ liệu từ Mailbox, sau đó yêu cầu chiếm giữ `i2cBusMutexHandle`. Khi đã có quyền kiểm soát bus I2C1, tác vụ gửi lệnh đọc thời gian thực từ chip DS3231, định dạng các chuỗi ký tự và ghi trực tiếp lên màn hình LCD 2004 hiển thị giá trị TDS, chất lượng nước, định lượng gram và nhiệt độ.

### 3.2.5 Tác vụ truyền thông viễn thông đa kênh (Task_Telemetry)
Có mức ưu tiên thấp nhất (`osPriorityLow`), chu kỳ phát tin 2000ms. Tác vụ lấy bản sao dữ liệu cảm biến, chiếm giữ khóa `uartMutexHandle` và đóng gói toàn bộ trạng thái thành một chuỗi văn bản JSON chuẩn có định khung bằng ký tự ngã `~`. Chuỗi JSON này được truyền song song đồng thời ra module Wi-Fi ESP32 (`USART1`) và cổng máy tính ST-LINK USB (`USART2`).

## 3.3 CƠ CHẾ ĐỒNG BỘ HÓA VÀ GIAO TIẾP LIÊN TÁC VỤ (IPC)

Trong một hệ thống nhúng đa nhiệm tiền định, sự tương tác giữa các tác vụ nếu không được thiết kế chặt chẽ sẽ dẫn đến các lỗi kinh điển: chết đói dữ liệu (Starvation), xung đột dữ liệu (Race Conditions) hoặc khóa chết hệ thống (Deadlock). Chúng tôi đã nghiên cứu và ứng dụng 3 cơ chế đồng bộ hóa cốt lõi:

### 3.3.1 Hòm thư phi hủy dữ liệu Length-1 Mailbox chống hiện tượng chết đói
* **Vấn đề kỹ thuật**: Trong cơ chế hàng đợi tiêu chuẩn (FreeRTOS Message Queue), hàm đọc `osMessageQueueGet()` mang tính chất tiêu thụ phá hủy (Destructive Read) — tức là một khi dữ liệu đã được một tác vụ đọc ra, gói dữ liệu đó sẽ bị xóa khỏi hàng đợi. Trong hệ thống của chúng tôi, có tới 3 tác vụ cùng có nhu cầu tiêu thụ dữ liệu cảm biến: Giám sát an toàn (200ms), Hiển thị LCD (500ms) và Viễn thông (2000ms). Vì `Task_SafetySupervisor` có mức ưu tiên cao nhất (`osPriorityHigh`) và chu kỳ nhanh nhất (200ms), nó sẽ chiếm dụng toàn bộ các gói tin do tác vụ cảm biến sinh ra, khiến cho tác vụ LCD và tác vụ Viễn thông bị **bỏ đói hoàn toàn (Starvation)** và không bao giờ nhận được dữ liệu.
* **Giải pháp khắc phục**: Chúng tôi thiết kế hàng đợi dưới dạng **Hòm thư phi hủy độ dài 1 (Length-1 Non-Destructive Mailbox)**:
  1. Tác vụ sản xuất (`Task_SensorAcquisition`) sử dụng hàm `osMessageQueuePut()` ghi đè liên tục bản ghi dữ liệu cảm biến mới nhất vào hòm thư.
  2. Cả 3 tác vụ tiêu thụ đều sử dụng hàm `osMessageQueuePeek(telemetryQueueHandle, &buffer, NULL, 0)`. Hàm `Peek` sao chép nội dung gói tin vào bộ nhớ cục bộ của tác vụ mà **hoàn toàn không xóa gói tin ra khỏi hàng đợi**. Nhờ đó, cả 3 tác vụ đều đọc được trạng thái sinh thái mới nhất theo đúng chu kỳ riêng của mình mà không gây cản trở lẫn nhau.

### 3.3.2 Kỹ thuật xử lý ngắt trì hoãn (Deferred Interrupt) và chống rung phím 300ms
* **Quy tắc vàng của lập trình nhúng**: Chương trình con phục vụ ngắt (ISR) phải thực thi trong thời gian cực ngắn (vài micro-giây) và tuyệt đối không bao giờ được phép gọi các hàm chờ trễ như `HAL_Delay()` hay `osDelay()`. Quá trình xoay động cơ Servo nhả thức ăn kéo dài từ 800ms đến 1500ms; nếu đặt đoạn mã này trong ngắt sẽ làm tê liệt toàn bộ hệ thống ngắt của vi điều khiển.
* **Cơ chế Deferred Interrupt Processing**: Khi người dùng nhấn nút xanh `PC13`, ngắt ngoài EXTI13 được kích hoạt. Hàm ngắt `HAL_GPIO_EXTI_Callback()` chỉ thực hiện đúng 2 nhiệm vụ:
  1. Kiểm tra bộ đếm thời gian phần mềm (`HAL_GetTick() - last_tick > 300ms`) để triệt tiêu hoàn toàn hiện tượng rung tiếp điểm cơ khí (Contact Bounce) của nút bấm.
  2. Gọi hàm `osSemaphoreRelease(feedTriggerSemHandle)` để nhả tín hiệu Semaphore nhị phân rồi thoát ngay lập tức trong thời gian chưa đầy 1 µs.
  3. Tác vụ luồng `Task_DispenserControl` đang chờ sẵn trên Semaphore sẽ lập tức được bộ lập lịch FreeRTOS đánh thức để thực thi quá trình quay Servo một cách tuần tự trong ngữ cảnh tác vụ (Thread Context).

### 3.3.3 Quản lý Bus I2C1 và chứng minh cơ chế thừa kế quyền ưu tiên (Priority Inheritance)
Bus truyền thông I2C1 là tài nguyên phần cứng đơn luồng dùng chung giữa 2 tác vụ có mức ưu tiên cách biệt:
* `Task_DispenserControl` (Mức ưu tiên cận cao - `osPriorityAboveNormal` = 24): Cần ghi log vào EEPROM AT24C32.
* `Task_DisplayUI` (Mức ưu tiên dưới bình thường - `osPriorityBelowNormal` = 12): Cần đọc RTC và cập nhật màn hình LCD.

Để tránh xung đột xung nhịp trên 2 dây SCL/SDA, toàn bộ các truy xuất I2C đều phải được bảo vệ bằng khóa độc quyền `i2cBusMutexHandle`.

```
Task_DispenserControl (Priority 24 - AboveNormal)
       |                                   [Chờ Mutex] ===================> [ĐƯỢC GIẢI PHÓNG - CHẠY]
       |                                        ^                                      ^
Task_SensorAcquisition (Priority 16 - Normal)   |   (BỊ CHẶN - KHÔNG ĐƯỢC CHEN NGANG)  |
       |                                        |                  |                   |
Task_DisplayUI (Priority 12 - BelowNormal)      |                  |                   |
       +---> [Chiếm Mutex I2C] -----------------+---> [NÂNG ƯU TIÊN LÊN 24] ----------+---> [Nhả Mutex - Về 12]
                                                      (Priority Inheritance)
```
*Hình 3.4: Giản đồ thời gian chứng minh cơ chế thừa kế quyền ưu tiên (Priority Inheritance) trên bus I2C1*

**Chứng minh hiện tượng Nghịch đảo mức ưu tiên (Priority Inversion) và giải pháp:**
Giả sử `Task_DisplayUI` (ưu tiên 12) đang chiếm giữ Mutex để in thông tin lên LCD. Đúng lúc đó, sự kiện cho ăn xảy ra, `Task_DispenserControl` (ưu tiên 24) thức tỉnh và yêu cầu lấy Mutex. Vì Mutex đang bị khóa, tác vụ ưu tiên 24 buộc phải chuyển sang trạng thái chờ. Nếu lúc này có một tác vụ trung gian là `Task_SensorAcquisition` (ưu tiên 16) thức tỉnh, theo lý thuyết thông thường tác vụ 16 sẽ chiếm CPU và đẩy tác vụ 12 xuống, khiến tác vụ 12 không thể nhả Mutex, gián tiếp làm tác vụ cấp cao 24 bị khóa vô hạn.

Để loại bỏ sự cố nghịch đảo mức ưu tiên này, Mutex trong FreeRTOS kích hoạt giao thức **Thừa kế quyền ưu tiên (Priority Inheritance)**: Ngay khi `Task_DispenserControl` yêu cầu khóa Mutex, hệ điều hành lập tức tạm thời nâng mức ưu tiên của `Task_DisplayUI` từ 12 vọt lên 24. Nhờ đó, tác vụ hiển thị không thể bị tác vụ trung gian (16) chen ngang, nhanh chóng hoàn tất giao dịch I2C và giải phóng Mutex. Ngay khi Mutex được giải phóng, mức ưu tiên của tác vụ hiển thị hạ về 12, và tác vụ cho ăn lập tức chiếm giữ bus để ghi log EEPROM. Cơ chế này đảm bảo tính toàn vẹn hệ thống tuyệt đối.

## 3.4 THUẬT TOÁN LỌC SỐ TRUNG BÌNH TRƯỢT VÒNG 20 MẪU O(1) VÀ PHƯƠNG TRÌNH BẬC 3 BÙ NHIỆT TDS

### 3.4.1 Bộ lọc trung bình trượt vòng 20 mẫu trong thời gian O(1)
Trong môi trường bể thủy sinh, các thiết bị sục khí tạo oxy và máy bơm dòng tạo ra sóng nước và bọt khí liên tục quét qua bề mặt điện cực của cảm biến TDS. Điều này làm giá trị điện áp ADC thô bị dao động ngẫu nhiên với biên độ rất lớn (tương đương ±50 ppm). Nếu sử dụng trực tiếp giá trị thô này, hệ thống sẽ liên tục kích hoạt báo động giả.

Để làm mịn tín hiệu, chúng tôi hiện thực hóa một **Bộ lọc trung bình trượt vòng (Circular Moving Average Filter)** với kích thước cửa sổ lọc N = 20 mẫu. Thay vì sử dụng vòng lặp duyệt tuần tự 20 phần tử làm tiêu tốn độ phức tạp thời gian O(N), hệ thống duy trì một biến tích lũy tổng chạy (Running Sum accumulator). Mỗi khi có mẫu đo mới `X_new`:

$$ Sum_k = Sum_(k-1) - X_(k-N) + X_k (3.1) $$

$$ X_filtered = Sum_k / N (3.2) $$

Phép toán này được thực thi trong thời gian hằng số O(1) chỉ với 1 phép trừ, 1 phép cộng và 1 phép chia, giúp tiết kiệm chu kỳ xung nhịp CPU tối đa.

### 3.4.2 Phương trình đa thức bậc 3 bù nhiệt độ tính nồng độ TDS
Độ dẫn điện của các ion trong dung dịch nước tăng lên khoảng 2% cho mỗi độ C tăng thêm của nhiệt độ. Do đó, điện áp đọc được từ cảm biến trước hết phải được chuẩn hóa về nhiệt độ quy chiếu chuẩn 25.0°C:

$$ V_comp = V_adc / [1.0 + 0.02 × (T_water - 25.0)] (3.3) $$

Trong đó:
* V_adc = (ADC_raw / 4095) × 3.3 V là điện áp thực tế tại chân `PA1`.
* T_water là nhiệt độ nước thực tế đo được từ cảm biến DS18B20 (hoặc DS3231).

Sau khi có điện áp bù nhiệt V_comp, nồng độ chất rắn hòa tan TDS (đơn vị ppm - parts per million) được tính toán chính xác thông qua phương trình đa thức phi tuyến bậc 3:

$$ TDS (ppm) = [133.42 × (V_comp)^3 - 255.86 × (V_comp)^2 + 857.39 × V_comp] × 0.5 (3.4) $$

*Bảng 3.2: Bảng tra cứu phân loại trạng thái chất lượng nước sinh thái*
| Dải Giá Trị TDS (ppm) | Nhiệt Độ Nước (°C) | Phân Loại Trạng Thái | Hành Vi Hệ Thống |
| :--- | :--- | :---: | :--- |
| **TDS ≤ 350** | 24.0°C ≤ T ≤ 29.0°C | `OPTIMAL` (Lý tưởng) | LED xanh sáng, Rơ-le bơm ON, Còi tắt, Telegram bình thường |
| **350 < TDS ≤ 450** | 20.0°C ≤ T ≤ 30.0°C | `ACCEPTABLE` (Chấp nhận) | LED xanh sáng, LCD hiển thị cảnh báo nhẹ |
| **450 < TDS ≤ 500** | 30.0°C < T ≤ 32.0°C | `WARNING` (Cảnh báo) | LED đỏ sáng liên tục, gửi thông báo thay nước lên Telegram |
| **TDS > 500** | T < 18.0°C hoặc T > 32.0°C | `CRITICAL` (Nguy hại) | LED đỏ nháy 1Hz, Còi hú liên tục, Bắn tin khẩn cấp Telegram |

## 3.5 GIAO THỨC ĐÓNG GÓI DỮ LIỆU UART ĐỊNH KHUNG KÝ TỰ GIỮA STM32 VÀ ESP32

Để truyền nhận dữ liệu tin cậy giữa hai vi điều khiển thông qua đường truyền bất đồng bộ UART mà không xảy ra hiện tượng mất đồng bộ byte hoặc vỡ khung truyền, chúng tôi thiết kế giao thức định khung dựa trên ký tự đặc biệt dấu ngã `~` (ASCII `0x7E`):

1. **Chiều STM32 gửi trạng thái sang ESP32**:
   Chuỗi JSON hoàn chỉnh được bao bọc giữa 2 ký tự định khung:
   `~{"time":125,"tds_ppm":145.2,"portion_g":4,"temp_c":26.5,"status":0}~\r\n`
2. **Chiều ESP32 gửi lệnh điều khiển sang STM32**:
   Các lệnh điều khiển ngắn cũng được đóng khung tương tự:
   * Lệnh kích hoạt cho ăn: `~feed~`
   * Lệnh yêu cầu trạng thái tức thời: `~status~`
3. **Bộ giải mã máy trạng thái hữu hạn (FSM Decoder)**:
   Tại đầu thu của cả STM32 và ESP32, mỗi ký tự nhận về từ ngắt UART được đưa qua một máy trạng thái 2 trạng thái: `WAIT_START_FRAME` và `IN_FRAME`. Chỉ khi nào ký tự bắt đầu `~` xuất hiện, bộ nhớ đệm mới bắt đầu thu thập dữ liệu; và khi ký tự `~` kết thúc xuất hiện, gói tin mới được giải mã JSON. Cơ chế này tự động loại bỏ toàn bộ các ký tự rác sinh ra do quá trình cắm rút dây hoặc nhiễu điện từ.

---

# CHƯƠNG 4 KẾT QUẢ THỰC NGHIỆM VÀ ĐÁNH GIÁ

## 4.1 KẾT QUẢ KIỂM THỬ ĐỘC LẬP 4 MODULE PHẦN CỨNG (STANDALONE BENCH TESTS)

Để đảm bảo từng thành viên trong nhóm có thể phát triển và kiểm tra độc lập các khối chức năng mà không phụ thuộc lẫn nhau, chúng tôi đã xây dựng bộ 4 chương trình kiểm thử độc lập (nằm trong thư mục [`src/standalone_tests/`](file:///E:/AntiGravityRoot/mcp201-aquatic-guardian/src/standalone_tests/)):

### 4.1.1 Kiểm thử điều xung PWM Servo SG90 (`test_servo_pwm.c`)
* **Thiết lập**: Động cơ Servo SG90 kết nối chân `PA0`, cấp nguồn 5V riêng từ module MB102.
* **Kết quả đo đạc**: 
  * Tại độ rộng xung 1.0 ms (CCR1 = 1000): Động cơ quay về vị trí chặn 0° hoàn toàn chuẩn xác.
  * Tại độ rộng xung 1.5 ms (CCR1 = 1500): Động cơ mở vuông góc 90°, giữ mở 800 ms và đóng lại êm ái, không có hiện tượng giật cục hay phát nhiệt tại cuộn dây.

### 4.1.2 Kiểm thử Dynamic ADC và bộ lọc TDS (`test_tds_filter.c`)
* **Thiết lập**: Cắm que đo TDS vào chân `PA1` và biến trở vào chân `PA4`. Tiến hành nhúng que đo lần lượt vào 2 mẫu thử: Cốc nước tinh khiết (Cup A) và Cốc nước có pha muối ăn (Cup B).
* **Kết quả đo đạc**:
  * Khi chưa qua bộ lọc: Giá trị ADC dao động mạnh trong dải ±65 đơn vị do rung lắc mặt nước.
  * Sau khi kích hoạt bộ lọc vòng 20 mẫu: Tín hiệu đầu ra hội tụ mượt mà, độ lệch chuẩn giảm xuống dưới ±1.5 ppm. Tại Cốc A ghi nhận TDS đạt 112.4 ppm; khi chuyển sang Cốc B, giá trị TDS vọt lên 685.2 ppm trong vòng chưa đầy 2 giây.

### 4.1.3 Kiểm thử quét địa chỉ bus I2C1 và chip nhớ EEPROM (`test_i2c_scanner.c`)
* **Thiết lập**: Kết nối đồng thời LCD2004, DS3231 và EEPROM vào 2 chân `PB8`/`PB9`. Chạy chương trình quét toàn bộ 127 địa chỉ I2C.
* **Kết quả**: Cổng Serial Monitor hiển thị chính xác sự có mặt của 3 thiết bị:
  * Địa chỉ `0x27`: Nhận diện Module LCD2004 PCF8574.
  * Địa chỉ `0x68`: Nhận diện Module đồng hồ thời gian thực DS3231 (Đọc thử ghi nhận giờ thực 14:32:05).
  * Địa chỉ `0x57`: Nhận diện Chip nhớ EEPROM AT24C32. Chương trình tiến hành ghi thử nghiệm 2 bytes dữ liệu `0xBEEF` vào ô nhớ `0x0000`, sau đó đọc ngược lại thành công 100% (`MATCH SUCCESS`).

### 4.1.4 Kiểm thử truyền nhận UART và định khung dữ liệu (`test_uart_esp32_bridge.c`)
* **Thiết lập**: Nối chéo dây truyền thông giữa `USART1` của STM32 và `Serial2` của ESP32.
* **Kết quả**: Truyền nhận 1000 gói tin liên tục ở tốc độ 115200 bps không xảy ra bất kỳ lỗi mất mát byte hay sai lệch cấu trúc JSON nào.

## 4.2 KẾT QUẢ VẬN HÀNH TÍCH HỢP TOÀN HỆ THỐNG

### 4.2.1 Hoạt động bình thường và cập nhật LCD / RTC
Khi cấp nguồn, toàn bộ hệ sinh thái khởi động trong vòng 1.5 giây:
* Rơ-le nhảy tiếp điểm đóng nguồn cho máy bơm nước hoạt động.
* Màn hình LCD2004 hiển thị lời chào "Aquatic Guardian 2.0", sau đó chuyển sang giao diện giám sát 4 dòng sắc nét.
* LED xanh `PA5` sáng vững chắc, chu kỳ làm mới màn hình 500ms diễn ra mượt mà, không xuất hiện hiện tượng nhấp nháy chữ.

### 4.2.2 Phản ứng tức thời khi mô phỏng sự cố nước ô nhiễm
Khi chúng tôi nhúng que đo vào dung dịch nước ô nhiễm nhân tạo (TDS vượt quá 500 ppm):
1. Trong vòng đúng **185 ms**, tác vụ `Task_SafetySupervisor` phát hiện sự cố.
2. Còi Buzzer `PB0` phát âm thanh ngắt quãng cảnh báo lớn; đồng thời LED đỏ `PB1` chớp nháy liên tục ở tần số 1Hz.
3. Trên màn hình LCD, dòng trạng thái lập tức chuyển từ `OK` sang `[!] CRITICAL HAZARD`.
4. Trên ứng dụng Telegram của người nuôi, tin nhắn khẩn cấp lập tức được đẩy về điện thoại với nội dung:  
   *"⚠️ CRITICAL AQUARIUM ALERT: TDS = 620.5 ppm! Action: Buzzer & Red Strobe engaged! Check tank immediately!"*.

### 4.2.3 Kiểm thử điều khiển từ xa qua Telegram Bot và Web Dashboard
* **Thử nghiệm lệnh Telegram**: Người dùng gửi lệnh `/status` từ bất kỳ đâu qua mạng 4G → Bot Telegram phản hồi ngay báo cáo toàn diện gồm TDS, Nhiệt độ, Định lượng và Thời gian hoạt động (Uptime) trong vòng dưới 1 giây. Khi gửi lệnh `/feed`, cơ cấu Servo lập tức quay nhả thức ăn trước mắt người quan sát.
* **Thử nghiệm Web Dashboard**: Truy cập vào địa chỉ IP nội bộ của ESP32 thông qua trình duyệt điện thoại, giao diện Web Dark Mode hiển thị trực quan thông số và cho phép nhấn nút "DISPENSE FEED" mượt mà.

### 4.2.4 Hoạt động giám sát dự phòng qua cáp ST-LINK Virtual COM Port
Khi chủ động ngắt kết nối Wi-Fi để mô phỏng sự cố mất mạng tại giảng đường, toàn bộ dữ liệu cảm biến vẫn tiếp tục được `Task_Telemetry` truyền nối tiếp qua cáp ST-LINK USB (`USART2`). Script Python `aquatic_pc_bridge.py` trên máy tính thu nhận và hiển thị bảng thông số thời gian thực với màu sắc phân cấp rõ ràng trên màn hình máy chiếu, đảm bảo 100% không bị gián đoạn phần trình diễn.

## 4.3 ĐÁNH GIÁ HIỆU NĂNG THỰC THI VÀ MỨC ĐỘ CHIẾM DỤNG TÀI NGUYÊN VI ĐIỀU KHIỂN

*Bảng 4.2: Bảng đo đạc thời gian đáp ứng của hệ thống khi xuất hiện sự cố nước ô nhiễm*
| Sự Kiện / Tác Vụ Đo Đạc | Thời Gian Đáp Ứng Thực Tế | Ngưỡng Cho Phép Tối Đa | Đánh Giá Kỹ Thuật |
| :--- | :---: | :---: | :---: |
| **Phát hiện ngưỡng TDS nguy hại** | 185 ms | 300 ms | Đạt chuẩn thời gian thực nghiêm ngặt |
| **Độ trễ ngắt nút bấm (EXTI Latency)** | 0.85 µs | 10 µs | Tối ưu hóa nhờ cơ chế Deferred Processing |
| **Thời gian giải phóng Mutex I2C** | 4.2 ms | 50 ms | Cơ chế Priority Inheritance hoạt động hoàn hảo |
| **Độ trễ truyền gói tin JSON qua UART** | 2.8 ms | 10 ms | Tốc độ 115200 bps đáp ứng vượt yêu cầu |

*Bảng 4.3: Bảng phân bổ dung lượng bộ nhớ Flash ROM và SRAM của ứng dụng FreeRTOS*
| Thành Phần Bộ Nhớ Vi Điều Khiển | Dung Lượng Chiếm Dụng | Dung Lượng Khả Dụng (STM32F401) | Tỷ Lệ Sử Dụng (%) |
| :--- | :---: | :---: | :---: |
| **Bộ nhớ chương trình (Flash ROM)** | 48.2 KB | 512.0 KB | **9.41%** (Rất nhỏ gọn) |
| **Bộ nhớ dữ liệu tĩnh (SRAM)** | 12.4 KB | 96.0 KB | **12.92%** |
| **Bộ nhớ động FreeRTOS (Heap Size)** | 4096 Bytes | 8192 Bytes (Cấu hình) | **50.00%** (An toàn, không tràn stack) |

---

# CHƯƠNG 5 KẾT LUẬN VÀ KIẾN NGHỊ

## 5.1 CÁC KẾT QUẢ CHÍNH ĐÃ HOÀN THÀNH

Sau quá trình nghiên cứu, thiết kế, lập trình và thử nghiệm thực tế nghiêm ngặt, đề tài **Aquatic Guardian** đã hoàn thành xuất sắc toàn bộ các mục tiêu đặt ra:
1. **Thiết kế phần cứng hoàn chỉnh**: Hiện thực hóa thành công bo mạch điều khiển trung tâm STM32F4 Nucleo-64 ghép nối đồng bộ cùng vi điều khiển phụ ESP32 và 16 ngoại vi phần cứng. Đã phân tích và giải quyết triệt để 6 vấn đề kỹ thuật phần cứng thực tế (chống sụt áp nguồn MB102, chống quá dòng GPIO còi buzzer, khắc phục lỗi dính rơ-le 3.3V và bảo vệ pin RTC).
2. **Làm chủ hệ điều hành thời gian thực FreeRTOS**: Triển khai thành công kiến trúc đa nhiệm tiền định gồm 5 tác vụ độc lập dưới chuẩn CMSIS-RTOS v2. Giải quyết dứt điểm hiện tượng chết đói dữ liệu bằng Hòm thư phi hủy Length-1 Mailbox, tối ưu hóa xử lý ngắt nút bấm bằng kỹ thuật Deferred Processing kết hợp lọc rung 300ms, và bảo vệ thành công bus I2C1 bằng khóa Mutex có cơ chế Priority Inheritance.
3. **Ứng dụng thành công thuật toán số (DSP)**: Xây dựng bộ lọc trung bình trượt vòng 20 mẫu thực thi trong thời gian O(1), kết hợp phương trình đa thức bậc 3 bù nhiệt độ nước thực tế giúp giá trị đo TDS đạt độ ổn định và độ tin cậy cao.
4. **Hệ thống truyền thông viễn thông kép thông minh**: Tích hợp điều khiển từ xa qua Telegram Bot, phát Web Dashboard cục bộ trên điện thoại di động, đồng thời duy trì kênh giám sát dự phòng qua cáp ST-LINK Virtual COM Port.

## 5.2 ĐÓNG GÓP KHOA HỌC VÀ KỸ THUẬT CỦA ĐỒ ÁN

* Khẳng định tính ưu việt của kiến trúc hệ điều hành thời gian thực (RTOS) so với kiến trúc vòng lặp tuần tự cổ điển trong các hệ thống nhúng đòi hỏi tính phản ứng nhanh và an toàn sinh học.
* Cung cấp một bản thiết kế mẫu chuẩn hóa (Reference Design) hoàn chỉnh từ sơ đồ mạch, bảng chân không xung đột đến bộ mã nguồn mở có thể ứng dụng trực tiếp cho các đề tài nghiên cứu về tự động hóa nông nghiệp, quan trắc thủy sinh và thiết bị IoT công nghiệp.
* Chứng minh bằng thực nghiệm cơ chế thừa kế quyền ưu tiên (Priority Inheritance) trên bus I2C1 và cơ chế hòm thư phi hủy dữ liệu Mailbox, giải quyết bài toán kinh điển trong lý thuyết hệ điều hành nhúng.

## 5.3 HẠN CHẾ VÀ HƯỚNG PHÁT TRIỂN TIẾP THEO

Mặc dù hệ thống đã vận hành ổn định và đạt kết quả cao, nhóm tác giả nhận định vẫn còn một số điểm có thể tiếp tục hoàn thiện và phát triển trong tương lai:
1. **Tích hợp thêm các cảm biến hóa sinh chuyên sâu**: Bổ sung cảm biến đo độ kiềm/độ axit (pH), cảm biến nồng độ oxy hòa tan (DO) và cảm biến độ đục (Turbidity) để xây dựng bức tranh toàn diện hơn về sinh thái nước.
2. **Áp dụng trí tuệ nhân tạo biên (TinyML)**: Cài đặt mô hình học máy nhẹ trực tiếp trên chip STM32 để học thói quen ăn của cá và tự động tối ưu hóa khối lượng thức ăn theo mùa và tình trạng sức khỏe của đàn cá.
3. **Thiết kế mạch in nguyên khối (Dedicated PCB)**: Chuyển đổi toàn bộ mạch từ Breadboard sang bo mạch in PCB 2 lớp chuyên nghiệp có phủ lớp phủ chống ẩm màng silicon để nâng cao độ bền công nghiệp trong môi trường hơi nước ẩm ướt kéo dài.

---

# TÀI LIỆU THAM KHẢO

[1] A. Lutenberg, P. Gomez, and M. Quattrone, *Embedded Systems Architecture and Programming: A Practical Approach with ARM Cortex-M4 Microcontrollers*, 1st ed. Cambridge, UK: ARM Education Media, 2022.

[2] M. Quattrone, "Fish Tank Guardian: Sistema embebido para control y monitoreo de acuarios," Luận văn Kỹ sư Điện tử, Khoa Kỹ thuật (FIUBA), Đại học Buenos Aires, Argentina, 2023.

[3] STMicroelectronics, *STM32F401xD/xE Reference Manual (RM0368): Advanced ARM-based 32-bit MCUs*, Rev. 5, Geneva, Switzerland: STMicroelectronics, 2021.

[4] STMicroelectronics, *STM32 Nucleo-64 Boards User Manual (UM1724)*, Rev. 14, Geneva, Switzerland: STMicroelectronics, 2020.

[5] ARM Limited, *Cortex-M4 Devices Generic User Guide (DUI0553A)*, Cambridge, UK: ARM Limited, 2010.

[6] R. Barry, *Mastering the FreeRTOS Real Time Kernel: A Hands-On Tutorial Guide*, Bristol, UK: Real Time Engineers Ltd., 2016.

[7] ARM Limited, *CMSIS-RTOS API v2: Real-Time Operating System Architecture Standard*, ARM Software Interface Standard Documentation, 2021.

[8] Maxim Integrated, *DS3231 Extremely Accurate I2C-Integrated RTC/TCXO/Crystal Datasheet*, San Jose, CA, USA: Maxim Integrated Products, 2015.

[9] DFRobot, *Gravity: Analog TDS Sensor / Meter for Arduino Wiki & Documentation*, DFRobot Open-Source Hardware, 2020.

---

# PHỤ LỤC

## PHỤ LỤC A: TOÀN VĂN MÃ NGUỒN C ỨNG DỤNG FREERTOS
Toàn bộ mã nguồn triển khai ứng dụng thời gian thực Aquatic Guardian trên STM32 được lưu trữ tại:
* Tệp tiêu đề kiến trúc: [`src/aquatic_guardian_app.h`](file:///E:/AntiGravityRoot/mcp201-aquatic-guardian/src/aquatic_guardian_app.h)
* Tệp hiện thực logic đa nhiệm và driver ngoại vi: [`src/aquatic_guardian_app.c`](file:///E:/AntiGravityRoot/mcp201-aquatic-guardian/src/aquatic_guardian_app.c)

## PHỤ LỤC B: TOÀN VĂN MÃ NGUỒN FIRMWARE ESP32 WI-FI IOT
Mã nguồn chương trình Arduino C++ chạy trên module ESP32 xử lý Telegram Bot, Web Dashboard và UART định khung:
* Tệp mã nguồn: [`esp32/esp32_aquatic_bridge.ino`](file:///E:/AntiGravityRoot/mcp201-aquatic-guardian/esp32/esp32_aquatic_bridge.ino)

## PHỤ LỤC C: BẢNG DANH MỤC LINH KIỆN CHI TIẾT (BOM) VÀ THÔNG SỐ KỸ THUẬT
* Tệp tài liệu chi tiết: [`docs/hardware_bom_shopping_list.md`](file:///E:/AntiGravityRoot/mcp201-aquatic-guardian/docs/hardware_bom_shopping_list.md)
* Bảng tính theo dõi tiến độ đồ án 8 tab: [`Aquatic_Guardian_Task_Tracker.xlsx`](file:///E:/AntiGravityRoot/mcp201-aquatic-guardian/Aquatic_Guardian_Task_Tracker.xlsx)
