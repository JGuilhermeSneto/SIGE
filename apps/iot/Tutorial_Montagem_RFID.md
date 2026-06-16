# 🛠️ Tutorial Montagem RFID (ESP32 + RC522)

## 📋 Componentes necessários
- ESP32 DevKit (ou placa ESP32 compatível)
- Módulo RFID **RC522** (13.56 MHz)
- Cabos jumper male‑male
- Fonte de alimentação 5 V (o ESP já recebe via USB)
- Opcional: protoboard para organizar as conexões

## 📍 Conexão física (pin‑out)
| ESP32 Pin | RC522 Pin | Função |
|-----------|-----------|--------|
| 3.3V      | VCC       | Alimentação (3.3 V) |
| GND       | GND       | Terra |
| GPIO5 (SCK) | SCK    | Clock SPI |
| GPIO18 (MOSI) | MOSI | Data Out (Master‑Out) |
| GPIO23 (MISO) | MISO | Data In (Master‑In) |
| GPIO21 (SS)   | SDA   | Chip Select / Slave Select |
| GPIO22 (RST)  | RST   | Reset do RC522 |

> **Dica:** O ESP32 opera a 3.3 V, portanto não é necessário regulador de tensão para o RC522.

## 🔧 Passos de montagem
1. **Posicione o módulo RC522** na protoboard.
2. **Conecte os fios** de acordo com a tabela acima.
3. **Alimente o ESP32** via cabo micro‑USB ao seu computador.
4. **Verifique as ligações** antes de prosseguir – um curto pode danificar a placa.
5. **Instale a biblioteca** `MFRC522` no Arduino IDE (ou PlatformIO) para facilitar a comunicação SPI.

## ✅ Verificação rápida
- Abra o Serial Monitor (115200 baud) e carregue o exemplo “**ReadUID**” da biblioteca MFRC522.
- Aproxima uma tag RFID – o UID deve aparecer no console.
- Se aparecer, a conexão está correta e você pode avançar para a próxima fase (upload do código que envia dados via MQTT).

---
### 📦 Arquivos relacionados
- Código exemplo do firmware está em **[Tutorial_Montagem_RFID.md](./Tutorial_Montagem_RFID.md)** – seção *Código de exemplo*.
- Para instalar o broker MQTT, veja **[Tutorial_Instalacao_Broker.md](./Tutorial_Instalacao_Broker.md)**.
- Para configurar o backend Django, veja **[Tutorial_Configuracao_Backend.md](./Tutorial_Configuracao_Backend.md)**.
