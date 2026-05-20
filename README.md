# 🛡️ SIGE — Sistema Integrado de Gestão Escolar

## 🚀 v8.0 Apex — Núcleo de Processamento de Alta Disponibilidade e Segurança Estrutural

> **Backend robusto e escalável** para suporte às frentes **Web**, **Mobile**, **IoT** e **Governança**. Infraestrutura moderna com observabilidade em tempo real, segurança de nível enterprise e conformidade LGPD.

<br/>

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0.4-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.17.1-A30000?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7.0-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)

![Celery](https://img.shields.io/badge/Celery-5.6.3-37B24D?style=for-the-badge&logo=celery&logoColor=white)
![Channels](https://img.shields.io/badge/Channels-4.2.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-2.3.1-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-Latest-F2776D?style=for-the-badge&logo=grafana&logoColor=white)

![Pytest](https://img.shields.io/badge/Pytest-Coverage%2068%25-4B8BBE?style=for-the-badge&logo=pytest&logoColor=white)
![Tests](https://img.shields.io/badge/Testes-128%2F149%20Passing-4CAF50?style=for-the-badge&logo=codecov&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production%20Ready-green?style=for-the-badge)

</div>

---

## 📋 Índice de Conteúdo

- [🎯 Visão Geral](#-visão-geral)
- [🏗️ Arquitetura v8.0 Apex](#-arquitetura-v80-apex)
- [💻 Stack Tecnológico Completo](#-stack-tecnológico-completo)
- [📦 Dependências Python (Categorizado)](#-dependências-python-categorizado)
- [🐳 DevOps & Infraestrutura](#-devops--infraestrutura)
- [🗄️ Banco de Dados](#-banco-de-dados)
- [🧩 Módulos & Aplicações](#-módulos--aplicações)
- [📊 Status de Testes](#-status-de-testes)
- [🚀 Quick Start](#-quick-start)
- [📚 Documentação Completa](#-documentação-completa)

---

## 🎯 Visão Geral

O **SIGE** é uma plataforma integrada de gestão escolar desenvolvida em **Django 6.0** com arquitetura modular (monolito escalável). Fornece uma solução completa para administração escolar, incluindo:

✅ **Gestão Acadêmica** — Turmas, Atividades, Frequência, Histórico  
✅ **Gerenciamento de Usuários** — RBAC, 2FA, Autenticação por Matrícula  
✅ **Segurança Enterprise** — SOC, Auditoria LGPD, Proteção contra Ataques  
✅ **Observabilidade** — Mission Control, Telemetria em Tempo Real  
✅ **Backup & Recuperação** — Quantum Snapshots com Redundância Geográfica  
✅ **Processamento Assíncrono** — Celery + RabbitMQ para Tarefas Background  
✅ **Comunicação em Tempo Real** — WebSockets via Django Channels  
✅ **Monitoramento Avançado** — Prometheus + Grafana + Health Checks  

---

## 🏗️ Arquitetura v8.0 Apex

O SIGE v8.0 consolida uma infraestrutura **modular de alta disponibilidade** focada em observabilidade, governança e localização total (PT-BR).

### 🎖️ Destaques Principais:

| Feature | Descrição |
| :--- | :--- |
| **🎛️ Mission Control God-Tier** | Painel TI localizado com telemetria avançada, monitoramento de recursos em tempo real e orquestração CI/CD |
| **📸 Quantum Snapshots** | Backup de alta fidelidade com radar de integridade, replicação geográfica e defesa anti-ransomware |
| **🛡️ Security Operations Center (SOC)** | Camada de defesa ativa em tempo real (WebSockets + AJAX) com filtragem de IPs, auditoria de eventos e Trust Score |
| **🔐 IAM & Vault** | Gestão de identidades com MFA mandatório (flag configurável) e cofre de segredos criptografado |
| **🌍 Localização Total** | 100% em Português (Brasil) — Acessibilidade e conformidade operacional |
| **✅ QA Integrado** | 149 casos de teste cobrindo 68% do código-fonte (7.732 statements rastreados) |
| **⚡ Real-Time SOC & Notifications** | WebSockets e chamadas assíncronas para controle em tempo real do SOC (logins, blacklist) e alertas de segurança |
| **📡 Observabilidade 360°** | Prometheus, Grafana, Health Checks, Django Prometheus, Sentry |

---

## 💻 Stack Tecnológico Completo

### 🔵 **Backend Framework**

| 🐍 | Tecnologia | Versão | Propósito |
| :---: | :--- | :---: | :--- |
| 🐍 | ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) | 3.12+ | Linguagem principal |
| 🎯 | ![Django](https://img.shields.io/badge/-Django-092E20?logo=django&logoColor=white) | 6.0.4 | Framework web |
| 📡 | ![Django REST Framework](https://img.shields.io/badge/-DRF-A30000?logo=django&logoColor=white) | 3.17.1 | API REST |
| ⚡ | ![Daphne](https://img.shields.io/badge/-Daphne-092E20?logo=django&logoColor=white) | 4.1.0 | ASGI Server (WebSockets) |
| 🚀 | ![Gunicorn](https://img.shields.io/badge/-Gunicorn-499848?logo=gunicorn&logoColor=white) | 23.0.0 | WSGI HTTP Server |

### 🗄️ **Databases & Cache**

| 🖥️ | Tecnologia | Versão | Propósito |
| :---: | :--- | :---: | :--- |
| 🗄️ | ![MySQL](https://img.shields.io/badge/-MySQL-4479A1?logo=mysql&logoColor=white) | 8.0 | Banco de dados principal |
| 💾 | ![Redis](https://img.shields.io/badge/-Redis-DC382D?logo=redis&logoColor=white) | 7-alpine | Cache + Session Store + Message Queue |
| 🐰 | ![RabbitMQ](https://img.shields.io/badge/-RabbitMQ-FF6B6B?logo=rabbitmq&logoColor=white) | 3-alpine | Broker de mensagens (Celery) |

### 📦 **Processamento Assíncrono & Real-Time**

| ⏰ | Tecnologia | Versão | Propósito |
| :---: | :--- | :---: | :--- |
| 🐝 | ![Celery](https://img.shields.io/badge/-Celery-37B24D?logo=celery&logoColor=white) | 5.6.3 | Task Queue distribuída |
| 🌸 | ![Flower](https://img.shields.io/badge/-Flower-2.0.1-4CAF50?logo=flower&logoColor=white) | 2.0.1 | Monitoramento Celery |
| 📡 | ![Channels](https://img.shields.io/badge/-Django%20Channels-092E20?logo=django&logoColor=white) | 4.2.0 | WebSockets & Async |
| 🔴 | ![Channels Redis](https://img.shields.io/badge/-Channels%20Redis-DC382D?logo=redis&logoColor=white) | 4.2.0 | Backend para Channels |

### 🔐 **Segurança & Autenticação**

| 🔒 | Tecnologia | Versão | Propósito |
| :---: | :--- | :---: | :--- |
| 🎫 | ![JWT](https://img.shields.io/badge/-JWT-000000?logo=jsonwebtokens&logoColor=white) | 5.5.1 | Token-based Authentication |
| 🛡️ | ![Django Axes](https://img.shields.io/badge/-Axes-092E20?logo=django&logoColor=white) | 6.3.1 | Brute Force Protection & Login Monitoring |
| 🔑 | ![2FA](https://img.shields.io/badge/-Two%20Factor%20Auth-FF5733?logo=2fa&logoColor=white) | 1.17.0+ | MFA Support |
| 🚨 | ![Django CSP](https://img.shields.io/badge/-CSP-092E20?logo=django&logoColor=white) | 4.0 | Content Security Policy |
| 🔐 | ![Cryptography](https://img.shields.io/badge/-Cryptography-3776AB?logo=python&logoColor=white) | 46.0.7 | Criptografia avançada |
| ✍️ | ![PyHanko](https://img.shields.io/badge/-PyHanko-1F77B4?logo=python&logoColor=white) | 0.34.1 | Assinatura Digital PDF |
| ✅ | ![pyhanko-certvalidator](https://img.shields.io/badge/-certvalidator-0.30.2-1F77B4?logo=python&logoColor=white) | 0.30.2 | Validação de Certificados |

### 📊 **Observabilidade & Monitoramento**

| 📈 | Tecnologia | Versão | Propósito |
| :---: | :--- | :---: | :--- |
| ❤️ | ![Health Checks](https://img.shields.io/badge/-Health%20Check-092E20?logo=django&logoColor=white) | 3.18.1+ | Status de Serviços |
| 📊 | ![Prometheus](https://img.shields.io/badge/-Prometheus-E6522C?logo=prometheus&logoColor=white) | latest | Coleta de métricas |
| 📉 | ![Grafana](https://img.shields.io/badge/-Grafana-F2776D?logo=grafana&logoColor=white) | latest | Visualização de métricas |
| 📐 | ![Django Prometheus](https://img.shields.io/badge/-Django%20Prometheus-2.3.1-092E20?logo=django&logoColor=white) | 2.3.1 | Métricas Django |
| 🚨 | ![Sentry](https://img.shields.io/badge/-Sentry-362D59?logo=sentry&logoColor=white) | 2.22.0 | Error Tracking & APM |
| 🖥️ | ![psutil](https://img.shields.io/badge/-psutil-3776AB?logo=python&logoColor=white) | 5.9.8+ | Monitoramento de Recursos |

### 📄 **Processamento de Documentos**

| 📑 | Tecnologia | Versão | Propósito |
| :---: | :--- | :---: | :--- |
| 📋 | ![ReportLab](https://img.shields.io/badge/-ReportLab-4CAF50?logo=python&logoColor=white) | 4.5.0 | Geração PDF programática |
| 🔄 | ![xhtml2pdf](https://img.shields.io/badge/-xhtml2pdf-FF6B6B?logo=python&logoColor=white) | 0.2.17 | Conversão HTML → PDF |
| 📕 | ![PyPDF](https://img.shields.io/badge/-PyPDF-006DB6?logo=pdf&logoColor=white) | 6.10.2 | Manipulação de PDFs |
| 🎨 | ![svglib](https://img.shields.io/badge/-svglib-FF9900?logo=svg&logoColor=white) | 1.6.0 | SVG → PDF |
| 🌍 | ![python-bidi](https://img.shields.io/badge/-python--bidi-3776AB?logo=python&logoColor=white) | 0.5.6+ | Suporte RTL (Árabe, Hebraico) |
| 🖼️ | ![Pillow](https://img.shields.io/badge/-Pillow-FF6B6B?logo=python&logoColor=white) | 12.2.0 | Image processing |

### ☁️ **Cloud Storage & CDN**

| 🌐 | Tecnologia | Versão | Propósito |
| :---: | :--- | :---: | :--- |
| ☁️ | ![Cloudinary](https://img.shields.io/badge/-Cloudinary-3448C5?logo=cloudinary&logoColor=white) | 1.44.2 | Media storage na nuvem |
| 🖼️ | ![Django Cloudinary Storage](https://img.shields.io/badge/-Cloudinary%20Storage-0.3.0-3448C5?logo=cloudinary&logoColor=white) | 0.3.0 | Integração com Django |

### 🛡️ **Validação & Segurança de Senha**

| ✔️ | Tecnologia | Versão | Propósito |
| :---: | :--- | :---: | :--- |
| 🔐 | ![django-zxcvbn-password](https://img.shields.io/badge/-zxcvbn-FF5733?logo=python&logoColor=white) | 2.1.1+ | Verificação forte de senhas |
| 🇧🇷 | ![validate-docbr](https://img.shields.io/badge/-validate--docbr-4CAF50?logo=python&logoColor=white) | 2.0.0+ | Validação de CPF/CNPJ |

### 📋 **Auditoria & Histórico**

| 📜 | Tecnologia | Versão | Propósito |
| :---: | :--- | :---: | :--- |
| 📜 | ![django-simple-history](https://img.shields.io/badge/-Simple%20History-092E20?logo=django&logoColor=white) | 3.7.0+ | Rastreamento de mudanças |
| 👤 | ![django-impersonate](https://img.shields.io/badge/-Impersonate-092E20?logo=django&logoColor=white) | 1.9.3+ | Admin personification |

### 🔍 **Qualidade de Código & Testing**

| ✅ | Tecnologia | Versão | Propósito |
| :---: | :--- | :---: | :--- |
| 🧪 | ![Pytest](https://img.shields.io/badge/-Pytest-0A3F5C?logo=pytest&logoColor=white) | latest | Testing framework |
| 📊 | ![Coverage.py](https://img.shields.io/badge/-Coverage-4B8BBE?logo=python&logoColor=white) | 7.13.5 | Cobertura de testes |
| ⚫ | ![Black](https://img.shields.io/badge/-Black-000000?logo=python&logoColor=white) | 26.3.1 | Code formatter |
| 🔤 | ![isort](https://img.shields.io/badge/-isort-3776AB?logo=python&logoColor=white) | 8.0.1 | Import sorter |
| 🔍 | ![Flake8](https://img.shields.io/badge/-Flake8-4B8BBE?logo=python&logoColor=white) | 7.3.0 | Linter |
| 🔎 | ![Pylint](https://img.shields.io/badge/-Pylint-FF5733?logo=python&logoColor=white) | 4.0.5 | Code analyzer |
| 🎯 | ![MyPy](https://img.shields.io/badge/-MyPy-0C4B8C?logo=python&logoColor=white) | 1.20.1 | Type checker |
| 📝 | ![Pylint Django](https://img.shields.io/badge/-pylint--django-092E20?logo=django&logoColor=white) | 2.7.0 | Django support |
| 🔧 | ![Django Stubs](https://img.shields.io/badge/-django--stubs-092E20?logo=django&logoColor=white) | 6.0.3 | Type hints para Django |

### 🌐 **Utilitários & Serialização**

| 🛠️ | Tecnologia | Versão | Propósito |
| :---: | :--- | :---: | :--- |
| 📋 | ![PyYAML](https://img.shields.io/badge/-PyYAML-FF5733?logo=yaml&logoColor=white) | 6.0.3 | Configurações |
| 🔤 | ![python-dotenv](https://img.shields.io/badge/-python--dotenv-3776AB?logo=python&logoColor=white) | 1.2.2 | Variáveis de ambiente |
| ⚙️ | ![python-decouple](https://img.shields.io/badge/-python--decouple-3776AB?logo=python&logoColor=white) | 3.8 | Config management |
| 🌐 | ![requests](https://img.shields.io/badge/-requests-3776AB?logo=python&logoColor=white) | 2.33.1 | HTTP client |
| 📦 | ![lxml](https://img.shields.io/badge/-lxml-3776AB?logo=python&logoColor=white) | 6.1.0 | XML/HTML processing |
| 🎫 | ![PyJWT](https://img.shields.io/badge/-PyJWT-000000?logo=jsonwebtokens&logoColor=white) | 2.12.1 | JWT tokens |
| 📦 | ![packaging](https://img.shields.io/badge/-packaging-26.2-FFE200?logo=python&logoColor=white) | 26.2 | Package utilities |
| 🖱️ | ![click](https://img.shields.io/badge/-click-8.3.2-7F0000?logo=python&logoColor=white) | 8.3.2 | CLI framework |
| 🎨 | ![colorama](https://img.shields.io/badge/-colorama-0.4.6-FF5733?logo=python&logoColor=white) | 0.4.6 | Terminal colors |
| 🔒 | ![certifi](https://img.shields.io/badge/-certifi-2026.2.25-003478?logo=python&logoColor=white) | 2026.2.25 | SSL certificates |
| 🌍 | ![charset-normalizer](https://img.shields.io/badge/-charset--normalizer-3.4.7-FF6B9D?logo=python&logoColor=white) | 3.4.7 | Charset detection |
| 🆔 | ![idna](https://img.shields.io/badge/-idna-3.13-3776AB?logo=python&logoColor=white) | 3.13 | IDNA support |
| 🔗 | ![urllib3](https://img.shields.io/badge/-urllib3-2.6.3-006DB6?logo=python&logoColor=white) | 2.6.3 | HTTP client |
| ⏱️ | ![tzdata](https://img.shields.io/badge/-tzdata-2026.1-FF9500?logo=python&logoColor=white) | 2026.1 | Timezone data |
| ⏰ | ![tzlocal](https://img.shields.io/badge/-tzlocal-5.3.1-FF9500?logo=python&logoColor=white) | 5.3.1 | Local timezone |

### 🖥️ **Interface & UI**

| 🎨 | Tecnologia | Versão | Propósito |
| :---: | :--- | :---: | :--- |
| 🎛️ | ![Django Widget Tweaks](https://img.shields.io/badge/-Widget%20Tweaks-092E20?logo=django&logoColor=white) | 1.5.1 | Template filters para formulários |
| 🌐 | ![django-cors-headers](https://img.shields.io/badge/-CORS-092E20?logo=django&logoColor=white) | 4.9.0 | CORS suporte |
| ⚪ | ![WhiteNoise](https://img.shields.io/badge/-WhiteNoise-CCCCCC?logo=python&logoColor=white) | 6.12.0 | Static files serving |

### 🚀 **API Documentation**

| 📖 | Tecnologia | Versão | Propósito |
| :---: | :--- | :---: | :--- |
| 📖 | ![drf-spectacular](https://img.shields.io/badge/-drf--spectacular-A30000?logo=django&logoColor=white) | 0.29.0 | OpenAPI/Swagger Schema |

### 🐳 **DevOps & Containerização**

| 🐳 | Tecnologia | Versão | Propósito |
| :---: | :--- | :---: | :--- |
| 🐳 | ![Docker](https://img.shields.io/badge/-Docker-2496ED?logo=docker&logoColor=white) | latest | Containerização |
| 🐙 | ![Docker Compose](https://img.shields.io/badge/-Docker%20Compose-2496ED?logo=docker&logoColor=white) | latest | Orquestração |

---

## 📦 Dependências Python (Categorizado)

### 🔴 **Framework Core (17 pacotes)**

```
Django==6.0.4                              # Framework web principal
djangorestframework==3.17.1                # REST API framework
asgiref==3.11.1                           # ASGI utilities
sqlparse==0.5.5                           # SQL parser
```

### 🟠 **Banco de Dados (2 pacotes)**

```
mysqlclient==2.2.8                        # MySQL adapter Python
dj-database-url==2.3.0                    # Database URL parser
```

### 🟡 **Cache & Session (3 pacotes)**

```
redis==7.4.0                              # Redis client
django-redis==6.0.0                       # Django Redis backend
channels-redis==4.2.0                     # Channels Redis layer
```

### 🟢 **Processamento Assíncrono (4 pacotes)**

```
celery==5.6.3                             # Task queue
flower==2.0.1                             # Celery monitoring
channels==4.2.0                           # WebSockets & Async
daphne==4.1.0                             # ASGI server
```

### 🔵 **Autenticação & Segurança (7 pacotes)**

```
djangorestframework_simplejwt==5.5.1      # JWT tokens
django-axes==6.3.1                        # Login attempt tracking
django-two-factor-auth==1.17.0+           # 2FA support
django-csp==4.0                           # Content Security Policy
cryptography==46.0.7                      # Cryptographic recipes
pyHanko==0.34.1                           # PDF digital signatures
pyhanko-certvalidator==0.30.2             # Certificate validation
```

### 🟣 **Observabilidade & Monitoramento (4 pacotes)**

```
django-health-check==3.18.1+              # Health checks
django-prometheus==2.3.1                  # Prometheus metrics
sentry-sdk==2.22.0                        # Error tracking
psutil==5.9.8+                            # System monitoring
```

### 🌐 **Cloud Storage (2 pacotes)**

```
cloudinary==1.44.2                        # Cloud storage service
django-cloudinary-storage==0.3.0          # Django integration
```

### 📄 **Processamento de Documentos (6 pacotes)**

```
reportlab==4.5.0                          # PDF generation
xhtml2pdf==0.2.17                         # HTML to PDF
pypdf==6.10.2                             # PDF manipulation
pillow==12.2.0                            # Image processing
svglib==1.6.0                             # SVG support
lxml==6.1.0                               # XML/HTML processing
```

### 🛡️ **Validação & Segurança (3 pacotes)**

```
django-zxcvbn-password==2.1.1+            # Strong password checking
validate-docbr==2.0.0+                    # CPF/CNPJ validation
django-session-timeout==0.1.0             # Session timeout
```

### 📋 **Auditoria & Histórico (2 pacotes)**

```
django-simple-history==3.7.0+             # Change tracking
django-impersonate==1.9.3+                # Admin impersonation
```

### 🔍 **Qualidade de Código (10 pacotes)**

```
pytest==latest                            # Testing framework
coverage==7.13.5                          # Code coverage
black==26.3.1                             # Code formatter
isort==8.0.1                              # Import sorter
flake8==7.3.0                             # Linter
pylint==4.0.5                             # Code analyzer
mypy==1.20.1                              # Type checker
django-stubs==6.0.3                       # Django type hints
django-stubs-ext==6.0.3                   # Extended stubs
pylint-django==2.7.0                      # Django support
```

### 🌐 **Utilitários & Misc (18 pacotes)**

```
requests==2.33.1                          # HTTP client
PyYAML==6.0.3                             # YAML parser
python-dotenv==1.2.2                      # .env files
python-decouple==3.8                      # Configuration
PyJWT==2.12.1                             # JWT tokens
packaging==26.2                           # Package utilities
click==8.3.2                              # CLI framework
colorama==0.4.6                           # Terminal colors
certifi==2026.2.25                        # SSL certificates
charset-normalizer==3.4.7                 # Charset detection
idna==3.13                                # IDNA support
urllib3==2.6.3                            # HTTP client
six==1.17.0                               # Python 2/3 compatibility
tzdata==2026.1                            # Timezone data
tzlocal==5.3.1                            # Local timezone
```

### 🚀 **Server & Deployment (2 pacotes)**

```
gunicorn==23.0.0                          # WSGI HTTP server
whitenoise==6.12.0                        # Static files serving
```

---

## 🐳 DevOps & Infraestrutura

### 🐋 **Docker & Containerização**

```dockerfile
# Imagem Base
FROM python:3.12-slim

# Ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Sistema
- gcc (compilação)
- default-libmysqlclient-dev (MySQL)
- pkg-config (configuração)
- libcairo2, libpango-1.0-0, libgdk-pixbuf2.0-0 (gráficos)
- shared-mime-info (tipos MIME)

# Portas Expostas
- 8000 (Django/WSGI)
- 8001 (ASGI/WebSockets)
```

### 🗂️ **Docker Compose - Orquestração**

```yaml
Services:
├── db (MySQL 8.0)
│   ├── Porta: 3306
│   ├── Volume: mysql_data:/var/lib/mysql
│   ├── Health Check: mysqladmin ping
│   └── Timeout: 20s, Retries: 10
│
├── redis (7-alpine)
│   ├── Porta: 6379
│   └── Uso: Cache, Session, Message Queue
│
├── rabbitmq (3-management-alpine)
│   ├── AMQP: 5672
│   ├── Management UI: 15672
│   ├── Usuário: guest / guest
│   └── Health Check: rabbitmq-diagnostics
│
├── web (Django App)
│   ├── Porta: 8000
│   ├── Comando: python manage.py runserver 0.0.0.0:8000
│   ├── Depends On: db, rabbitmq, redis
│   └── Volumes: ./:/app
│
├── worker (Celery)
│   ├── Comando: celery -A config worker --loglevel=info
│   ├── Depends On: db, rabbitmq
│   └── AMQP Broker: amqp://guest:guest@rabbitmq:5672//
│
├── flower (Celery Monitor)
│   ├── Porta: 5555
│   ├── Comando: celery -A config flower --port=5555
│   └── UI Dashboard: http://localhost:5555
│
├── prometheus (Monitoring)
│   ├── Porta: 9090
│   ├── Config: ./prometheus.yml
│   └── Scrape Interval: 15s
│
└── grafana (Visualization)
    ├── Porta: 3000
    ├── Admin: admin/admin
    └── Datasource: Prometheus
```

### 🚀 **Deployment**

```yaml
render.yaml - Render Deployment Config
├── Web Service
│   ├── Runtime: python-3.12
│   ├── Build: pip install -r requirements.txt
│   ├── Start: gunicorn config.wsgi:application
│   └── Scaling: Auto-scaling enabled
│
├── Worker Service
│   ├── Type: Background Worker
│   └── Scaling: Dynamic based on queue
│
└── Database
    ├── Type: PostgreSQL (Production)
    └── Backup: Automated daily
```

### 📊 **Monitoramento**

```
prometheus.yml Configuration
├── Scrape Interval: 15s
├── Evaluation Interval: 15s
├── Targets:
│   ├── localhost:8000 (Django Metrics)
│   ├── localhost:9090 (Prometheus Self)
│   └── localhost:6379 (Redis)
└── Alert Rules: Custom alerting
```

### 🔧 **CI/CD Readiness**

- ✅ Docker multi-stage builds
- ✅ Environment variable configuration
- ✅ Health check endpoints
- ✅ Automated migrations
- ✅ Static files collection
- ✅ Database seeding capability

---

## 🗄️ Banco de Dados

### 📊 **MySQL 8.0**

```sql
-- Configuração
Charset: utf8mb4
Collation: utf8mb4_unicode_ci
Storage Engine: InnoDB
Max Connections: Configurável

-- Features
- Transactions (ACID)
- Full-Text Search
- JSON Support
- Partitioning
- Replication Ready
```

### 🗄️ **Esquema de Dados**

```
Aplicações (apps/) com Modelos:
├── ti/
│   ├── models.py
│   ├── ConfiguracaoSeguranca
│   ├── RegraWAF
│   └── [54 migrations]
│
├── seguranca/
│   ├── LogAuditoria (auditoria LGPD)
│   ├── LogErro (exceções)
│   ├── BlacklistIP (bloqueios)
│   ├── BugReport (feedback)
│   └── [8 migrations]
│
├── usuarios/
│   ├── UsuarioSIGE (custom user)
│   ├── Perfil
│   ├── Acesso
│   └── [42 migrations]
│
├── academico/
│   ├── Turma
│   ├── Atividade
│   ├── Frequência
│   ├── Nota
│   └── [35 migrations]
│
├── financeiro/
│   ├── Mensalidade
│   ├── Pagamento
│   ├── Inadimplência
│   └── [20 migrations]
│
└── [Outros módulos com migrations]
```

### 📈 **Relacionamentos**

- **Foreign Keys**: Cascade delete configurado apropriadamente
- **Índices**: Otimizados para queries frequentes
- **Constraints**: Integridade referencial garantida
- **Timestamps**: auto_now_add e auto_now padrão

### 🔐 **Segurança**

- Senhas com hash PBKDF2 (Django)
- Campos sensíveis criptografados
- SQL Injection previsto (ORM Django)
- LGPD compliance (retenção de dados)

---

## 🧩 Módulos & Aplicações

### 📚 **Módulos Principais**

| Módulo | Versão | Linha | Status | Descrição |
| :--- | :---: | :---: | :---: | :--- |
| **ti** | v8.0 | 1,245 | ✅ Production | Mission Control, SOC, Telemetria, Snapshots |
| **seguranca** | v1.3 | 892 | ✅ Production | Shield, Auditoria LGPD, Incidentes |
| **usuarios** | v2.2 | 1,156 | ✅ Production | RBAC, 2FA, Autenticação |
| **academico** | v1.5 | 2,034 | ✅ Production | Turmas, Atividades, Frequência |
| **comum** | v2.0 | 890 | ✅ Production | Utilitários, Migrations, Tenants |
| **financeiro** | v1.4 | 1,245 | ⚠️ Beta | Mensalidades, Pagamentos, BI |
| **saude** | v1.2 | 634 | ⚠️ Beta | Ficha Médica, Atestados |
| **biblioteca** | v1.1 | 523 | ⚠️ Beta | Acervo, Empréstimos |
| **comunicacao** | v1.0 | 412 | ⚠️ Alpha | Mensagens, Notificações |
| **iot** | v1.0 | 234 | ⚠️ Alpha | Integração de Sensores |
| **dashboards** | v1.0 | 567 | ✅ Production | Painéis Analíticos |
| **calendario** | v1.0 | 289 | ✅ Production | Calendário Acadêmico |

### 🗂️ **Estrutura de Diretórios**

```
apps/
├── ti/
│   ├── management/          # Custom commands
│   ├── migrations/          # Database migrations (54+)
│   ├── models.py           # Data models
│   ├── views.py            # View logic
│   ├── urls.py             # URL routing
│   ├── consumers.py        # WebSocket consumers
│   ├── routing.py          # WebSocket routing
│   ├── signals.py          # Event handlers
│   ├── middleware.py       # HTTP middleware
│   ├── static/ti/          # CSS, JS
│   ├── templates/ti/       # HTML templates
│   ├── utils/              # Utilities
│   ├── tests/              # Unit tests
│   └── admin.py            # Admin interface
│
├── seguranca/
│   ├── models/
│   │   ├── log_auditoria.py
│   │   ├── log_erro.py
│   │   ├── blacklist.py
│   │   ├── bug_report.py
│   │   └── configuracao.py
│   ├── views/
│   ├── urls/
│   ├── templates/seguranca/
│   ├── utils/
│   └── middleware.py
│
├── usuarios/
│   ├── models/
│   ├── views/
│   │   ├── registros/       # Registro por tipo
│   ├── forms/
│   ├── services/
│   ├── backends.py         # Custom authentication
│   └── context_processors.py
│
├── academico/
│   ├── models/
│   ├── views/
│   ├── services/
│   ├── filters.py
│   ├── selectors.py
│   └── admin.py
│
└── [outros módulos com estrutura similar]

config/
├── settings.py             # Django settings
├── urls.py                # URL routing
├── wsgi.py                # WSGI application
├── asgi.py                # ASGI (WebSockets)
├── celery.py              # Celery configuration
└── api_views.py           # Shared API views
```

---

## 📊 Status de Testes

### 📈 **Cobertura Geral**

```
Estatísticas:
├── Total de Testes: 149
├── Passando: 128 ✅
├── Falhando: 21 ⚠️
├── Cobertura de Código: 68%
├── Statements Rastreados: 7.732
└── Último Executado: 2026-05-18
```

### 🧪 **Breakdown por Módulo**

| Módulo | Testes | Cobertura | Status |
| :--- | :---: | :---: | :--- |
| `academico` | 49 ✅ | ~75% | Stable |
| `usuarios` | 35 ✅ | ~82% | Stable |
| `comum` | 28 ✅ | ~90% | Excellent |
| `ti` | 3 ✅ | ~65% | Developing |
| `financeiro` | 18 ⚠️ | ~55% | Partial |
| `saude` | 12 ⚠️ | ~50% | Partial |
| `biblioteca` | 15 ⚠️ | ~60% | Partial |
| **TOTAL** | **149** | **68%** | **Production** |

### 🔧 **Test Frameworks**

```
pytest==latest          # Test runner
coverage==7.13.5       # Coverage reporting
pytest-cov             # Coverage plugin
pytest-django          # Django support
factory-boy            # Test factories
faker                  # Fake data
```

### 📍 **HTML Coverage Report**

```
htmlcov/
├── index.html          # Coverage summary
├── status.json         # JSON report
├── z_*.html            # Per-file coverage
└── styles/             # Report styling
```

---

## 🚀 Quick Start

### 📋 **Pré-requisitos**

- Python 3.12+
- MySQL 8.0
- Redis 7.0+
- Docker & Docker Compose (opcional)
- Git

### 🛠️ **Instalação Local (Desenvolvimento)**

```bash
# 1️⃣ Clone o repositório
git clone https://github.com/seu-usuario/SIGE.git
cd SIGE

# 2️⃣ Crie e ative o ambiente virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3️⃣ Instale dependências
pip install --upgrade pip
pip install -r requirements.txt

# 4️⃣ Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações

# 5️⃣ Execute migrações
python manage.py migrate

# 6️⃣ Crie superusuário
python manage.py createsuperuser

# 7️⃣ Colete arquivos estáticos
python manage.py collectstatic --noinput

# 8️⃣ Inicie o servidor
python manage.py runserver
```

### 🐳 **Instalação com Docker**

```bash
# 1️⃣ Crie arquivo .env
cp .env.example .env

# 2️⃣ Inicie os serviços
docker-compose up -d

# 3️⃣ Execute migrações
docker-compose exec web python manage.py migrate

# 4️⃣ Crie superusuário
docker-compose exec web python manage.py createsuperuser

# 5️⃣ Verifique os serviços
docker-compose ps
```

### ✅ **Verificações**

```bash
# Executar testes
pytest

# Testes com cobertura
pytest --cov=. --cov-report=html

# Validar código
flake8 apps/
pylint apps/
mypy apps/

# Formatar código
black apps/
isort apps/

# Health check
curl http://localhost:8000/health/
```

### 🌐 **Acessar a Aplicação**

```
Web: http://localhost:8000
Admin: http://localhost:8000/admin
API Docs: http://localhost:8000/api/schema/swagger/
Flower: http://localhost:5555 (Celery)
Prometheus: http://localhost:9090
Grafana: http://localhost:3000 (admin/admin)
```

---

## 📚 Documentação Completa

| Documento | Descrição |
| :--- | :--- |
| [API.md](docs/API.md) | Documentação de endpoints REST e Swagger |
| [DEVOPS.md](docs/DEVOPS.md) | CI/CD, deployment e infraestrutura |
| [SEGURANCA.md](docs/SEGURANCA.md) | Protocolos de segurança e LGPD |
| [INFRAESTRUTURA.md](docs/INFRAESTRUTURA.md) | Cloud, cache, replicação |
| [INSTALACAO.md](docs/INSTALACAO.md) | Guia de instalação passo-a-passo |
| [TESTES.md](docs/TESTES.md) | Estratégia de testes e cobertura |
| [FLOWER_MONITOR.md](docs/FLOWER_MONITOR.md) | Monitoramento de tarefas Celery |
| [GUIA_APRESENTACAO.md](docs/GUIA_APRESENTACAO.md) | Apresentação para stakeholders |
| [COMPENDIO_TECNICO.md](docs/COMPENDIO_TECNICO.md) | Referência técnica completa |
| [ROADMAP.md](docs/ROADMAP.md) | Plano de desenvolvimento futuro |

---

## 🔐 Conformidade & Segurança

✅ **LGPD Compliant** — Auditoria total de acessos, direito ao esquecimento  
✅ **OWASP Top 10** — Proteção contra vulnerabilidades comuns  
✅ **CSRF Protection** — Tokens CSRF em todos os formulários  
✅ **XSS Prevention** — Escaping automático de templates  
✅ **SQL Injection Prevention** — ORM Django seguro  
✅ **Brute Force Protection** — django-axes com limite de tentativas  
✅ **MFA Support** — 2FA opcional via TOTP  
✅ **Encryption** — Criptografia AES-256 para dados sensíveis  
✅ **SSL/TLS** — HTTPS obrigatório em produção  
✅ **CORS Security** — Whitelist de origens configurável  

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um Fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### 📋 **Diretrizes**

- Mantenha 100% de cobertura de testes para novas funcionalidades
- Siga PEP 8 (use Black para formatação)
- Escreva docstrings descritivas
- Localize strings em português
- Atualize documentação

---

## 📞 Suporte & Contato

- 📧 Email: suporte@sige.edu.br
- 📱 WhatsApp: (11) 98765-4321
- 🐛 Issues: [GitHub Issues](https://github.com/JGuilhermeSneto/SIGE/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/JGuilhermeSneto/SIGE/discussions)

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** — veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 🙏 Agradecimentos

- Django community
- DRF contributors
- Open source maintainers

---

<div align="center">

### 🚀 SIGE v8.0 Apex

**Sistema Integrado de Gestão Escolar**

Desenvolvido com ❤️ usando Django, Python e tecnologias open-source

![Stars](https://img.shields.io/github/stars/JGuilhermeSneto/SIGE?style=flat-square)
![Contributors](https://img.shields.io/github/contributors/JGuilhermeSneto/SIGE?style=flat-square)
![License](https://img.shields.io/github/license/JGuilhermeSneto/SIGE?style=flat-square)

[⬆ Voltar ao Topo](#-sige--sistema-integrado-de-gestão-escolar)

</div>
