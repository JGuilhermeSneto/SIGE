<div align="center">

# 🏫 SIGE — Sistema Integrado de Gestão Escolar
### A Engenharia de Software Aplicada à Educação de Alta Performance

> Este projeto faz parte de um monorepo. Para um guia de inicio rápido, consulte `../README.md`.

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

### ✨ Atualizações recentes (Abr/2026)

- **Sistema de Biblioteca & Reservas**
  - Workflow completo de reserva de livros, gestão de acervo e tela de confirmação para o gestor.
  - Limite inteligente de 2 livros por aluno com integração no frontend.
- **Design System Premium**
  - Padronização de todo o sistema em três temas principais: "Indigo Profundo", "Cinza Industrial" e "Azul Corporativo".
  - Padronização global dos botões (Próximo, Salvar) garantindo alto contraste e interatividade fluida por componente.
  - Atualização do "Mural de Avisos" e "Notificações" usando o layout em `card-mural-sidebar`.
- **Gestão Acadêmica e Saúde**
  - Alunos agora têm autonomia para visualizar a própria ficha médica no sistema ("Minha Saúde").
  - Otimização do dashboard acadêmico utilizando ORM aggregations.
  - Calendário dinâmico com tooltip padronizado para sobreposição de status (ex: aula suspensa e evento).
- **Notificações & Atividades**
  - Sistema de avisos integrado por público-alvo e alertas visuais persistentes para correções de provas, notas e faltas.

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
- **Regra de geração da base anual**: não sobrescreve datas que já tenham ajustes manuais (ex.: prova/evento definido pela gestão).

### 🧪 Gabarito e entrega

- `AtividadeProfessor.exibir_gabarito_para_aluno` considera:
  - liberação manual (`gabarito_liberado=True`), ou
  - prazo encerrado (`prazo_encerrado=True`).
- A correção individual calcula a nota final e grava em `NotaAtividade`.

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
2. **Dependências e variáveis**
    ```bash
    pip install -r requirements.txt
    copy .env.example .env   # Windows
    # em Unix/macOS: cp .env.example .env
    ```
    Edite o `.env` com os valores do seu ambiente. Os campos principais são:
    - `SECRET_KEY`
    - `DEBUG` (True em desenvolvimento)
    - `ALLOWED_HOSTS`
    - `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` quando usar MySQL.

3. **Banco e servidor Django**
    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
    ```

> Se você estiver atualizando um banco existente, garanta que as migrations mais recentes foram aplicadas:
>
> ```bash
> python manage.py migrate
> ```
>
> As migrations recentes incluem:
> - `academico.0003_atividadeprofessor_gabarito_liberacao`
> - `academico.0004_notificacaoaluno`

Para MySQL no ambiente institucional, consulte também `instruções.md`.

---

## 🔗 9. Front-end Vite em paralelo

O front-end React + Vite fica em `frontend_SIGE/Frontend_SIGE`, ao lado da pasta `SIGE` no monorepo. O backend Django oferece as APIs usadas pelo app:

- `GET /api/ping/` → verifica se o backend está online
- `GET /api/dashboard/resumo/` → totais de turmas e disciplinas + amostra de turmas

Essas views estão implementadas em `SIGE/config/api_views.py`.

### Executar Django + Vite juntos

1. **Terminal 1 — Back-end**
   ```bash
   cd SIGE
   python manage.py runserver
   ```
   O servidor Django padrão fica em `http://127.0.0.1:8000/`.

2. **Terminal 2 — Front-end**
   ```bash
   cd frontend_SIGE/Frontend_SIGE
   npm install
   npm run dev
   ```
   O Vite roda em `http://127.0.0.1:5173/` e, em modo dev, proxy passa `/api` para `http://127.0.0.1:8000`.

3. Abra o endereço do Vite (geralmente `http://127.0.0.1:5173/`). A página deve mostrar que o back-end respondeu.

### Quando usar proxy ou URL direta

- `VITE_API_URL=` vazio: em dev, a app usa o proxy do Vite para `/api` → Django.
- `VITE_API_URL=http://127.0.0.1:8000`: o app chama o Django diretamente, sem proxy.

O front-end lê essa variável em `frontend_SIGE/Frontend_SIGE/src/services/api.js`.

### Autenticação JWT

Para obter um token JWT, use:

```bash
POST /api/token/
{
  "email": "seu@email.com",
  "password": "sua-senha"
}
```

Para renovar o token de acesso, use:

```bash
POST /api/token/refresh/
{
  "refresh": "<refresh_token>"
}
```

O frontend já está preparado para enviar o cabeçalho `Authorization: Bearer <access_token>` automaticamente quando o token estiver armazenado.

### Usar Vite em qualquer template Django

Para usar os assets do Vite diretamente em qualquer template do Django, carregue a biblioteca de tags e chame o entrypoint:

```django
{% load static vite_assets %}
{% vite_entry 'src/main.jsx' %}
```

Em desenvolvimento, isso injeta automaticamente `@vite/client` e o módulo do Vite. Em produção, usa o `manifest.json` gerado pelo build e serve os arquivos em `STATIC_URL/vite/`.

Alternativamente, se você quiser habilitar Vite pelo contexto no `base.html`, passe `vite_entry_name = 'src/main.jsx'` na view e o template pai o incluirá.

### Segurança em produção

Em produção, defina no `.env`:

- `DEBUG=False`
- `ALLOWED_HOSTS=seu-dominio.com`
- `SECRET_KEY` forte e secreta
- `SECURE_SSL_REDIRECT=True`
- `SESSION_COOKIE_SECURE=True`
- `CSRF_COOKIE_SECURE=True`
- `CORS_ALLOWED_ORIGINS=https://seu-dominio.com`
- `CSRF_TRUSTED_ORIGINS=https://seu-dominio.com`

Assim o Django habilita HSTS, cookies seguros, XSS e content-type protections.

### Rota integrada no Django

Enquanto o Vite estiver ativo, é possível abrir o React embutido dentro do layout do SIGE em:

```bash
http://127.0.0.1:8000/app/vite/
```

Essa view usa o template `SIGE/apps/usuarios/templates/core/app_vite.html`, que injeta o Vite dev server em desenvolvimento. Em produção, o Django serve os assets buildados.

### Build de produção

Quando estiver pronto para produção:

```bash
cd frontend_SIGE/Frontend_SIGE
npm run build
```

O build é gerado em `SIGE/apps/comum/static/vite` e o Django irá servir esses arquivos como estáticos. Em produção, configure `VITE_API_URL` para a URL pública da API e defina `DEBUG=False` no Django.

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
