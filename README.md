<div align="center">

# 🏫 SIGE
### Sistema Integrado de Gestão Escolar

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/Licen%C3%A7a-MIT-yellow?style=for-the-badge)](LICENSE)

<br/>

> **SIGE** é uma plataforma robusta e moderna para administração acadêmica, desenvolvida com **Django**. O sistema foca em uma experiência de usuário (UX) excepcional, com dashboards centralizados, automação de processos e alta qualidade de código.

[🚀 Instalação](#-instalação-e-configuração) • [🏗️ Arquitetura](#-estrutura-e-módulos) • [🎨 Interface](#-design--uiux) • [🧪 Qualidade](#-qualidade-e-testes) • [👥 Autores](#-equipe-desenvolvedora)

</div>

---

## 📌 Visão Geral do Projeto

O **SIGE** foi projetado para centralizar todas as operações de uma instituição de ensino. Diferente de sistemas genéricos, ele oferece interfaces especializadas para cada tipo de usuário, garantindo que alunos, professores e administradores tenham exatamente as ferramentas que precisam em um ambiente **Dark Mode** sofisticado.

### 🧩 Módulos Meticulosos

| Módulo | Funcionalidades de Elite |
| :--- | :--- |
| **🔐 Segurança** | Autenticação RBAC (Role-Based Access Control) com 4 níveis de permissão. |
| **📑 Acadêmico** | Matrículas, gestão de turmas por turnos e controle de disciplinas vinculadas. |
| **👨‍🏫 Professor** | Lançamento de notas bimestrais com cálculo automático de média e frequência. |
| **✅ Frequência** | Sistema de chamada diária com histórico retroativo e alertas de baixa presença. |
| **📊 Dashboards** | Paineis centralizados com micro-animações e calendários dinâmicos. |
| **📄 Relatórios** | Geração automática de documentos e boletins em PDF via ReportLab. |

---

## 🎨 Design & UI/UX

O projeto utiliza um sistema de design proprietário focado em **Profissionalismo e Fluidez**:

*   **Standardization**: Todos os ícones foram padronizados usando **FontAwesome 6**, garantindo consistência visual.
*   **Micro-Animações**: Implementamos um sistema de animações CSS nativas (Floating Icons, Pulsing Charts) que tornam a interface "viva" e responsiva.
*   **Centralização**: Dashboards com `max-width: 1200px` para leitura otimizada em monitores ultra-wide.
*   **Dark Mode Premium**: Paleta baseada em `Plus Jakarta Sans` e cores harmônicas como `Cyan`, `Emerald` e `Violet`.

---

## 🚀 Instalação e Configuração

O SIGE agora utiliza `python-decouple` para garantir uma instalação segura e portátil.

### 1️⃣ Preparação do Ambiente
```bash
# Clone o repositório
git clone https://github.com/JGuilhermeSneto/SIGE.git
cd SIGE

# Crie e ative o ambiente virtual (VENV)
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 2️⃣ Configuração de Ambiente (.env)
Crie um arquivo `.env` na raiz do projeto (use o `.env.example` como base):
```env
SECRET_KEY=sua_chave_secreta
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Para usar SQLite (padrão):
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Para usar MySQL:
# DB_ENGINE=django.db.backends.mysql
# DB_NAME=sige_db
# DB_USER=seu_usuario
# DB_PASSWORD=sua_senha
```

### 3️⃣ Inicialização do Banco
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 4️⃣ Execução
```bash
python manage.py runserver
```
Acesse: [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)

---

## 📂 Estrutura e Módulos

O projeto segue a arquitetura **MTV (Model-Template-View)** do Django organizada de forma modular:

```text
SIGE/
├── core/                   # Núcleo da aplicação (Models, Views, Logic)
│   ├── static/core/css/    # Design System centralizado
│   └── templates/          # Interfaces divididas por módulos acadêmicos
├── notas/                  # Configurações globais do projeto (Settings)
├── media/                  # Uploads de fotos e documentos
├── .github/workflows/      # Automação de CI/CD (GitHub Actions)
└── .env.example            # Template de configuração segura
```

---

## 🧪 Qualidade e Testes

Mantemos um alto padrão de integridade através de ferramentas de análise estática e cobertura:

*   **Testes Unitários**: `python manage.py test`
*   **Cobertura**: `coverage run manage.py test` && `coverage report`
*   **Linting**: `flake8 .` e `pylint **/*.py`
*   **Tipagem**: `mypy .`

---

## 👥 Equipe Desenvolvedora

Desenvolvido com dedicação por alunos da **UPE** (Universidade de Pernambuco):

<div align="center">

| | Autor | GitHub |
| :---: | :--- | :--- |
| 👤 | **João Batista** | [@JBatista](https://github.com/JBatista) |
| 👤 | **José Guilherme** | [@JGuilhermeSneto](https://github.com/JGuilhermeSneto) |
| 👤 | **Suanderson Santos** | [@Suanderson](https://github.com/Suanderson) |
| 👤 | **Israel Cipriano** | [@Israel](https://github.com/Israel) |
| 👤 | **Pedro Henrique** | [@Pedro](https://github.com/Pedro) |
| 👤 | **Vanessa Gonçalves** | [@Vanessa](https://github.com/Vanessa) |

</div>

---

<div align="center">

Desenvolvido com ❤️ pela equipe SIGE.

</div>
