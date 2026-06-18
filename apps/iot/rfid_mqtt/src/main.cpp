#include <Arduino.h>
#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
#include <PubSubClient.h>

// ----- Pin Definitions -----
#define SS_PIN 5          // VSPI SS (SDA)
#define RST_PIN 22        // VSPI Reset
#define LED_GREEN 2       // Green LED
#define LED_RED 4         // Red LED

#include "config.h"

// ----- Global Objects -----
MFRC522 rfid(SS_PIN, RST_PIN);
WiFiClient espClient;
PubSubClient client(espClient);

void connectToWiFi() {
  Serial.print("Connecting to WiFi ");
  Serial.println(WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print('.');
  }
  Serial.println("\nWiFi connected. IP address: ");
  Serial.println(WiFi.localIP());
}

void connectToMqtt() {
  client.setServer(MQTT_BROKER, MQTT_PORT);
  Serial.print("Connecting to MQTT broker ");
  Serial.println(MQTT_BROKER);
  while (!client.connected()) {
    String clientId = "ESP32-" + String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      Serial.println("MQTT connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 2 seconds");
      delay(2000);
    }
  }
}

String uidToString() {
  String uidStr = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    if (rfid.uid.uidByte[i] < 0x10) uidStr += "0";
    uidStr += String(rfid.uid.uidByte[i], HEX);
    if (i < rfid.uid.size - 1) uidStr += ":";
  }
  uidStr.toUpperCase();
  return uidStr;
}

void setup() {
    Serial.begin(115200);
    // optional: wait for the serial port to be ready (useful on some boards)
    // while (!Serial) { ; }

    SPI.begin();
    rfid.PCD_Init();
    
    // Mostra a versão do firmware do leitor RFID para testar a comunicação SPI
    Serial.print("MFRC522: ");
    rfid.PCD_DumpVersionToSerial();

    pinMode(LED_GREEN, OUTPUT);
    pinMode(LED_RED, OUTPUT);

    // Start with "closed" state (red on)
    digitalWrite(LED_GREEN, LOW);
    digitalWrite(LED_RED, HIGH);

    connectToWiFi();
    connectToMqtt();

    Serial.println("System ready. Await RFID tag...");
}

void loop() {
  if (!client.connected()) {
    connectToMqtt();
  }
  client.loop();

  // Check for new RFID cards
  if (!rfid.PICC_IsNewCardPresent()) return;
  if (!rfid.PICC_ReadCardSerial()) return;

  String uid = uidToString();
  Serial.print("Tag detected! UID: ");
  Serial.println(uid);

  // Publish UID to MQTT
  if (client.publish(MQTT_TOPIC, uid.c_str())) {
    Serial.println("UID published to MQTT");
  } else {
    Serial.println("Failed to publish UID");
  }

  // Alternating red and green LEDs while starting to read/process
  for (int i = 0; i < 10; i++) {
    digitalWrite(LED_RED, i % 2 == 0 ? LOW : HIGH);
    digitalWrite(LED_GREEN, i % 2 == 0 ? HIGH : LOW);
    delay(100);
  }

  // Validate the connection (RFID UID check)
  bool isValid = false;
  String studentName = "";

  if (uid.equalsIgnoreCase(AUTHORIZED_UID_ISRAEL)) {
    isValid = true;
    studentName = "Isreal";
  } else if (uid.equalsIgnoreCase(AUTHORIZED_UID_PEDRO)) {
    isValid = true;
    studentName = "Pedro";
  }

  if (isValid) {
    // Green ON, Red OFF for 10 seconds
    digitalWrite(LED_GREEN, HIGH);
    digitalWrite(LED_RED, LOW);
    Serial.print("Nome do aluno: ");
    Serial.print(studentName);
    Serial.println(": Acesso Liberado!");

    // Keep active state for 10 seconds keeping MQTT alive
    unsigned long startMillis = millis();
    while (millis() - startMillis < 10000) {
      client.loop();
      delay(50);
    }
  } else {
    // Red blinks for 10 seconds, Green OFF
    digitalWrite(LED_GREEN, LOW);
    Serial.println("Nome do aluno: Acesso Negado!");

    unsigned long startMillis = millis();
    unsigned long lastToggle = 0;
    bool redState = false;
    while (millis() - startMillis < 10000) {
      if (millis() - lastToggle >= 250) {
        redState = !redState;
        digitalWrite(LED_RED, redState ? HIGH : LOW);
        lastToggle = millis();
      }
      client.loop();
      delay(10);
    }
  }

  // Return to normal (Red ON, Green OFF)
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_RED, HIGH);
  Serial.println("System closed.");

  rfid.PICC_HaltA();
}
