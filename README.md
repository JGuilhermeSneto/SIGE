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
| **`academico`** | Lógica de Notas/Frequência. | Engine central de regras escolares. |
| **`iot`** | **Automação & MQTT** 🤖 | Interface com hardware (RFID/Sensores). |
| **`seguranca`** | **Shield v1.0** 🛡️ | Auditoria LGPD, MFA e Telemetria de Erros. |
| **`financeiro`** | Fluxo de Caixa e BI. | Gestão de faturas e KPIs financeiros. |
| **`documentos`** | ReportLab Engine. | Geração atômica de PDFs oficiais. |

---

## 🔒 2. Segurança & Criptografia

O SIGE implementa uma camada de segurança de nível industrial para proteção de dados sensíveis:

-   **AES-256 Encryption**: Dados como CPF, Data de Nascimento, Telefone e Endereço são criptografados em repouso no banco de dados.
-   **Audit Log**: Rastreamento completo de quem acessou ou modificou dados sensíveis, em conformidade com a LGPD.
-   **Protection Shield**: Telemetria em tempo real de erros (500) e monitoramento de tentativas de Brute Force.

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
-   **45/45 testes passando (100% verde)**.
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
