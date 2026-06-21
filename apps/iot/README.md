# 📡 IoT – RFID Integration Guide

> **Objetivo**: Configurar rapidamente o módulo IoT do SIGE para leitura de tags RFID (UID) via ESP32 e expor uma API REST que permita cadastrar, listar e validar tags usando o backend Django.

---

## 📦 Estrutura de pastas
```
SIGE/
└── apps/
    └── iot/
        ├── __init__.py          # Inicializa o app Django
        ├── models.py            # Modelo RFIDTag
        ├── serializers.py       # Serializador para a API
        ├── views.py             # ViewSet (list, create, retrieve, delete)
        ├── urls.py              # Roteamento -> /api/v1/iot/rfid/
        └── README.md            # <‑‑ ESTE ARQUIVO
```

---

## 1️⃣ Preparar o backend Django

1. **Ativar o virtual‑env**
```cmd
cd C:\Users\gu268\Projetos\Django-projetos\SIGE
venv\Scripts\activate
```
2. **Aplicar migrações do módulo IoT**
```cmd
python manage.py makemigrations iot
python manage.py migrate iot
```
3. **Verificar se o endpoint está ativo** (substitua `<TOKEN>` pelo JWT obtido no login do mobile ou via `/api/v1/auth/login/`)
```cmd
curl -X GET http://192.168.18.90:8000/api/v1/iot/rfid/ \
     -H "Authorization: Bearer <TOKEN>"
```
   - Deve retornar `[]` (lista vazia) se ainda não houver tags.

---

## 2️⃣ Configurar o ESP32 (hardware RFID)

> **Requisitos de hardware**
- **ESP32 DevKit**
- **Módulo RC522** (leitor RFID 13.56 MHz)
- Cabos jumper

### 2.1 Conexão física
| ESP32 Pin | RC522 Pin | Função |
|----------|-----------|--------|
| 3.3V     | VCC       | Alimentação |
| GND      | GND       | Terra |
| GPIO5 (SCK) | SCK   | Clock |
| GPIO18 (MOSI) | MOSI | Data out |
| GPIO23 (MISO) | MISO | Data in |
| GPIO21 (SS)   | SDA  | Chip select |
| GPIO22 (RST)  | RST  | Reset |

### 2.2 Código de exemplo (Arduino IDE / PlatformIO)
```cpp
#include <SPI.h>
#include "MFRC522.h"
#include <WiFi.h>
#include <PubSubClient.h>

// ---------- Wi‑Fi ----------
const char* ssid     = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

// ---------- MQTT ----------
const char* mqtt_server = "192.168.18.90"; // IP da máquina que roda o broker
const int   mqtt_port   = 1883;
const char* mqtt_user   = "mqtt_user";   // opcional
const char* mqtt_pass   = "mqtt_pass";   // opcional

WiFiClient espClient;
PubSubClient client(espClient);

// ---------- RFID ----------
#define RST_PIN  22
#define SS_PIN   21
MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(115200);
  SPI.begin();
  mfrc522.PCD_Init();

  // Wi‑Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");

  // MQTT
  client.setServer(mqtt_server, mqtt_port);
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32_RFID")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

void loop() {
  // Look for new cards
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial())
    return;

  // Build UID string (hex)
  String uid = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    if (mfrc522.uid.uidByte[i] < 0x10) uid += "0";
    uid += String(mfrc522.uid.uidByte[i], HEX);
  }
  uid.toUpperCase();
  Serial.print("Tag UID: ");
  Serial.println(uid);

  // Publish to MQTT
  String topic = "sige/iot/rfid"; // same as broker subscription
  client.publish(topic.c_str(), uid.c_str());

  // Delay to avoid flood
  delay(1500);
}
```
> **Dica**: ajuste `mqtt_server` para o IP do seu broker (pode ser o próprio Django se usar `django-mqtt` ou um broker externo como Mosquitto).

---

## 3️⃣ Consumidor MQTT no Django (Celery ou script simples)

Crie um **consumer** que escuta o tópico `sige/iot/rfid` e salva/atualiza o registro `RFIDTag`.

### 3.1 Instalar dependências
```cmd
pip install paho-mqtt celery redis
```
### 3.2 Arquivo `apps/iot/mqtt_consumer.py`
```python
import os
import django
import json
import paho.mqtt.client as mqtt

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from .models import RFIDTag
from django.contrib.auth import get_user_model
User = get_user_model()

BROKER_HOST = "192.168.18.90"
BROKER_PORT = 1883
TOPIC = "sige/iot/rfid"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    uid = msg.payload.decode().strip()
    print(f"Received UID: {uid}")
    # Exemplo simples: associa a um usuário pré‑definido (ID = 194)
    user = User.objects.get(id=194)  # ajuste conforme necessidade
    RFIDTag.objects.update_or_create(uid=uid, defaults={"user": user})
    print("Tag saved/updated")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_HOST, BROKER_PORT, 60)
client.loop_forever()
```
> **Execução** (em background):
```cmd
python apps/iot/mqtt_consumer.py
```
> Para produção, rode‑o via **Celery worker** ou como serviço systemd.

