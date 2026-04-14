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
![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?style=flat-square)

<br/>

> **SIGE** centraliza a gestão acadêmica em uma aplicação **Django** (arquitetura **MTV**), com perfis de aluno, professor e gestor, frequência, notas, calendário e relatórios. A interface usa um **design system** próprio em CSS (tokens, componentes e animações) e JavaScript para interações (calendário, frequência, formulários).

[Visão geral](#1-visão-geral-e-módulos) · [Regras de negócio](#2-lógica-de-negócio-e-algoritmos) · [Stack](#3-stack-tecnológica--dependências) · [Topografia](#4-topografia-do-projeto) · [Design system](#5-design-system--uiux) · [CI/CD](#6-garantia-de-qualidade--devops) · [Roadmap](#7-futuras-melhorias-e-roadmap) · [Instalação](#8-instalação-setup-rápido) · [Front-end Vite](#9-front-end-vite-em-paralelo)

</div>

---

## 📖 1. Visão Geral e Módulos

O SIGE reduz a fragmentação de dados em instituições de ensino, cobrindo matrículas, turmas, disciplinas, lançamento de notas e frequência até relatórios consolidados.

### 🧩 Aplicativos Django (`apps/`)

| Módulo | Escopo técnico | Cobertura funcional |
| :--- | :--- | :--- |
| **`apps.usuarios`** | Autenticação, perfis e painéis por papel. | Login, reset de senha, cadastro/edição de perfis, dashboards (superusuário, gestor, professor, aluno). |
| **`apps.academico`** | Domínio acadêmico e regras de negócio. | Turmas, disciplinas, grade horária, notas, frequência, atividades, relatórios. |
| **`apps.calendario`** | Calendário acadêmico e eventos. | Visualização mensal, integração com utilitários de grade em `apps.academico`. |
| **`apps.comum`** | Recursos compartilhados. | Formulários base, templatetags, **estáticos globais** em `static/core/`. |

---

## 🧠 2. Lógica de Negócio e Algoritmos

As regras de situação acadêmica estão centralizadas em `apps/academico/utils/academico.py` (constantes e funções como `_calcular_situacao_nota`).

### ⚖️ Situação acadêmica (resumo)

1. **Frequência crítica**: se presença **&lt; 75%**, status **Reprovado por Falta** (a média não desfaz essa regra).
2. **Aprovação**: média **≥ 7,0** e frequência **≥ 75%** → **Aprovado**.
3. **Recuperação**: média **≥ 5,0** e **&lt; 7,0** → **Recuperação**.
4. **Reprovação**: média **&lt; 5,0** → **Reprovado**.

### 📅 Calendário

- **View principal**: `visualizar_calendario` em `apps/calendario/views/calendario.py` (monta o mês/ano e usa `gerar_calendario` de `apps.academico.utils.interface_usuario`).
- **Frontend**: JavaScript em `apps/comum/static/core/js/` (por exemplo `ui_utils.js`, `calendar.js`).

### 🔐 Matriz de permissões (RBAC)

| Perfil | Painel amplo | Alunos / prof. / turmas | Notas | Frequência | Relatórios |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Superusuário** | ✅ | ✅ | ✅ | ❌ | ✅ |
| **Gestor** | ✅ | ✅ | ✅ | ❌ | ✅ |
| **Professor** | — | ❌ | ✅ | ✅ | ✅ |
| **Aluno** | — | ❌ | ❌ | ❌ | ❌ |

*(Detalhes finos estão nos decorators e checagens em cada view.)*

---

## 🛠️ 3. Stack Tecnológica & Dependências

Tudo fica em **um único** `requirements.txt`, com blocos comentados (execução × desenvolvimento/CI). Basta `pip install -r requirements.txt` em qualquer máquina.

<details>
<summary><b>📦 Catálogo resumido (ver o próprio <code>requirements.txt</code>)</b></summary>

#### Core
* [Django 6.0.x](https://www.djangoproject.com/)
* [python-decouple](https://pypi.org/project/python-decouple/) — variáveis de ambiente e `.env`
* [python-dotenv](https://pypi.org/project/python-dotenv/)

#### Banco e relatórios
* [mysqlclient](https://pypi.org/project/mysqlclient/) — MySQL em produção
* [Pillow](https://python-pillow.org/) — imagens (ex.: perfil)
* [ReportLab](https://www.reportlab.com/) — PDFs

#### Templates e formulários
* [django-widget-tweaks](https://github.com/jazzband/django-widget-tweaks)

#### Qualidade de código
* Black, Flake8, isort, Pylint, pylint-django, Mypy (django-stubs), Coverage

</details>

O `config/settings.py` registra **REST framework** e **CORS** em `INSTALLED_APPS`; os pacotes correspondentes já estão no `requirements.txt`.

---

## 🏗️ 4. Topografia do Projeto

| Caminho | Função |
| :--- | :--- |
| `config/` | Pacote de configuração Django: `settings.py`, `urls.py` (rotas `admin/`, `academico/`, `calendario/`, raiz para `apps.usuarios`), `wsgi.py`, `asgi.py`. |
| `manage.py` | Entrada da CLI; `DJANGO_SETTINGS_MODULE=config.settings`. |
| `apps/usuarios/` | Models de perfil, views de auth e painéis, templates em `templates/`, URLs na raiz do site. |
| `apps/academico/` | Models (`models/`), views (`views/`), forms, URLs sob prefixo `/academico/`, templates acadêmicos. |
| `apps/calendario/` | Models e views do calendário; URLs sob `/calendario/`. |
| `apps/comum/` | Formulários base, templatetags (`custom_tags`, `get_item`), estáticos em `static/core/`. |
| `.env` / `.env.example` | Segredos e opções de banco (não versionar o `.env`). |
| `.github/workflows/` | Pipeline CI (testes, migrations MySQL, flake8, pylint, mypy, coverage). |

---

## 🎨 5. Design System & UI/UX

Interface em modo escuro baseada em tokens CSS em `apps/comum/static/core/css/design_system/tokens.css`.

### 💠 Exemplos de tokens
* `--accent-cyan` — identidade professor
* `--accent-violet` — destaque superusuário
* `--bg-base` — fundo principal

### 📽️ Animações (`animations.css`)
* `iconFloat`, `diaAtualPulse`, `fadeUp`, entre outras usadas nos templates base.

---

## 🧪 6. Garantia de Qualidade & DevOps

No GitHub Actions (`.github/workflows/django.yml`), em **push** e **pull request** para `main`:

* Serviço **MySQL 8** e `python manage.py migrate`
* `coverage run --source='.' manage.py test` e `coverage report`
* `flake8 .`, `pylint **/*.py`, `mypy .`

**Python na CI:** 3.12 (o projeto também pode ser desenvolvido com 3.11+ localmente).

Localmente você pode ainda usar **Black** e **isort** (presentes no `requirements.txt`) antes de commitar.

---

## 🛣️ 7. Futuras Melhorias e Roadmap

* [ ] **API**: consolidar e documentar endpoints com Django REST Framework.
* [ ] **BI / dashboards**: gráficos de desempenho (ex.: Chart.js).
* [ ] **Notificações**: alertas sobre notas e faltas.
* [ ] **Multi-tenant**: várias escolas na mesma instância, se necessário.

---

## 🚀 8. Instalação (Setup Rápido)

1. **Clone e ambiente virtual**
    ```bash
    git clone https://github.com/JGuilhermeSneto/SIGE.git
    cd SIGE
    python -m venv venv
    # Linux/macOS: source venv/bin/activate
    # Windows: venv\Scripts\activate
    ```
2. **Dependências e variáveis** (lista completa no único `requirements.txt` na raiz)
    ```bash
    pip install -r requirements.txt
    copy .env.example .env   # Windows; em Unix: cp .env.example .env
    ```
    Edite o `.env` (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, e opcionalmente `DB_*` para MySQL — ver `config/settings.py`).
3. **Banco e servidor**
    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
    ```

Para MySQL no ambiente institucional, veja também `instruções.md`.

---

## 🔗 9. Front-end Vite em paralelo

O repositório do **React + Vite** fica em `frontend_SIGE/Frontend_SIGE` (irmão desta pasta `SIGE` no monorepo local). O back expõe **`GET /api/ping/`** (health check) e **`GET /api/dashboard/resumo/`** (totais de turmas/disciplinas e lista de turmas do banco), ambos em `config/api_views.py`, sem autenticação, para o front validar a conexão e exibir dados reais.

### Rodar Django e Vite ao mesmo tempo

1. **Terminal 1 — Django** (na pasta `SIGE`):
   ```bash
   python manage.py runserver
   ```
   O servidor padrão fica em `http://127.0.0.1:8000/`. O endpoint de teste: `http://127.0.0.1:8000/api/ping/`.

2. **Terminal 2 — Vite** (na pasta do front `frontend_SIGE/Frontend_SIGE`):
   ```bash
   npm install
   npm run dev
   ```
   O Vite encaminha requisições **`/api`** para `http://127.0.0.1:8000` (veja `vite.config.js`). Com `VITE_API_URL` vazio (padrão), o axios usa URLs relativas e o proxy aplica.

3. Abra a URL que o Vite mostrar (em geral `http://localhost:5173/`). A página deve indicar que o back-end **SIGE** respondeu.

**Sem proxy:** no front, crie `.env` a partir de `.env.example` e defina `VITE_API_URL=http://127.0.0.1:8000`. O CORS do Django já permite origens em desenvolvimento (`CORS_ALLOW_ALL_ORIGINS`); em produção restrinja origens e use HTTPS.

### React dentro do layout SIGE (templates + Vite)

Há uma rota que **reusa o `base.html` real** (menu superior, lateral, design system) e só a área principal é o app React carregado pelo Vite em modo dev:

1. Com **Django** e **Vite** rodando como acima.
2. Faça login no SIGE e acesse **`http://127.0.0.1:8000/app/vite/`** (ou use o item **App React** no menu lateral, para gestor/superusuário e professor).

O template `apps/usuarios/templates/core/app_vite.html` estende `core/base.html` e injeta `http://127.0.0.1:5173/@vite/client` e `.../src/main.jsx`. A URL do servidor Vite pode ser ajustada com **`VITE_DEV_SERVER_URL`** no `.env` (ver `config/settings.py`). Em produção (`DEBUG=False`), substitua por arquivos estáticos gerados com `npm run build` e referências em `{% static %}`.

---

## 👥 Equipe Desenvolvedora

* **João Batista** — [@JBatista](https://github.com/JBatista)
* **José Guilherme** — [@JGuilhermeSneto](https://github.com/JGuilhermeSneto)
* **Suanderson Santos** — [@JuniorNascimento2](https://github.com/JuniorNascimento2)
* **Israel Cipriano** — [@Israelf1lho](https://github.com/Israelf1lho)
* **Pedro Henrique** — [@Henrriks](https://github.com/Henrriks)
* **Vanessa Gonçalves** — [@vangoncalves](https://github.com/vangoncalves)

<br/>

<div align="center">

Desenvolvido com excelência técnica pela equipe SIGE.

</div>
