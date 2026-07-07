#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>
#include <cstdint>

// ----- WiFi & MQTT Settings (replace with your own) -----
constexpr const char* WIFI_SSID = "Zeca";             // WiFi SSID
constexpr const char* WIFI_PASSWORD = "zecas1301"; // WiFi password
constexpr const char* MQTT_BROKER = "broker.hivemq.com"; // Public HiveMQ broker
const uint16_t MQTT_PORT = 1883;               // MQTT broker port
constexpr const char* MQTT_TOPIC = "esp32/rfid";        // Topic to publish UID
constexpr const char* MQTT_TOPIC_RESPONSE = "esp32/rfid/response"; // Topic to receive validation response

// ----- Authorized Users -----
constexpr const char* AUTHORIZED_UID_ISRAEL = "E2:00:80:05"; // Israel's tag UID
constexpr const char* AUTHORIZED_UID_PEDRO = "D1:DF:A3:A4";  // Pedro's tag UID

#endif // CONFIG_H
