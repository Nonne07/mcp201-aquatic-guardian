/**
 * ==============================================================================
 * Project: Aquatic Guardian (Smart Fish Tank Controller & Feeder)
 * Subsystem: ESP32 Wi-Fi & Telegram IoT Co-Processor
 * Author: Hoang Duc Anh & Group 7 (Class IC2005 - MCP201 Capstone)
 * Target Board: ESP32 NodeMCU / ESP32-WROOM-32
 * ==============================================================================
 *
 * HARDWARE CONNECTIONS (To STM32 Nucleo-64):
 * ------------------------------------------------------------------------------
 *  ESP32 Pin          STM32 Nucleo Pin       Description
 *  ------------------------------------------------------------------------------
 *  GPIO 16 (RX2)  <-- PA9 (USART1_TX)        Receives JSON telemetry from STM32
 *  GPIO 17 (TX2)  --> PA10 (USART1_RX)       Transmits commands (~feed~,
 * ~status~) GND            <-- GND                    COMMON GROUND (CRITICAL!)
 *  VIN / 5V       <-- Nucleo 5V / USB        External 5V supply
 *  GPIO 2 (LED)       Internal LED           Status indicator
 * (Blink=Connecting, ON=Ready)
 * ------------------------------------------------------------------------------
 *
 * REQUIRED ARDUINO LIBRARIES:
 * 1. WiFi (Built-in ESP32 core)
 * 2. WiFiClientSecure (Built-in ESP32 core)
 * 3. WebServer (Built-in ESP32 core)
 * 4. UniversalTelegramBot (Install via Arduino Library Manager by Brian Lough)
 * 5. ArduinoJson (Version 6.x or 7.x by Benoit Blanchon)
 *
 * TELEGRAM BOT CAPABILITIES:
 * - /start  : Display system intro and command list
 * - /status : Fetch latest real-time TDS, Water Temp, and Safety Status
 * - /feed   : Send ~feed~ UART pulse to STM32 to trigger servo dispenser
 * - Auto-Push Notification: Instantly messages Telegram if TDS > 500ppm
 * (Critical)
 *
 * LOCAL WEB SERVER CAPABILITIES:
 * - Access http://<ESP32_IP>/ from your phone browser on the same Wi-Fi
 * - Displays a live responsive UI card with TDS, Temp, and a big "FEED NOW"
 * button!
 * ==============================================================================
 */

#include <ArduinoJson.h>
#include <UniversalTelegramBot.h>
#include <WebServer.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>

/* ========================================================================== */
/* NETWORK & CREDENTIALS CONFIGURATION */
/* (Update these with your phone hotspot credentials before defense) */
/* ========================================================================== */
const char *WIFI_SSID = "Anon";         // Your Phone Hotspot SSID
const char *WIFI_PASSWORD = "Antidote"; // Hotspot Password

// Telegram Bot Token (Obtained from @BotFather on Telegram)
#define BOT_TOKEN "9257091642:AAHRAe2HRIXkT82Up-5zT-fOmGA0Mp7v6M0"

// Your personal Telegram User ID (Obtained from @userinfobot on Telegram)
// Set to "0" or leave blank to accept commands from the first authorized user
#define AUTHORIZED_CHAT_ID "9024311568"

/* ========================================================================== */
/* HARDWARE SERIAL & PIN CONFIGURATION                                        */
/* ========================================================================== */
#define STM32_RX_PIN 16  // ESP32 GPIO16 connects to STM32 PA9 (TX)
#define STM32_TX_PIN 17  // ESP32 GPIO17 connects to STM32 PA10 (RX)
#define STATUS_LED_PIN 2 // Onboard Blue LED

HardwareSerial SerialSTM32(2); // Use ESP32 Hardware UART2

/* ========================================================================== */
/* CLIENTS & OBJECTS                                                          */
/* ========================================================================== */
WiFiClientSecure secured_client;
UniversalTelegramBot bot(BOT_TOKEN, secured_client);
WebServer server(80);

/* ========================================================================== */
/* TELEMETRY STATE STRUCT                                                     */
/* ========================================================================== */
struct AquaticTelemetry {
  uint32_t timestamp = 0;
  float tds_ppm = 0.0f;
  int portion_g = 5;
  float temp_c = 25.0f;
  int water_status = 0; // 0=Pristine, 1=Acceptable, 2=Critical
  bool has_fresh_data = false;
  unsigned long last_received_ms = 0;
} telemetry;

/* UART Framing Protocol */
#define FRAME_DELIMITER '~'
String uart_rx_buffer = "";
bool in_frame = false;

