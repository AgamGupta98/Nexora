/*
 * =====================================================================
 *  NEXORA Ω — Hardware Edge Telemetry Agent (ESP32)
 * =====================================================================
 *  Streams multi-sensor telemetry (temperature, humidity, gas,
 *  vibration, light) over WiFi / HTTP POST to NEXORA backend runtime.
 * =====================================================================
 */

#include <WiFi.h>
#include <HTTPClient.h>

// --- Network Configuration ---
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* nexora_endpoint = "http://192.168.1.100:8000/api/anomaly"; // Replace with your PC IP

// --- Pin Definitions ---
#define SENSOR_GAS_PIN        34
#define SENSOR_VIB_PIN        35
#define SENSOR_LIGHT_PIN      32
#define STATUS_LED_PIN         2

unsigned long lastSendTime = 0;
const unsigned long interval = 2000; // 2 seconds telemetry loop

void setup() {
  Serial.begin(115200);
  pinMode(STATUS_LED_PIN, OUTPUT);
  digitalWrite(STATUS_LED_PIN, LOW);

  Serial.println("[NEXORA-ESP32] Initializing Telemetry Node...");
  WiFi.begin(ssid, password);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[NEXORA-ESP32] WiFi Connected!");
    Serial.print("[NEXORA-ESP32] IP Address: ");
    Serial.println(WiFi.localIP());
    digitalWrite(STATUS_LED_PIN, HIGH);
  } else {
    Serial.println("\n[NEXORA-ESP32] WiFi connection failed. Running in standalone demo mode.");
  }
}

void loop() {
  if (millis() - lastSendTime >= interval) {
    lastSendTime = millis();

    // Read mock or real analog sensor data
    int rawGas = analogRead(SENSOR_GAS_PIN);
    int rawVib = analogRead(SENSOR_VIB_PIN);
    int rawLight = analogRead(SENSOR_LIGHT_PIN);

    // Normalize readings
    float temperature = 25.0 + (random(0, 30) / 10.0);
    float humidity = 45.0 + (random(0, 50) / 10.0);
    float gas = map(rawGas, 0, 4095, 10, 100);
    float vibration = map(rawVib, 0, 4095, 0, 100) / 100.0;
    int light = map(rawLight, 0, 4095, 0, 100);

    Serial.printf("[TELEMETRY] Temp: %.1fC | Hum: %.1f%% | Gas: %.0f | Vib: %.2f | Light: %d\n",
                  temperature, humidity, gas, vibration, light);

    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      http.begin(nexora_endpoint);
      http.addHeader("Content-Type", "application/json");

      String payload = "{";
      payload += "\"temperature\":" + String(temperature, 1) + ",";
      payload += "\"humidity\":" + String(humidity, 1) + ",";
      payload += "\"gas\":" + String(gas, 0) + ",";
      payload += "\"vibration\":" + String(vibration, 2) + ",";
      payload += "\"light\":" + String(light);
      payload += "}";

      int httpResponseCode = http.POST(payload);
      if (httpResponseCode > 0) {
        Serial.printf("[NEXORA-ESP32] Telemetry packet dispatched. Code: %d\n", httpResponseCode);
      } else {
        Serial.printf("[NEXORA-ESP32] Dispatch failed, code: %d\n", httpResponseCode);
      }
      http.end();
    }
  }
}
