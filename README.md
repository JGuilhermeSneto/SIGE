<div align="center">

# 🏫 SIGE — Sistema Integrado de Gestão Escolar
### A Engenharia de Software Aplicada à Educação de Alta Performance

> Este projeto faz parte de um monorepo. Para um guia de inicio rápido, consulte `../README.md`.

<br/>

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)

<br/>

![License](https://img.shields.io/badge/Licen%C3%A7a-MIT-green?style=flat-square)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white)

<br/>

> **SIGE** centraliza a gestão acadêmica em uma aplicação **Django** (arquitetura **MTV**), com perfis de aluno, professor e gestor, frequência, notas, calendário e relatórios. A interface usa um **design system** próprio em CSS (tokens, componentes e animações) e JavaScript para interações (calendário, frequência, formulários).

[Visão geral](#1-visão-geral-e-módulos) · [Regras de negócio](#2-lógica-de-negócio-e-algoritmos) · [Stack](#3-stack-tecnológica--dependências) · [Topografia](#4-topografia-do-projeto) · [Design system](#5-design-system--uiux) · [CI/CD](#6-garantia-de-qualidade--devops) · [Deploy](#-deploy-em-produção) · [Instalação](#8-instalação-setup-rápido)

</div>

---

## 📖 1. Visão Geral e Módulos

O SIGE reduz a fragmentação de dados em instituições de ensino, cobrindo matrículas, turmas, disciplinas, lançamento de notas e frequência até relatórios consolidados.

### 🧩 Aplicativos Django (`apps/`)

| Módulo | Escopo técnico | Cobertura funcional |
| :--- | :--- | :--- |
| **`apps.usuarios`** | Autenticação, perfis e painéis por papel. | Login, reset de senha, cadastro/edição de perfis, dashboards. RBAC completo. |
| **`apps.academico`** | Domínio acadêmico e regras de negócio. | Turmas, disciplinas, notas, frequência, materiais didáticos. |
| **`apps.dashboards`** | **Hub de Inteligência & BI** 🧠 | Unificação de BI Acadêmico + Relatórios. Dashboards de Evasão, Saúde e Performance. |
| **`apps.infraestrutura`** | Patrimônio e Almoxarifado. | Refatorado para **Clean Architecture**. Tombamento, manutenções e estoque atômico. |
| **`apps.comum`** | Recursos compartilhados. | Design System Premium, Multi-Tenancy e Audit Log. |
| **`apps.saude`** | Saúde e bem-estar escolar. | Fichas médicas, alertas de alergia e integração com BI de Inclusão. |
| **`apps.financeiro`** | BI Financeiro e Contabilidade. | Livro Diário, Faturas, DRE e KPIs gerenciais. |

- **Design System Premium — "Azul Corporativo"**
  - Padronização em componentes super-arredondados (`border-radius: 48px`), glassmorphism e animações fluidas.
- **Observabilidade & Monitoramento (Stack Elite)**
  - **Grafana + Prometheus**: Monitoramento técnico de performance em tempo real.
  - **RabbitMQ + Celery**: Processamento assíncrono industrial.
- **Design System Reforçado**
  - Bordas de cor visíveis em **todos os cards** dos temas Azul e Cinza.
  - Cache com fallback automático para `LocMemCache` em ambiente local.
- **Garantia de Qualidade**
  - **45/45 testes passando (100% verde)** — Cobertura de 55%, meta de 75%.
  - Pipeline CI/CD com Lint, Security Scan e Tests.
- **Simulador de Dados (`seed_db.py`)**
  - Geração de 10 anos de histórico escolar realista (2016-2026).

---

## 🧠 2. Lógica de Negócio e Arquitetura Clean
A lógica de negócio do SIGE segue o padrão **Service Layer** e **Selectors**, garantindo testabilidade e separação de preocupações.

- **Serviços Acadêmicos**: `apps/academico/services/`
- **Serviços de Infraestrutura**: `apps/infraestrutura/services/` (Lógica atômica de estoque)
- **Seletores de Inteligência**: `apps/dashboards/selectors/` (Leitura otimizada para BI)

---

## 🛠️ 3. Stack Tecnológica

### 💻 Linguagens & Frameworks
| | | | |
| :---: | :---: | :---: | :---: |
| ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) | ![Django](https://img.shields.io/badge/django-%23092e20.svg?style=for-the-badge&logo=django&logoColor=white) | ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) | ![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB) |

### 🗄️ Banco de Dados, Cache & Mensageria
| | | | |
| :---: | :---: | :---: | :---: |
| ![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white) | ![RabbitMQ](https://img.shields.io/badge/RabbitMQ-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white) | ![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white) | ![Cloudinary](https://img.shields.io/badge/Cloudinary-3448C5?style=for-the-badge&logo=Cloudinary&logoColor=white) |

### 🚀 Infraestrutura, DevOps & Observabilidade
| | | | |
| :---: | :---: | :---: | :---: |
| ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) | ![Grafana](https://img.shields.io/badge/grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white) | ![Prometheus](https://img.shields.io/badge/prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white) | ![Celery](https://img.shields.io/badge/celery-%2337814A.svg?style=for-the-badge&logo=celery&logoColor=white) |

---

## 🏗️ 4. Topografia do Projeto

| `apps/` | Aplicativos do sistema (Django). |
| `config/` | Configurações centrais do Django. |
| `docs/` | **Central de Documentação** (Roadmap, Gap Analysis, Infra). |
| `scripts/` | **Scripts Utilitários** e ferramentas de debug. |
| `media/` | Arquivos dinâmicos, fotos e documentos de upload. |
| `seed_db.py` | Simulador de 10 anos de dados escolares (2016–2026). |
| `manage.py` | Entrada da CLI Django. |
| `docker-compose.yml` | Orquestração completa: App + MySQL + RabbitMQ + Redis + Prometheus + Grafana. |

---

## 🎨 5. Design System & UI/UX

A interface é baseada no conceito **Premium Glassmorphism**, com foco em densidade de informação limpa para gestores.
* **Bordas 48px**: Botões e inputs em formato de pílula.
* **Hub Analítico**: Alternância rápida entre BI e Relatórios via abas dinâmicas.

---

## 🛣️ 7. Documentação Estratégica & Roadmap

| [`ROADMAP.md`](docs/ROADMAP.md) | Roadmap v2.0 com foco em IA e Integrações Financeiras. |
| [`DEPLOYMENT.md`](docs/DEPLOYMENT.md) | **Guia de Deploy (Render + Aiven)** para novos desenvolvedores. |
| [`INFRASTRUCTURE.md`](docs/INFRASTRUCTURE.md) | Guia para subir o stack de monitoramento e mensageria. |
| [`GAP_ANALYSIS.md`](docs/GAP_ANALYSIS.md) | Análise competitiva SIGE vs. SUAP/SIGEDUC. |

---

## 🚀 8. Instalação (Setup Rápido)

### 🐳 8.1. Rodando com Docker (Recomendado)
Para subir o ambiente completo com RabbitMQ e Grafana:
```bash
docker-compose up --build
```
Acesse o sistema em `http://localhost:8000`. Veja o [INFRASTRUCTURE.md](INFRASTRUCTURE.md) para configurar o Grafana.

---

## 🚀 Deploy em Produção

O SIGE está configurado para deploy contínuo no **Render** com banco de dados **MySQL** hospedado no **Aiven**.

*   **PaaS:** [Render](https://render.com/)
*   **Banco de Dados:** [Aiven Console](https://console.aiven.io/)
*   **Guia Passo a Passo:** Consulte o documento [**`docs/DEPLOYMENT.md`**](docs/DEPLOYMENT.md).

---

<div align="center">

Desenvolvido com excelência técnica pela equipe SIGE.

</div>
