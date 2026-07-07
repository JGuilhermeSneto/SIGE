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
#define BUZZER_PIN 15      // Buzzer (passivo)


#include "config.h"


// ----- Global Objects -----
MFRC522 rfid(SS_PIN, RST_PIN);
WiFiClient espClient;
PubSubClient client(espClient);

// ----- Global Variables for MQTT Response -----
volatile bool responseReceived = false;
volatile bool responseAuthorized = false;
String responseName = "";
String waitingUid = "";

// ----- MQTT Callback for Verification -----
void mqttCallback(char* topic, byte* payload, unsigned int length) {
  String msg = "";
  for (unsigned int i = 0; i < length; i++) {
    msg += (char)payload[i];
  }
  Serial.print("\n[MQTT] Message arrived on topic: ");
  Serial.println(topic);
  Serial.print("[MQTT] Payload: ");
  Serial.println(msg);

  if (String(topic).equals(MQTT_TOPIC_RESPONSE)) {
    // Extract UID from JSON: "uid":"..."
    int uidIdx = msg.indexOf("\"uid\":\"");
    if (uidIdx != -1) {
      int start = uidIdx + 7;
      int end = msg.indexOf("\"", start);
      if (end != -1) {
        String rcvUid = msg.substring(start, end);
        // Compare with the UID we are waiting for
        if (rcvUid.equalsIgnoreCase(waitingUid)) {
          responseAuthorized = (msg.indexOf("\"authorized\":true") != -1);
          
          // Extract Name: "name":"..."
          int nameIdx = msg.indexOf("\"name\":\"");
          if (nameIdx != -1) {
            int nStart = nameIdx + 8;
            int nEnd = msg.indexOf("\"", nStart);
            if (nEnd != -1) {
              responseName = msg.substring(nStart, nEnd);
            } else {
              responseName = "";
            }
          } else {
            responseName = "";
          }
          responseReceived = true;
          Serial.println("[MQTT] Validation response processed successfully.");
        }
      }
    }
  }
}



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
      client.subscribe(MQTT_TOPIC_RESPONSE);
      Serial.print("Subscribed to topic: ");
      Serial.println(MQTT_TOPIC_RESPONSE);
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


// ----- Som de acesso liberado -----
void tocarSomLiberado() {
  tone(BUZZER_PIN, 1000, 100);
  delay(120);
  tone(BUZZER_PIN, 1500, 100);
  delay(120);
  tone(BUZZER_PIN, 2000, 200);
  delay(220);
  noTone(BUZZER_PIN);
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
    pinMode(BUZZER_PIN, OUTPUT);
    noTone(BUZZER_PIN);


    // Start with "closed" state (red on)
    digitalWrite(LED_GREEN, LOW);
    digitalWrite(LED_RED, HIGH);


    connectToWiFi();
    connectToMqtt();
    client.setCallback(mqttCallback);


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

  // Set up waiting context for MQTT response callback
  waitingUid = uid;
  responseReceived = false;
  responseAuthorized = false;
  responseName = "";

  // Publish UID to MQTT
  if (client.publish(MQTT_TOPIC, uid.c_str())) {
    Serial.println("UID published to MQTT");
  } else {
    Serial.println("Failed to publish UID");
  }

  // Alternating red and green LEDs while waiting for response (max 2 seconds)
  unsigned long startWait = millis();
  int flashCount = 0;
  while (!responseReceived && (millis() - startWait < 2000)) {
    digitalWrite(LED_RED, flashCount % 2 == 0 ? LOW : HIGH);
    digitalWrite(LED_GREEN, flashCount % 2 == 0 ? HIGH : LOW);
    flashCount++;
    
    client.loop(); // Process incoming messages (triggers mqttCallback)
    delay(100);
  }

  // Validate the connection
  bool isValid = false;
  String studentName = "";

  if (responseReceived) {
    Serial.println("Response received from backend!");
    isValid = responseAuthorized;
    studentName = responseName;
  } else {
    Serial.println("Timeout waiting for backend. Falling back to local offline validation.");
    // Offline fallback using local config cache
    if (uid.equalsIgnoreCase(AUTHORIZED_UID_ISRAEL)) {
      isValid = true;
      studentName = "Israel";
    } else if (uid.equalsIgnoreCase(AUTHORIZED_UID_PEDRO)) {
      isValid = true;
      studentName = "Pedro";
    }
  }


  if (isValid) {
    // Green ON, Red OFF for 10 seconds
    digitalWrite(LED_GREEN, HIGH);
    digitalWrite(LED_RED, LOW);
    Serial.print("Nome do aluno: ");
    Serial.print(studentName);
    Serial.println(": Acesso Liberado!");


    tocarSomLiberado();   // som de acesso liberado


    // Keep active state for 10 seconds keeping MQTT alive
    unsigned long startMillis = millis();
    while (millis() - startMillis < 1000) {
      client.loop();
      delay(50);
    }
  } else {
    // Red blinks for 10 seconds, Green OFF, buzzer bipa em sincronia
    digitalWrite(LED_GREEN, LOW);
    Serial.println("Nome do aluno: Acesso Negado!");


    unsigned long startMillis = millis();
    unsigned long lastToggle = 0;
    bool redState = false;
    while (millis() - startMillis < 1500) {
      if (millis() - lastToggle >= 250) {
        redState = !redState;
        digitalWrite(LED_RED, redState ? HIGH : LOW);
        if (redState) {
          tone(BUZZER_PIN, 300, 200); // bipe sincronizado com o LED
        }
        lastToggle = millis();
      }
      client.loop();
      delay(10);
    }
    noTone(BUZZER_PIN);
  }


  // Return to normal (Red ON, Green OFF)
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_RED, HIGH);
  Serial.println("System closed.");


  rfid.PICC_HaltA();
}

