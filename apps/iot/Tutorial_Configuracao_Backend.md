# 📦 Tutorial de Configuração do Backend (Django)

## Objetivo
Configurar o backend Django para receber os UIDs das tags RFID enviadas pelo ESP32 via MQTT e expor a API REST.

## Passo a passo
1. **Criar/ativar o ambiente virtual**
   ```cmd
   cd C:\Users\gu268\Projetos\Django-projetos\SIGE
   python -m venv venv
   venv\Scripts\activate
   ```
2. **Instalar dependências**
   ```cmd
   pip install -r requirements.txt
   pip install paho-mqtt  # cliente MQTT usado pelo consumer
   ```
3. **Aplicar migrações do módulo IoT**
   ```cmd
   python manage.py makemigrations iot
   python manage.py migrate iot
   ```
4. **Verificar rotas**
   - `config/urls.py` já inclui `path("api/v1/iot/", include("apps.iot.urls"))`.
   - O endpoint ficará em `http://<HOST>:8000/api/v1/iot/rfid/` (ex.: `http://192.168.18.90:8000/api/v1/iot/rfid/`).
5. **Iniciar o servidor Django**
   ```cmd
   python manage.py runserver 0.0.0.0:8000
   ```
6. **Executar o consumidor MQTT** (opcionalmente como comando management)
   - **Via comando management** (recomendado):
     ```cmd
     python manage.py runmqtt
     ```
   - **Manual**:
     ```cmd
     python apps/iot/mqtt_consumer.py
     ```
7. **Testar a API** (obtenha um JWT via login mobile ou `/api/v1/auth/login/`)
   ```cmd
   curl -X GET http://192.168.18.90:8000/api/v1/iot/rfid/ \
        -H "Authorization: Bearer <SEU_TOKEN>"
   ```
   Deve retornar `[]` antes da primeira leitura.

## Checklist
- [ ] Virtual‑env ativo e dependências instaladas.
- [ ] Migrações aplicadas.
- [ ] Broker MQTT em execução.
- [ ] Consumidor MQTT rodando.
- [ ] Endpoint `/api/v1/iot/rfid/` responde.
