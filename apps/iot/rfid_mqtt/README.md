# RFID + MQTT ESP32 Example

> **Quick start** – clone this repo, edit the Wi‑Fi/MQTT credentials in `src/config.h`, run `pio run -t upload`, and watch the serial monitor.

## 📋 Overview
This project demonstrates how to read an RFID tag with an **MFRC522** module on an **ESP32‑dev** board, publish the tag UID to an MQTT broker, and give visual feedback with two LEDs (green = access granted, red = access denied/closed).

## 📦 Structure
```
rfid_mqtt/
│   platformio.ini          # PlatformIO configuration (dependencies, board, etc.)
│   README.md               # ← this file
│   WIRING.md               # wiring diagram and pinout
└─ src/
    │   config.h            # Wi‑Fi/MQTT constants (edit before building)
    │   main.cpp            # Arduino sketch – all logic lives here
```

## 🔌 Wiring (see **WIRING.md** for a diagram)
| ESP32 Pin | Function | Connection |
|-----------|----------|------------|
| **5**     | SS (SDA) | MFRC522 **SDA** |
| **22**    | RST      | MFRC522 **RST** |
| **18**    | SCK      | MFRC522 **SCK** |
| **23**    | MOSI     | MFRC522 **MOSI** |
| **19**    | MISO     | MFRC522 **MISO** |
| **3V3**   | 3.3 V    | MFRC522 **3.3V** (do **not** use 5 V) |
| **GND**   | Ground   | MFRC522 **GND** |
| **2**     | LED‑GREEN| LED anode (through ~220 Ω) → GND |
| **4**     | LED‑RED  | LED anode (through ~220 Ω) → GND |
| **GND**   | Ground   | LEDs cathode → GND |

> **Tip:** Use resistor values between 150‑330 Ω to limit current for the LEDs.

## ⚙️ Configuration (`src/config.h`)
Edit the placeholder values:
```cpp
const char* WIFI_SSID     = "YOUR_SSID";      // Wi‑Fi network name
const char* WIFI_PASSWORD = "YOUR_PASSWORD"; // Wi‑Fi password
const char* MQTT_BROKER   = "broker.hivemq.com"; // MQTT broker address
const uint16_t MQTT_PORT = 1883;               // MQTT broker port (default 1883)
const char* MQTT_TOPIC   = "esp32/rfid";      // Topic where UIDs are published
```
You can also point to a private broker (e.g., Mosquitto, EMQX) – just change the address/port.

## 🛠️ Build & Upload
```powershell
# 1️⃣ Navigate to the project folder
cd C:\Users\gu268\Projetos\Django-projetos\SIGE\apps\iot\rfid_mqtt

# 2️⃣ Install / update PlatformIO dependencies (runs automatically on first build)
pio run          # compile only (checks for errors)

# 3️⃣ Upload to the ESP32 (replace COMx with your actual serial port)
pio run -t upload --upload-port COM3

# 4️⃣ Open the serial monitor to see logs
pio device monitor -p COM3 -b 115200
```
If you use VS Code with the PlatformIO extension, the same tasks are available through the *PlatformIO* sidebar.

## 🚀 Expected Runtime Behaviour
1. On power‑up the board connects to Wi‑Fi → MQTT broker.
2. The red LED is ON (system closed).
3. When an RFID tag is presented:
   - UID is printed on the serial monitor.
   - UID is published to the MQTT topic.
   - Green LED turns on for **5 seconds**, then the system closes again (red LED on).
4. The loop repeats indefinitely.

## 📁 Updating the Repository
Any change to the source files should be committed with a meaningful message, e.g.:
```bash
git add src/* README.md WIRING.md
git commit -m "Add wiring diagram and usage documentation"
git push
```
(If you are not using Git, simply keep the files in the `rfid_mqtt` folder.)

## 📜 License
This example code is released under the **MIT License** – feel free to adapt, share, and integrate it into your own projects.

---
*Created by Antigravity – your AI coding assistant.*
