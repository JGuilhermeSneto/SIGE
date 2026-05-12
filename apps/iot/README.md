# 🔌 App: IoT (Internet das Coisas)

Módulo de integração com hardware para automação de rotinas escolares.

## Responsabilidades
- Recebimento de dados de sensores via MQTT/API
- Registro automático de frequência via RFID (ESP32 + RC522)
- Controle de acesso por QR Code (carteirinha digital)
- Monitoramento de ocupação de salas (sensores PIR)

## Status
> 🚧 **Em desenvolvimento** — Projeto Integrador II

## Tecnologias Planejadas
- `ESP32` como microcontrolador
- `Protocolo MQTT` para comunicação em tempo real
- `paho-mqtt` (Python) como cliente MQTT
- Sincronização automática com `apps.academico`

## Arquitetura de Comunicação
```
ESP32 (RFID) → MQTT Broker → SIGE API → apps.academico.Frequencia
```
