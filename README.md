<div align="center">

# 🛡️ SIGE — Back-end (Django Core Engine)
### O Coração do Ecossistema SIGE: Alta Performance e Segurança Industrial

> Este é o núcleo central do SIGE. Ele gerencia a API, lógica de negócio e persistência para as frentes **Web (Django/React)**, **Mobile** e **IoT**.

<br/>

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)

<br/>

[Estrutura do Projeto](#1-estrutura-do-back-end) · [Segurança & Criptografia](#2-seguran%C3%A7a--criptografia) · [Stack Técnica](#3-stack-tecnol%C3%B3gica) · [Qualidade & Testes](#4-qualidade--testes) · [Deploy](#5-deploy-em-produ%C3%A7%C3%A3o)

</div>

---

## 🏛️ 1. Estrutura do Back-end

O Back-end é o pilar principal do SIGE, responsável por fornecer dados e regras para:
1.  **Web (Django Templates + Design System)**: Interface clássica estável.
2.  **Web (React + Vite)**: Interface de alta densidade via API.
3.  **Mobile (Expo)**: Notificações e acesso discente via API.
4.  **IoT (ESP32)**: Coleta de dados físicos via MQTT/API.

### 🧩 Módulos Core (`apps/`)

| Módulo | Escopo técnico | Papel no Ecossistema |
| :--- | :--- | :--- |
| **`usuarios`** | Auth, RBAC e Perfil. | Gerencia identidades e permissões de todos os apps. |
| **`academico`** | Lógica de Notas/Frequência. | Engine de regras e **Notificações Unificadas**. |
| **`iot`** | **Automação & MQTT** 🤖 | Interface com hardware (RFID/Sensores). |
| **`seguranca`** | **Shield v1.2 (Hardening)** 🛡️ | Honeypot, Auto-Blacklist, PII Scrubbing e TI Workflow. |
| **`financeiro`** | Fluxo de Caixa e BI. | Gestão de faturas e KPIs financeiros. |
| **`documentos`** | ReportLab Engine. | Geração atômica de PDFs oficiais. |

---

## 🔒 2. Segurança & Criptografia (Shield v1.2)

O SIGE implementa uma camada de segurança de nível industrial para proteção de dados sensíveis:

-   **AES-256 Encryption**: Dados sensíveis (CPF, Endereço) criptografados em repouso.
-   **Admin Honeypot**: Armadilha para bots que tentam acessar o admin sem autenticação (Banimento Automático).
-   **Auto-Blacklist Proativo**: Bloqueio de IPs com comportamento anômalo ou alto volume de erros.
-   **PII Sanitization**: Scrubbing automático de dados sensíveis em logs de erro (Conformidade LGPD).
-   **Magic Number Validation**: Verificação binária de assinaturas de arquivos para impedir uploads maliciosos.
-   **Audit Log**: Rastreamento completo de acesso a áreas críticas.
-   **Maintenance Kill-Switch**: Middleware global para isolamento do sistema em manutenção.

---

## 🛠️ 3. Stack Tecnológica

-   **Framework**: Django 6.0 (Architecture MTV + Service Layer).
-   **Banco de Dados**: MySQL 8.0 (Hospedado no Aiven).
-   **Mensageria**: RabbitMQ + Celery para tarefas assíncronas (PDFs, E-mails).
-   **Observabilidade**: Prometheus + Grafana para métricas de performance.
-   **Cache**: Redis para aceleração de respostas em produção.

---

## 🧪 4. Qualidade & Testes

A estabilidade do SIGE é garantida por uma rigorosa suíte de automação:
-   **80+ testes automatizados (100% verde)**.
-   **Cobertura: ~70%** (Meta alcançada em Q2/2026).
-   **Ferramentas**: Pytest, Flake8, Pylint, Mypy.
-   **CI/CD**: GitHub Actions validando cada push antes do deploy.

---

## 🚀 5. Instalação & Setup

### Desenvolvimento Local
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Comandos de Manutenção
| Ação | Comando |
| :--- | :--- |
| **Rodar Testes** | `pytest` |
| **Popular Banco** | `python seed_db.py` |
| **Coletar Estáticos** | `python manage.py collectstatic` |

---

## 🚀 Deploy em Produção

O SIGE está configurado para deploy contínuo no **Render** com banco **MySQL** no **Aiven**.
*   **Guia Completo:** Consulte [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md).

---
<div align="center">
Desenvolvido com excelência técnica para o futuro da educação.
</div>

## 📌 Quick Wins – Ajustes a implementar hoje

- **Cobertura de testes**: adicionar testes nos services críticos (`financeiro/services/financeiro_service.py`, `usuarios/services/perfil_service.py`, `dashboards/views.py`, `saude/views.py`) e garantir >75% no CI.
- **Pre‑commit**: instalar `pre-commit` com hooks `black`, `isort`, `flake8`, `mypy`.
- **Segredos**: mover `.env` para `.gitignore`, criar `.env.example` e atualizar README com instruções de setup.
- **Cache de notas**: usar `cache.get_or_set` ao calcular total de notas no painel do professor.
- **Headers de segurança**: adicionar middleware que define CSP, HSTS, X‑Content‑Type‑Options.
- **Docker‑compose dev**: criar `docker-compose.dev.yml` com PostgreSQL, Redis, Celery e Flower.
