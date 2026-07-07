# 🚀 Guia de Demonstração — SIGE + Mobile + IoT

> **Integração completa:** Leitor RFID (ESP32) → Backend Django → App Mobile React Native

---

## 👥 Alunos Cadastrados no IoT

| Aluno | Matrícula | Tag RFID | Senha (Mobile) |
|---|---|---|---|
| Israel Cipriano Ribeiro Filho | `20260170199` | `E2:00:80:05` | `SenhaSIGE2026` |
| Pedro Henrique de Oliveira Querino | `20260170200` | `D1:DF:A3:A4` | `SenhaSIGE2026` |

**Turma:** Projeto Integrador — Manhã (2026)  
**Disciplina:** Projeto Integrador

---

## ⚙️ Pré-requisitos

- Python 3.11+ com `venv` ativado
- Node.js 18+ e npm instalados
- App **Expo Go** no celular (Android ou iOS)
- ESP32 com firmware RFID carregado e conectado via USB
- PlatformIO instalado (para compilar/monitorar o ESP32)
- Todos os dispositivos na **mesma rede Wi-Fi**

---

## 📋 Passo a Passo

### 🟢 Terminal 1 — Servidor Django (Backend)

```powershell
cd C:\Users\gu268\Projetos\Django-projetos\SIGE

# Ativar o ambiente virtual
..\venv\Scripts\activate

# Iniciar o servidor (acessível na rede local)
python manage.py runserver 0.0.0.0:8000
```

> ✅ Confirmação: o terminal deve exibir  
> `Starting development server at http://0.0.0.0:8000/`

---

### 🟡 Terminal 2 — Consumidor MQTT (IoT → Backend)

> **Abra um segundo terminal PowerShell** e execute:

```powershell
cd C:\Users\gu268\Projetos\Django-projetos\SIGE

# Ativar o ambiente virtual
..\venv\Scripts\activate

# Iniciar o consumidor MQTT
python manage.py runmqtt
```

> ✅ Confirmação: o terminal deve exibir  
> `Conectado ao Broker MQTT com sucesso!`  
> `Inscrito no tópico: esp32/rfid`

---

### 🔵 Terminal 3 — App Mobile (React Native / Expo)

> **Abra um terceiro terminal PowerShell** e execute:

```powershell
cd C:\Users\gu268\Projetos\Django-projetos\SIGE_APP\SIGE_Mobile

# Iniciar o Expo
npx expo start --clear
```

> ✅ Um **QR Code** será exibido no terminal.  
> Abra o app **Expo Go** no celular e escaneie o código.

**Login no app:**

| Campo | Valor |
|---|---|
| Matrícula | `20260170199` (Israel) ou `20260170200` (Pedro) |
| Senha | `SenhaSIGE2026` |

---

### ⚡ Terminal 4 — Monitor Serial do ESP32 (IoT)

> **Abra um quarto terminal PowerShell** e execute:

```powershell
cd C:\Users\gu268\Projetos\Django-projetos\SIGE\apps\iot\rfid_mqtt

# Monitorar a comunicação serial do ESP32
# (ajuste COM3 para a porta correta do seu ESP32)
pio device monitor -p COM3 -b 115200
```

> Para descobrir a porta COM correta:
> ```powershell
> # No Gerenciador de Dispositivos do Windows, ou:
> Get-PnpDevice -Class Ports | Select-String "CP210"
> ```

---

## 🔄 Fluxo de Demonstração

```
1. [App Mobile]
   └─ Faça login com a matrícula de Israel ou Pedro

2. [ESP32 + Cartão RFID]
   └─ Aproxime o cartão do leitor
   └─ LEDs piscam enquanto aguarda validação (até 2s)

3. [Terminal 2 — runmqtt]
   └─ Mostra: "PRESENÇA REGISTRADA: <Nome> na disciplina Projeto Integrador"

4. [ESP32]
   └─ LED Verde acende + som de acesso liberado ✅
   └─ (Se offline/timeout → valida localmente e abre igualmente)

5. [App Mobile → Aba "Frequência"]
   └─ Recarregue a tela para ver a nova presença registrada
   └─ Uma notificação é gerada automaticamente
```

---

## 🛠️ Comandos Úteis Adicionais

### Re-gravar o firmware no ESP32
```powershell
cd C:\Users\gu268\Projetos\Django-projetos\SIGE\apps\iot\rfid_mqtt

# Compilar e enviar para o ESP32
pio run -t upload --upload-port COM3
```

### Listar todas as Tags RFID cadastradas no banco
```powershell
cd C:\Users\gu268\Projetos\Django-projetos\SIGE
..\venv\Scripts\activate
python manage.py listrfid
```

### Verificar o banco de dados manualmente
```powershell
cd C:\Users\gu268\Projetos\Django-projetos\SIGE
..\venv\Scripts\activate
python manage.py shell

# No shell Django:
# from apps.iot.models import RFIDTag
# RFIDTag.objects.all().values('uid', 'user__first_name', 'user__last_name')
```

---

## 🌐 URLs do Backend

| Endpoint | Descrição |
|---|---|
| `http://192.168.18.90:8000/api/ping/` | Verificar se o backend está online |
| `http://192.168.18.90:8000/api/v1/auth/login/` | Login (POST) |
| `http://192.168.18.90:8000/api/v1/aluno/dashboard/` | Dashboard do aluno |
| `http://192.168.18.90:8000/api/v1/aluno/boletim/` | Frequência e notas |
| `http://192.168.18.90:8000/admin/` | Painel administrativo |

> 💡 Substitua `192.168.18.90` pelo IP da sua máquina na rede local.  
> Para encontrar seu IP: `ipconfig` → procure "Endereço IPv4"

---

## 🔧 Configurações do Firmware ESP32

**Arquivo:** `apps/iot/rfid_mqtt/src/config.h`

```cpp
// Wi-Fi
WIFI_SSID     = "Zeca"
WIFI_PASSWORD = "zecas1301"

// MQTT Broker (público)
MQTT_BROKER         = "broker.hivemq.com"
MQTT_TOPIC          = "esp32/rfid"          // ESP32 publica aqui
MQTT_TOPIC_RESPONSE = "esp32/rfid/response" // Backend responde aqui

// Fallback offline (se backend não responder em 2 segundos)
AUTHORIZED_UID_ISRAEL = "E2:00:80:05"
AUTHORIZED_UID_PEDRO  = "D1:DF:A3:A4"
```

---

## ❗ Solução de Problemas

| Problema | Solução |
|---|---|
| App mobile não conecta | Confirme que o celular está na mesma rede Wi-Fi que o PC. Verifique `API_BASE_URL` em `src/services/api.js` |
| `runmqtt` não recebe mensagens | Verifique se o ESP32 está conectado ao Wi-Fi e ao broker `broker.hivemq.com` via monitor serial |
| ESP32 não abre a porta | Confirme o tópico MQTT no `config.h` (`esp32/rfid`) é o mesmo no `runmqtt.py` |
| Presença não aparece no app | Deslogue e logue novamente ou puxe para baixo para recarregar a tela de Frequência |
| Login falha no app | Execute `python manage.py runserver 0.0.0.0:8000` (não apenas `runserver`) |
