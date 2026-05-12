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

[Estrutura do Projeto](#1-estrutura-do-back-end) · [Segurança & Criptografia](#2-seguran%C3%A7a--criptografia) · [Área de TI Avançada](#%EF%B8%8F-%C3%A1rea-de-ti-avan%C3%A7ada-v10) · [Stack Técnica](#3-stack-tecnol%C3%B3gica) · [Qualidade & Testes](#4-qualidade--testes) · [Deploy](#6-deploy-em-produ%C3%A7%C3%A3o)

</div>

---

## 🏛️ 1. Estrutura do Back-end

O Back-end é o pilar principal do SIGE, responsável por fornecer dados e regras para:
1.  **Web (Django Templates + Design System)**: Interface clássica estável.
2.  **Web (React + Vite)**: Interface de alta densidade via API.
3.  **Portal do Responsável**: Dashboard premium com controle parental e monitoramento acadêmico.
4.  **Mobile (Expo)**: Notificações e acesso discente via API.
5.  **IoT (ESP32)**: Coleta de dados físicos (Matrícula) via MQTT/API.

### 🧩 Módulos Core (`apps/`)

| Módulo | Escopo técnico | Papel no Ecossistema |
| :--- | :--- | :--- |
| **`usuarios`** | Auth, RBAC e Perfil. | Gerencia identidades e permissões de todos os apps. |
| **`academico`** | Lógica de Notas/Frequência. | Engine de regras e **Matrículas Automáticas**. |
| **`iot`** | **Automação & MQTT** 🤖 | Interface com hardware (RFID/Matrícula). |
| **`seguranca`** | **Shield v1.2 (Hardening)** 🛡️ | Honeypot, Controle Parental e TI Workflow. |
| **`ti`** | **Área de TI Avançada** 🛠️ | **NOVO** — Painel operacional, manutenção e monitoramento administrativo. |
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

## 🛠️ Área de TI Avançada (v1.0)

O SIGE inclui um painel administrativo completo para operações de TI:

- **Painel de Monitoramento**: KPIs em tempo real com cache inteligente (5min)
- **Operações Administrativas**: Limpeza de logs, health checks, gerenciamento de cache
- **Dashboard de Segurança**: Auditoria LGPD, telemetria de erros, controle de intrusões
- **Ferramentas de Manutenção**: Sessões expiradas, configurações do sistema, export de dados
- **Interface Otimizada**: Design system consistente, paginação inteligente, UX profissional

*Consulte [`docs/TI_OPERATIONS.md`](docs/TI_OPERATIONS.md) para guia completo.*

---

## 🛠️ 3. Stack Tecnológica

-   **Framework**: Django 6.0 (Architecture MTV + Service Layer).
-   **Banco de Dados**: MySQL 8.0 (Hospedado no Aiven).
-   **Mensageria**: RabbitMQ + Celery para tarefas assíncronas (PDFs, E-mails).
-   **Observabilidade**: Prometheus + Grafana para métricas de performance.
-   **Cache**: Redis para aceleração de respostas em produção.
-   **Mídia & Performance**: Cloudinary + Lazy Loading + Placeholders CDN (UI Avatars).
-   **Queries Otimizadas**: Implementação de O(1) Queries em dashboards críticos (Prefetch/Select Related).

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

## 🚀 6. Deploy em Produção

O SIGE está configurado para deploy contínuo no **Render** com banco **MySQL** no **Aiven**.
*   **Guia Completo:** Consulte [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md).

---
<div align="center">
Desenvolvido com excelência técnica para o futuro da educação.
</div>

- **Migração React**: Iniciar migração dos componentes de BI para React/Vite.
- **Segredos**: Mover `.env` para `.gitignore`, criar `.env.example` e atualizar README com instruções de setup.
- **Testes**: Subir a cobertura para >80% no CI.
- **Docker‑compose dev**: criar `docker-compose.dev.yml` com PostgreSQL, Redis, Celery e Flower.
