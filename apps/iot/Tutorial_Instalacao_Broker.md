# 📡 Tutorial de Instalação do Broker MQTT (Mosquitto)

## Objetivo
Instalar e configurar um broker MQTT local que receberá os **UIDs** das tags RFID enviadas pelo ESP32.

## Requisitos
- Windows 10/11 ou Linux (o tutorial abaixo foca em Windows).
- Permissão de administrador para instalar serviços.
- Rede com IP estático (aqui usamos `192.168.18.90`).

## Passo a passo
1. **Download** – acesse https://mosquitto.org/download/ e baixe *mosquitto‑2.0.15‑install‑windows‑x64.exe* (ou versão mais recente).
2. **Instalação** – execute como **Administrador** e marque **“Install as Service”**.
3. **Configuração** – abra `C:\Program Files\mosquitto\mosquitto.conf` e adicione:
   ```conf
   listener 1883
   allow_anonymous true   # para teste rápido; em produção use autenticação
   ```
4. **Inicie o serviço**
   ```powershell
   net start mosquitto
   ```
   Verifique: `sc query mosquitto`.
5. **Teste a conexão**
   - Baixe **MQTT Explorer** (https://mqtt-explorer.com/).
   - Crie conexão para `192.168.18.90:1883`.
   - Publique no tópico `test/topic` com payload `hello`.
   - Se aparecer, o broker está funcionando.

## Próximos passos
- Deixe o broker rodando enquanto o ESP32 envia UIDs.
- Para segurança, configure `password_file` e `allow_anonymous false`.

> **⚙️ Dica**: abra a porta 1883 no firewall se necessário.
