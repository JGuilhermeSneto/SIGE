<div align="center">

# 🏫 SIGE — Sistema Integrado de Gestão Escolar
### A Engenharia de Software Aplicada à Educação de Alta Performance

<br/>

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

<br/>

![License](https://img.shields.io/badge/Licen%C3%A7a-MIT-green?style=flat-square)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen?style=flat-square)
![Linting](https://img.shields.io/badge/Quality-10%2F10-blueviolet?style=flat-square)
![Coverage](https://img.shields.io/badge/Coverage-100%25-orange?style=flat-square)
![MyPy](https://img.shields.io/badge/Types-Strict-blue?style=flat-square)

<br/>

> **SIGE** não é apenas um sistema de gestão — é uma infraestrutura completa de software focada em escalabilidade, segurança e experiência do usuário. Desenvolvido com uma arquitetura **MTV** robusta, integra automação acadêmica com padrões modernos de UI/UX.

[🚀 Primeiros Passos](#-instalação-e-configuração) • [🏗️ Arquitetura](#-topografia-do-projeto) • [🧠 Regras de Negócio](#-lógica-de-negócio-e-algoritmos) • [🎨 Design System](#-design-system--uiux) • [🧪 QA & CI/CD](#-garantia-de-qualidade--devops) • [🛣️ Roadmap](#-futuras-melhorias-e-roadmap)

</div>

---

## 📖 1. Visão Geral e Módulos

O SIGE resolve a fragmentação de dados em instituições de ensino, centralizando o fluxo de vida acadêmica desde a matrícula até a emissão de relatórios consolidados.

### 🧩 Decomposição de Módulos (Meticulosa)

| Módulo | Escopo Técnico | Cobertura Funcional |
| :--- | :--- | :--- |
| **🛡️ Gestão de Identidade (IAM)** | Autenticação RBAC personalizada. | Controle de perfis, reset de senha seguro, gestão de fotos via `Pillow`. |
| **🏫 Infraestrutura Acadêmica** | Gestão de entidades relacionais. | CRUD completo de Turmas, Disciplinas e Grade Horária com detecção de conflitos. |
| **📊 Engine de Desempenho** | Algoritmos de média e status. | Lançamento de notas bimestrais com processamento automático de situação acadêmica. |
| **✅ Attendance System** | Rastreabilidade de presença. | Chamada diária vinculada à disciplina, histórico retroativo e estatística de evasão. |
| **📱 Front-End Engine** | Design System Proprietário. | Dashboards centralizados, micro-animações CSS e arquitetura responsiva multinível. |

---

## 🧠 2. Lógica de Negócio e Algoritmos

O núcleo do sistema opera sob regras estritas definidas no backend (`views.py` e `models.py`):

### ⚖️ Algoritmo de Situação Acadêmica (`_calcular_situacao_nota`)
O sistema avalia automaticamente o desempenho do aluno seguindo o fluxo:
1.  **Frequência Crítica**: Se `Presença < 75%`, o status é fixado em `Reprovado por Falta`, ignorando a média.
2.  **Média de Aprovação**: `Média >= 7.0` e `Freq >= 75%` ➔ `Aprovado`.
3.  **Recuperação**: `Média >= 5.0` e `Média < 7.0` ➔ `Recuperação`.
4.  **Reprovação**: `Média < 5.0` ➔ `Reprovado`.

### 📅 Geração de Calendário (Sincronia JS/Python)
- **Backend**: `gerar_calendario()` em `views.py` gera uma lista plana de células considerando bissextos e semanas escolares (Início no Domingo).
- **Frontend**: Utiliza JavaScript puro no Dashboard para garantir interatividade instantânea sem recarregar a página.

### 🔐 Matriz de Permissões (RBAC)

| Perfil | Dashboard | Gerir Alunos | Gerir Prof. | Gerir Turmas | Lançar Notas | Lançar Freq. | Relatórios |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **👑 SuperUser** | Total | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| **🏛️ Gestor** | Admin | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| **👨‍🏫 Professor** | Academic | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| **🎓 Aluno** | Personal | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

---

## 🛠️ 3. Stack Tecnológica & Dependências

O SIGE é construído sobre um ecossistema de 36 bibliotecas de alto nível.

<details>
<summary><b>📦 Clique para ver o catálogo completo de dependências</b></summary>

#### Core & Web
*   [Django 6.0](https://www.djangoproject.com/): Framework Web de alta performance (The "Ridiculously Fast" framework).
*   [python-decouple](https://pypi.org/project/python-decouple/): Abstração de variáveis de ambiente para segurança.
*   [python-dotenv](https://pypi.org/project/python-dotenv/): Suporte a arquivos `.env`.

#### Banco de Dados & Persistence
*   [mysqlclient](https://pypi.org/project/mysqlclient/): Driver nativo em C para integração MySQL de baixa latência.
*   [sqlparse](https://pypi.org/project/sqlparse/): Processamento e formatação de SQL.

#### UI & Ativos
*   [Pillow](https://python-pillow.org/): Processamento de imagens (fotos de perfil).
*   [ReportLab](https://www.reportlab.com/): Motor de geração de PDFs para boletins e relatórios.
*   [django-widget-tweaks](https://github.com/jazzband/django-widget-tweaks): Renderização avançada de formulários HTML5.

#### Garantia de Qualidade (QA)
*   [Black](https://github.com/psf/black): O formatador de código "uncompromising".
*   [Flake8](https://flake8.pycqa.org/): Validação de estilo PEP8.
*   [Mypy](http://mypy-lang.org/): Verificação de tipagem estática.
*   [Pylint](https://pylint.org/): Análise profunda de erros e qualidade de código.
*   [Coverage](https://coverage.readthedocs.io/): Medição de cobertura de testes unitários.
*   [isort](https://pycqa.github.io/isort/): Organização automática de imports.

</details>

---

## 🏗️ 4. Topografia do Projeto

Mapeamento meticuloso da estrutura de arquivos:

| Diretório/Arquivo | Função Crítica |
| :--- | :--- |
| `core/models.py` | Definição do Esquema de Banco e Integridade de Dados. |
| `core/views.py` | Lógica Central de Negócio e Roteamento de Dashboards. |
| `core/templatetags/` | Filtros customizados de auxílio a templates (`get_item`, `dict_get`). |
| `core/static/core/css/` | **Design System**: Global CSS, Variáveis e Animações. |
| `notas/settings.py` | Configurações de segurança distribuídas via `decouple`. |
| `.github/workflows/` | Automatização do Pipeline de Continuous Integration. |

---

## 🎨 5. Design System & UI/UX

O SIGE implementa uma interface **Premium Dark Mode** baseada em tokens de design:

### 💠 Design Tokens (Variáveis CSS)
*   `--accent-cyan`: `#22d3ee` (Identidade do Professor)
*   `--accent-violet`: `#7c6fff` (Identidade do Superusuário)
*   `--bg-base`: `#090e1a` (Background Profundo)

### 📽️ Catálogo de Animações
*   `iconFloat`: Translação suave em Y para feedback interativo em cards.
*   `diaAtualPulse`: Efeito de pulsação luminosa no calendário para o dia hoje.
*   `fadeUp`: Transição suave de entrada para componentes asíncronos.

---

## 🧪 6. Garantia de Qualidade & DevOps

Nossa pipeline de CI/CD não permite a entrada de código que não atinja os critérios:

```bash
# 1. Conformidade Estética
flake8 .
black --check .

# 2. Tipagem e Integridade
mypy .
pylint core/

# 3. Testes e Cobertura
coverage run manage.py test
coverage report -m
```

A cada `push` na branch `main`, o **GitHub Actions** valida esses 3 pilares. Falhas bloqueiam o merge automaticamente.

---

## 🛣️ 7. Futuras Melhorias e Roadmap

O projeto está em constante evolução. Nossos próximos passos são:

*   [ ] **API RESTful**: Implementação de Django Rest Framework para integração com apps mobile.
*   [ ] **Dashboard de BI**: Gráficos analíticos de desempenho escolar usando `Chart.js`.
*   [ ] **Notificações Push**: Alertas em tempo real sobre notas e faltas.
*   [ ] **Multi-Tenancy**: Suporte para múltiplas escolas em uma única instância do banco.

---

## 🚀 8. Instalação (Setup Rápido)

1.  **Clone & VENV**:
    ```bash
    git clone https://github.com/JGuilhermeSneto/SIGE.git
    cd SIGE
    python -m venv venv
    source venv/bin/activate # Ou venv\Scripts\activate no Windows
    ```
2.  **Config**:
    ```bash
    pip install -r requirements.txt
    cp .env.example .env # Edite com suas credenciais
    ```
3.  **Boot**:
    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
    ```

---

## 👥 Equipe Desenvolvedora

| João Batista | José Guilherme | Suanderson Santos | Israel Cipriano | Pedro Henrique | Vanessa Gonçalves |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 🎓 UI/UX | 🏗️ Backend | 🧪 QA | 📂 Database | ⚖️ Legal | 📊 Testing |

<br/>

<div align="center">

Desenvolvido com excelência técnica pela equipe SIGE.

</div>
