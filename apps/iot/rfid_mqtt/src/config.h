#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>
#include <cstdint>
// ----- WiFi & MQTT Settings (replace with your own) -----
const char* WIFI_SSID = "YOUR_SSID";          // WiFi SSID
const char* WIFI_PASSWORD = "YOUR_PASSWORD"; // WiFi password
const char* MQTT_BROKER = "broker.hivemq.com"; // MQTT broker host
const uint16_t MQTT_PORT = 1883;               // MQTT broker port
const char* MQTT_TOPIC = "esp32/rfid";        // Topic to publish UID

#endif // CONFIG_H