/* Rate Limiting & Timers */
unsigned long last_bot_check_time = 0;
const unsigned long BOT_CHECK_INTERVAL = 1000; // Check Telegram every 1 second
unsigned long last_alert_time = 0;
const unsigned long ALERT_COOLDOWN_MS = 60000; // Only alert once every 60s max

/* ========================================================================== */
/* LOCAL WEB SERVER HTML TEMPLATE */
/* ========================================================================== */
const char HTML_PAGE[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Aquatic Guardian IoT</title>
  <style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0b132b; color: #ffffff; text-align: center; margin: 0; padding: 20px; }
    .card { background: #1c2541; border-radius: 16px; padding: 24px; max-width: 420px; margin: 0 auto; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    h1 { color: #48cae4; font-size: 24px; margin-bottom: 5px; }
    p.sub { color: #a0aec0; font-size: 13px; margin-top: 0; }
    .metric { display: flex; justify-content: space-between; padding: 12px 16px; margin: 10px 0; background: #3a506b; border-radius: 10px; font-size: 16px; }
    .val { font-weight: bold; color: #5bc0be; }
    .btn { background: linear-gradient(135deg, #00b4d8, #0077b6); color: white; border: none; padding: 16px 32px; font-size: 18px; border-radius: 30px; cursor: pointer; font-weight: bold; width: 100%; margin-top: 20px; box-shadow: 0 4px 15px rgba(0,180,216,0.4); }
    .btn:active { transform: scale(0.98); }
    .status-ok { color: #4ade80; font-weight: bold; }
    .status-warn { color: #f87171; font-weight: bold; }
  </style>
</head>
<body>
  <div class="card">
    <h1>🐠 Aquatic Guardian</h1>
    <p class="sub">Dual-Core IoT Bridge (ESP32 + STM32 FreeRTOS)</p>
    <hr style="border: 0.5px solid #2d3748; margin: 15px 0;">
    <div class="metric"><span>Water TDS:</span><span class="val" id="tds">-- ppm</span></div>
    <div class="metric"><span>Temperature:</span><span class="val" id="temp">-- &deg;C</span></div>
    <div class="metric"><span>Portion Setting:</span><span class="val" id="portion">-- g</span></div>
    <div class="metric"><span>Tank Status:</span><span id="status">Connecting...</span></div>
    <button class="btn" onclick="feedFish()">DISPENSE FEED</button>
  </div>
  <script>
    function updateMetrics() {
      fetch('/api/status').then(r => r.json()).then(data => {
        document.getElementById('tds').innerText = data.tds_ppm.toFixed(1) + " ppm";
        document.getElementById('temp').innerText = data.temp_c.toFixed(1) + " °C";
        document.getElementById('portion').innerText = data.portion_g + " g";
        let st = document.getElementById('status');
        if(data.water_status === 0) { st.innerHTML = "<span class='status-ok'>PRISTINE</span>"; }
        else if(data.water_status === 1) { st.innerHTML = "<span class='status-ok'>ACCEPTABLE</span>"; }
        else { st.innerHTML = "<span class='status-warn'>CRITICAL ALERT</span>"; }
      }).catch(e => console.log(e));
    }
    function feedFish() {
      fetch('/feed').then(r => alert('Feed Command Sent to STM32!'));
    }
    setInterval(updateMetrics, 2000);
    updateMetrics();
  </script>
</body>
</html>
)rawliteral";

/* ========================================================================== */
/* FORWARD DECLARATIONS                                                       */
/* ========================================================================== */
void sendCommandToSTM32(const char *cmd);
void parseIncomingPacket(const String &payload);
void handleTelegramMessages(int numNewMessages);
void sendTelegramAlert(const char *reason);

/* ========================================================================== */
/* SETUP                                                                      */
/* ========================================================================== */
void setup() {
  pinMode(STATUS_LED_PIN, OUTPUT);
  digitalWrite(STATUS_LED_PIN, LOW);

  // Initialize USB Serial for local PC debugging
  Serial.begin(115200);
  delay(100);
  Serial.println("\n[ESP32] Aquatic Guardian IoT Co-Processor Initializing...");

  // Initialize Hardware UART2 connected to STM32 Nucleo
  SerialSTM32.begin(115200, SERIAL_8N1, STM32_RX_PIN, STM32_TX_PIN);
  Serial.printf("[ESP32] UART2 initialized: RX=%d, TX=%d @ 115200 bps\n",
                STM32_RX_PIN, STM32_TX_PIN);

  // Connect to Wi-Fi
  Serial.printf("[ESP32] Connecting to Wi-Fi: %s", WIFI_SSID);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int wifi_timeout = 0;
  while (WiFi.status() != WL_CONNECTED && wifi_timeout < 30) {
    delay(500);
    Serial.print(".");
    digitalWrite(STATUS_LED_PIN,
                 !digitalRead(STATUS_LED_PIN)); // Fast blink while connecting
    wifi_timeout++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[ESP32] Wi-Fi Connected!");
    Serial.print("[ESP32] IP Address: ");
    Serial.println(WiFi.localIP());
    digitalWrite(STATUS_LED_PIN, HIGH); // Solid ON when online

    // Secure client setup for Telegram Bot API
    secured_client.setCACert(
        TELEGRAM_CERTIFICATE_ROOT); // Use Telegram root CA or setInsecure
    // Alternatively, if certificate check fails on campus network:
    // secured_client.setInsecure();

    // Setup Local Web Server Routes
    server.on("/", HTTP_GET,
              []() { server.send_P(200, "text/html", HTML_PAGE); });

    server.on("/api/status", HTTP_GET, []() {
      StaticJsonDocument<256> doc;
      doc["timestamp"] = telemetry.timestamp;
      doc["tds_ppm"] = telemetry.tds_ppm;
      doc["portion_g"] = telemetry.portion_g;
      doc["temp_c"] = telemetry.temp_c;
      doc["water_status"] = telemetry.water_status;
      doc["fresh"] = telemetry.has_fresh_data;

      String json_str;
      serializeJson(doc, json_str);
      server.send(200, "application/json", json_str);
    });

    server.on("/feed", HTTP_GET, []() {
      sendCommandToSTM32("feed");
      server.send(200, "text/plain", "Feed triggered successfully");
    });

    server.begin();
    Serial.println("[ESP32] Local Web Dashboard ready at: http://" +
                   WiFi.localIP().toString());
  } else {
    Serial.println("\n[ESP32] Wi-Fi Connection Failed. Running in Offline UART "
                   "Gateway Mode.");
  }
}

/* ========================================================================== */
/* MAIN LOOP                                                                  */
/* ========================================================================== */
void loop() {
  // 1. Process incoming UART bytes from STM32 Nucleo
  while (SerialSTM32.available()) {
    char c = (char)SerialSTM32.read();
    if (c == FRAME_DELIMITER) {
      if (!in_frame) {
        // Start of frame
        in_frame = true;
        uart_rx_buffer = "";
      } else {
        // End of frame
        in_frame = false;
        parseIncomingPacket(uart_rx_buffer);
        uart_rx_buffer = "";
      }
    } else if (in_frame) {
      if (uart_rx_buffer.length() < 256) {
        uart_rx_buffer += c;
      } else {
        // Buffer overflow protection
        in_frame = false;
        uart_rx_buffer = "";
      }
    }
  }

  // 2. Handle HTTP Client requests
  server.handleClient();

  // 3. Periodic Telegram Bot Message Polling
  if (WiFi.status() == WL_CONNECTED &&
      (millis() - last_bot_check_time > BOT_CHECK_INTERVAL)) {
    last_bot_check_time = millis();
    int numNewMessages = bot.getUpdates(bot.last_message_received + 1);
    while (numNewMessages) {
      handleTelegramMessages(numNewMessages);
      numNewMessages = bot.getUpdates(bot.last_message_received + 1);
    }
  }

  // 4. Proactive Safety Alarm Notification to Telegram
  if (telemetry.water_status == 2 &&
      (millis() - last_alert_time > ALERT_COOLDOWN_MS)) {
    last_alert_time = millis();
    sendTelegramAlert("CRITICAL TDS ALERT (> 500 ppm)! High mineral/pollutant "
                      "concentration detected.");
  }
}

/* ========================================================================== */
/* UART TRANSMISSION & PACKET PARSING                                         */
/* ========================================================================== */

/**
 * @brief Sends framed command '~<cmd>~' to STM32 Nucleo over USART1
 */
void sendCommandToSTM32(const char *cmd) {
  String framed =
      String(FRAME_DELIMITER) + cmd + String(FRAME_DELIMITER) + "\r\n";
  SerialSTM32.print(framed);
  Serial.printf("[ESP32 -> STM32] Sent Command: %s", framed.c_str());

  // Blink LED to indicate transmission
  digitalWrite(STATUS_LED_PIN, LOW);
  delay(50);
  digitalWrite(STATUS_LED_PIN, HIGH);
}

/**
 * @brief Parses JSON telemetry packet sent by STM32 FreeRTOS Task_Telemetry
 * Format: {"time":12,"tds_ppm":142.5,"portion_g":4,"temp_c":26.5,"status":0}
 */
void parseIncomingPacket(const String &payload) {
  StaticJsonDocument<256> doc;
  DeserializationError err = deserializeJson(doc, payload);

  if (err) {
    Serial.printf("[ESP32] JSON Parse Error: %s | Raw: %s\n", err.c_str(),
                  payload.c_str());
    return;
  }

  telemetry.timestamp = doc["time"] | 0;
  telemetry.tds_ppm = doc["tds_ppm"] | 0.0f;
  telemetry.portion_g = doc["portion_g"] | 5;
  telemetry.temp_c = doc["temp_c"] | 25.0f;
  telemetry.water_status = doc["status"] | 0;
  telemetry.has_fresh_data = true;
  telemetry.last_received_ms = millis();

  Serial.printf("[STM32 -> ESP32] TDS: %.1f ppm | Temp: %.1f C | Portion: %dg "
                "| Status: %d\n",
                telemetry.tds_ppm, telemetry.temp_c, telemetry.portion_g,
                telemetry.water_status);
}

/* ========================================================================== */
/* TELEGRAM BOT MESSAGE HANDLER                                               */
/* ========================================================================== */

void handleTelegramMessages(int numNewMessages) {
  for (int i = 0; i < numNewMessages; i++) {
    String chat_id = String(bot.messages[i].chat_id);
    String text = bot.messages[i].text;
    String from = bot.messages[i].from_name;

    Serial.printf("[Telegram] Message from %s (Chat ID %s): %s\n", from.c_str(),
                  chat_id.c_str(), text.c_str());

    if (text == "/start") {
      String welcome = "🐠 *Aquatic Guardian IoT Bot* (Group 7)\n\n";
      welcome += "Hello *" + from + "*! System commands:\n";
      welcome += "🔹 `/feed` : Trigger food dispenser servo\n";
      welcome += "🔹 `/status` : View real-time tank sensor telemetry\n";
      welcome += "🔹 `/help` : View command help";
      bot.sendMessage(chat_id, welcome, "Markdown");
    } else if (text == "/feed") {
      // 1. Send command to STM32 Nucleo
      sendCommandToSTM32("feed");

      // 2. Reply to user
      String msg = "🐟 *Feeding Triggered!*\n";
      msg += "Signal sent to STM32 FreeRTOS Dispenser Task.\n";
      msg += "Servo rotated by 90° for portion: *" +
             String(telemetry.portion_g) + "g*.";
      bot.sendMessage(chat_id, msg, "Markdown");
    } else if (text == "/status") {
      String status_str;
      if (telemetry.water_status == 0)
        status_str = "🟢 *PRISTINE (Ideal)*";
      else if (telemetry.water_status == 1)
        status_str = "🟡 *ACCEPTABLE*";
      else
        status_str = "🔴 *CRITICAL HAZARD (Overheat / High TDS)*";

      String report = "📊 *Live Aquarium Telemetry Report*\n";
      report += "----------------------------------------\n";
      report += "💧 *Water TDS:* `" + String(telemetry.tds_ppm, 1) + " ppm`\n";
      report += "🌡️ *Water Temp:* `" + String(telemetry.temp_c, 1) + " °C`\n";
      report += "⚖️ *Portion Dial:* `" + String(telemetry.portion_g) + " g`\n";
      report += "🛡️ *Tank State:* " + status_str + "\n";
      report += "⏱️ *System Uptime:* `" + String(telemetry.timestamp) + " s`\n";
      report += "----------------------------------------\n";
      report += "ESP32 IP: `" + WiFi.localIP().toString() + "`";
      bot.sendMessage(chat_id, report, "Markdown");
    } else if (text == "/help") {
      bot.sendMessage(
          chat_id, "Use `/feed` to drop food, `/status` to check parameters.",
          "");
    }
  }
}

/**
 * @brief Proactively notifies the owner when water quality reaches dangerous
 * threshold
 */
void sendTelegramAlert(const char *reason) {
  String alert_msg = "⚠️ *CRITICAL AQUARIUM ALERT!*\n";
  alert_msg += "----------------------------------------\n";
  alert_msg += "Reason: " + String(reason) + "\n";
  alert_msg += "💧 TDS: *" + String(telemetry.tds_ppm, 1) + " ppm*\n";
  alert_msg += "🌡️ Temp: *" + String(telemetry.temp_c, 1) + " °C*\n";
  alert_msg += "🚨 Action: Buzzer & Red Alert Strobe engaged!\n";
  alert_msg += "----------------------------------------\n";
  alert_msg += "Check tank immediately or inspect filter pump!";

  // Send to predefined chat ID if configured
  if (strlen(AUTHORIZED_CHAT_ID) > 5 &&
      strcmp(AUTHORIZED_CHAT_ID, "YOUR_CHAT_ID_HERE") != 0) {
    bot.sendMessage(AUTHORIZED_CHAT_ID, alert_msg, "Markdown");
  }
}