---

## 4️⃣ Testar a integração completa
1. **Inicie o broker MQTT** (Mosquitto recomendado).  
   ```cmd
   sudo apt install mosquitto   # Linux
   # ou baixe o instalador para Windows
   ```
2. **Rode o consumidor Django** (passo 3.2).  
3. **Carregue o firmware no ESP32** e aproxime uma tag RFID.
4. **Verifique no backend**:
   ```cmd
   curl -X GET http://192.168.18.90:8000/api/v1/iot/rfid/ \
        -H "Authorization: Bearer <TOKEN>"
   ```
   - Você deverá ver a tag recém‑lida associada ao usuário.
5. **Teste via Mobile** (app React Native já configurado para chamar `/api/v1/iot/rfid/` se desejar).

---

## 🛠️ Ferramentas úteis
- **MQTT Explorer** – UI para inspecionar mensagens no broker.
- **Postman** – para testar os endpoints da API.
- **Arduino IDE / VS Code + PlatformIO** – para compilar e fazer upload no ESP32.

---

## 🏫 Usando o IoT em Redes Institucionais (ex.: IFRN)

Redes de institutos federais e universidades possuem **firewall que bloqueia o tráfego direto entre dispositivos** (ex.: ESP32 → PC na mesma rede). Se você estiver no IFRN ou em rede similar, siga uma das estratégias abaixo:

### ✅ Solução 1 — Broker MQTT Público (testes rápidos)

A forma mais simples: use um broker público acessível pela internet. O ESP32 e o Django Consumer apontam para o mesmo endereço externo, sem depender de comunicação local.

No código do ESP32 (string `mqtt_server`):
```cpp
const char* mqtt_server = "broker.hivemq.com"; // ou broker.emqx.io
const int   mqtt_port   = 1883;
```

No `apps/iot/mqtt_consumer.py`:
```python
BROKER_HOST = "broker.hivemq.com"
BROKER_PORT = 1883
TOPIC = "sige/iot/rfid/SEU_TOPICO_UNICO"
```

| Broker | Endereço | Porta |
|---|---|---|
| HiveMQ | `broker.hivemq.com` | `1883` |
| EMQX | `broker.emqx.io` | `1883` |
| Mosquitto (test) | `test.mosquitto.org` | `1883` |

> ⚠️ **Nunca publique dados de produção em brokers públicos.** Use tópicos com nomes únicos (ex.: `sige/iot/rfid/ifrn-natal-2026`) para evitar colisão com outros usuários.

---

### ✅ Solução 2 — Hotspot do Celular (rede isolada)

Conecte o ESP32 e o seu PC na mesma rede de hotspot do celular. Isso elimina o firewall institucional.

1. Ative o **Hotspot** no celular.
2. Conecte o PC ao hotspot.
3. Descubra o IP do PC nessa rede:
   ```powershell
   ipconfig
   # Ex.: 192.168.43.100  (interface "Wi-Fi" ou "Adaptador Ethernet sem Fio")
   ```
4. No firmware do ESP32, altere:
   ```cpp
   const char* ssid        = "Nome_do_Hotspot";
   const char* password    = "Senha_do_Hotspot";
   const char* mqtt_server = "192.168.43.100";  // IP do PC no hotspot
   ```
5. Inicie o Mosquitto no PC:
   ```powershell
   mosquitto -v
   ```
> **Dica:** O IP do PC no hotspot pode variar a cada reconexão. Se o ESP32 não alcançar o broker, repita o passo 3 e recompile o firmware.

---

### ✅ Solução 3 — Liberação de Porta pelo TI (produção)

Para uso permanente nas instalações do IFRN, solicite à **Coordenação de TI** a liberação da **porta `1883` (TCP)** para o IP fixo da máquina que rodará o broker Mosquitto. Isso habilita a comunicação direta ESP32 → broker sem dependência de internet ou hotspot.

---


- [ ] Virtual‑env ativo e dependências instaladas (`pip install -r requirements.txt`).
- [ ] Migrações IoT aplicadas.
- [ ] Broker MQTT rodando e acessível.
- [ ] Consumidor Django em execução.
- [ ] Firmware ESP32 carregado e conectado ao Wi‑Fi.
- [ ] Endpoint `/api/v1/iot/rfid/` responde corretamente.

---

**⚡️ Pronto!** Seu módulo IoT está pronto para receber tags RFID, registrar a presença dos alunos e alimentar o restante do ecossistema SIGE (dashboard, relatórios, notificações, etc.).
