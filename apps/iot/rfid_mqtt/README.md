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

## 🏫 Configuração em Redes Institucionais (ex.: IFRN)

Redes universitárias e de institutos federais (como a do **IFRN**) possuem restrições que diferem de uma rede doméstica. Siga os passos abaixo para adaptar o projeto:

### Problema comum
Nessas redes, o tráfego **peer-to-peer entre dispositivos** (ESP32 → PC) costuma ser **bloqueado por padrão**. Isso impede que o ESP32 alcance o broker MQTT rodando na sua máquina diretamente pelo IP local.

### ✅ Solução 1 — Broker MQTT Público (recomendado para testes rápidos)
Use um broker público gratuito que seja acessível pela internet. O ESP32 usa a internet da rede institucional para se conectar, **sem depender da comunicação direta com o seu PC**.

Edite o `src/config.h`:
```cpp
const char* MQTT_BROKER = "broker.hivemq.com"; // broker público gratuito
const uint16_t MQTT_PORT = 1883;
const char* MQTT_TOPIC   = "sige/iot/rfid/SEU_NOME"; // use um tópico único!
```
> **⚠️ Atenção:** Brokers públicos são compartilhados. Nunca publique dados sensíveis neles. Use-os apenas para desenvolvimento e testes.

Opções de brokers públicos gratuitos:
| Broker | Endereço | Porta |
|---|---|---|
| HiveMQ | `broker.hivemq.com` | `1883` |
| EMQX | `broker.emqx.io` | `1883` |
| Mosquitto (test) | `test.mosquitto.org` | `1883` |

O consumidor Django também precisa apontar para o mesmo broker. Em `apps/iot/mqtt_consumer.py`:
```python
BROKER_HOST = "broker.hivemq.com"
BROKER_PORT = 1883
TOPIC = "sige/iot/rfid/SEU_NOME"  # deve ser idêntico ao do ESP32
```

---

### ✅ Solução 2 — Hotspot do Celular (rede isolada e controlada)
Crie um **hotspot Wi-Fi** no seu celular e conecte tanto o ESP32 quanto o seu PC nessa rede. Assim, a comunicação é direta, sem firewall institucional.

1. Ative o hotspot no celular.
2. Conecte o seu PC ao hotspot.
3. Descubra o IP do seu PC nessa rede:
   ```powershell
   ipconfig
   # Procure pela interface "Adaptador de Rede sem Fio Wi-Fi" → Endereço IPv4
   # Exemplo: 192.168.43.100
   ```
4. Edite o `src/config.h` do ESP32:
   ```cpp
   const char* WIFI_SSID     = "Nome_do_Hotspot";
   const char* WIFI_PASSWORD = "Senha_do_Hotspot";
   const char* MQTT_BROKER   = "192.168.43.100"; // IP do PC no hotspot
   const uint16_t MQTT_PORT  = 1883;
   ```
5. Inicie o broker Mosquitto no seu PC:
   ```powershell
   mosquitto -v
   ```
> **Dica:** O IP do PC no hotspot pode mudar a cada conexão. Se o ESP32 não conectar, repita o passo 3 e atualize o `config.h`.

---

### ✅ Solução 3 — Solicitar Liberação de Porta ao TI (produção)
Para implantação definitiva no IFRN, solicite à equipe de TI a **liberação da porta `1883`** (MQTT) e do IP fixo da máquina que rodará o broker. Essa é a solução mais robusta para ambiente de produção.

---

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
