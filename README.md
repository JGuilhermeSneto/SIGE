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
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square)
![Redis](https://img.shields.io/badge/Redis-Cache-DC382D?style=flat-square)

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
| **`apps.usuarios`** | Autenticação, perfis e painéis por papel. | Login, reset de senha, cadastro/edição de perfis, dashboards (superusuário, gestor, professor, aluno). RBAC completo com Groups. |
| **`apps.academico`** | Domínio acadêmico e regras de negócio. | Turmas, disciplinas, grade horária, notas, frequência, atividades com quiz/gabarito, materiais didáticos. Painel Aluno em tela cheia. |
| **`apps.calendario`** | Calendário acadêmico e eventos. | Visualização mensal interativa, eventos letivos e de recesso por turma. |
| **`apps.comum`** | Recursos compartilhados. | Formulários base, templatetags, estáticos globais em `static/core/`, Design System Premium (3 temas, tokens, animações). |
| **`apps.biblioteca`** | Gestão do acervo escolar. | Empréstimos, devoluções, controle de exemplares. **OpenLibrary API**: 200+ Best-Sellers com capas HD baixadas automaticamente. |
| **`apps.comunicacao`** | Comunicados institucionais. | Mural de avisos segmentado por público (Alunos, Professores, Todos). |
| **`apps.saude`** | Saúde e bem-estar escolar. | Fichas médicas (alergias em Rubi, PCD), vacinas, atestados com fluxo de aprovação e abono automático de faltas. |
| **`apps.financeiro`** | BI Financeiro e Contabilidade. | Livro Diário, Faturas com status, Folha de Pagamento, Centro de Custo, DRE e KPIs gerenciais. |
| **`apps.infraestrutura`** | Patrimônio e Almoxarifado. | Tombamento de bens, manutenções, estoque com alertas de reposição mínima. |

- **Design System Premium — "Azul Corporativo"**
  - Padronização em componentes super-arredondados (`border-radius: 48px`), glassmorphism e sombras dinâmicas.
  - Paleta com tokens vibrantes (Azul Corporativo, Rubi para Alertas Médicos, Esmeralda para Faturas Pagas).
- **Garantia de Qualidade & CI/CD Robusto**
  - Pipeline do GitHub Actions reformulado com jobs em paralelo: Lint, Security Scan e Tests.
  - **Deploy Contínuo (CD)**: Automatizado via SSH para servidores de produção após aprovação no CI.
- **Processamento Assíncrono e Seed Massivo**
  - **Simulador de Dados (`seed_db.py`)**: Script monumental de geração de histórico. Gera 10 anos de dados contínuos (2016-2026), processando dezenas de milhares de presenças, faturas pagas e inadimplentes, e históricos de evasão.
- **Segurança Avançada (Fortaleza Jarvis 2026 — Enterprise Grade)**
  - **🛡️ Criptografia de Dados (AES/Fernet)**: Dados sensíveis protegidos no banco de dados.
  - **📜 Trilha de Auditoria (Audit Trail)**: Registro histórico com `django-simple-history` nas finanças e perfis.
  - **✅ Validação Matemática**: Algoritmos de checksum para CPF.

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
| **Superusuário** | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| **Gestor** | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| **Professor** | — | ❌ | ✅ | ✅ | ✅ |
| **Aluno** | — | ❌ | ❌ | ❌ | ❌ |

*(Nota: Módulo de Saúde acessível por todos para envio de atestados e consulta de prontuário pessoal.)*

*(Detalhes finos estão nos decorators e checagens em cada view.)*

---

## 🛠️ 3. Stack Tecnológica

O SIGE utiliza tecnologias de ponta para garantir performance, escalabilidade e segurança.

### 💻 Linguagens & Frameworks
| | | | |
| :---: | :---: | :---: | :---: |
| ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) | ![Django](https://img.shields.io/badge/django-%23092e20.svg?style=for-the-badge&logo=django&logoColor=white) | ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) | ![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB) |

### 🗄️ Banco de Dados & Cache
| | | | |
| :---: | :---: | :---: | :---: |
| ![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white) | ![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white) | ![Cloudinary](https://img.shields.io/badge/Cloudinary-3448C5?style=for-the-badge&logo=Cloudinary&logoColor=white) | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white) |

### 🚀 Infraestrutura & DevOps
| | | | |
| :---: | :---: | :---: | :---: |
| ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) | ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white) | ![Celery](https://img.shields.io/badge/celery-%2337814A.svg?style=for-the-badge&logo=celery&logoColor=white) | ![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white) |

### 🛡️ Segurança & Qualidade
| | | | |
| :---: | :---: | :---: | :---: |
| ![Sentry](https://img.shields.io/badge/Sentry-362D59?style=for-the-badge&logo=sentry&logoColor=white) | ![ESLint](https://img.shields.io/badge/ESLint-4B3263?style=for-the-badge&logo=eslint&logoColor=white) | ![Bandit](https://img.shields.io/badge/Bandit-Security-yellow?style=for-the-badge) | ![Coverage](https://img.shields.io/badge/Coverage-53%25-green?style=for-the-badge) |

---

<details>
<summary><b>📦 Lista Completa de Dependências</b></summary>

- **Core**: `Django`, `python-decouple`, `python-dotenv`.
- **Relatórios**: `ReportLab`, `xhtml2pdf`, `Pillow`.
- **API**: `djangorestframework`, `simplejwt`, `drf-spectacular`.
- **Segurança**: `django-csp`, `django-axes`, `zxcvbn`.
- **Qualidade**: `Black`, `Flake8`, `Pylint`, `Mypy`, `Bandit`, `Pip-audit`.

</details>

---

## 🏗️ 4. Topografia do Projeto

| Caminho | Função |
| :--- | :--- |
| `config/` | Configuração Django: `settings.py`, `urls.py`, `wsgi.py`, `asgi.py`. |
| `manage.py` | Entrada da CLI Django. |
| `apps/usuarios/` | Models de perfil, views de auth, painéis e templates. |
| `apps/academico/` | Models, views, forms, URLs e templates acadêmicos. |
| `apps/financeiro/` | Livro Diário, Faturas, Folha de Pagamento, BI gerencial. |
| `apps/saude/` | Fichas médicas, atestados, vacinas e alertas de inclusão. |
| `apps/biblioteca/` | Acervo, empréstimos, integração OpenLibrary API. |
| `apps/infraestrutura/` | Patrimônio, manutenções, almoxarifado. |
| `apps/comum/` | Templatetags, utilitários e Design System em `static/core/`. |
| `seed_db.py` | Simulador de 10 anos de dados escolares (2016–2026). |
| `.env` / `.env.example` | Segredos e configurações de ambiente. |
| `.github/workflows/` | Pipeline CI/CD (Lint, Security Scan, Tests, Deploy). |
| `Dockerfile` / `docker-compose.yml` | Orquestração: App + MySQL + Redis + Celery. |
| `SECURITY.md` | Camadas de proteção e auditoria. |
| `PIPELINE.md` | Manual do workflow de CI/CD. |
| `ROADMAP.md` | Roadmap estratégico v2.0 com fases e prioridades. |
| `GAP_ANALYSIS.md` | Análise de gap SIGE vs. SUAP/SIGEDUC com score e esforço. |
| `SEED_INSTRUCTIONS.md` | Guia de uso do simulador de dados. |

---

## 🎨 5. Design System & UI/UX

Interface baseada no sistema **Premium BI**, focada em um estilo vibrante e fluido. 
Os tokens de estilo residem em `apps/comum/static/core/css/design_system/tokens.css`.

### 💠 Princípios do Design System
* **Bordas em 48px**: Todos os botões principais utilizam o estilo de pílula (`border-radius: 48px`), conferindo um aspecto mais amigável.
* **Cores Semânticas**: 
  * `--accent-ruby` (Vermelho) — Destaques médicos urgentes (ex: Alergias no prontuário).
  * `--accent-emerald` (Verde) — Operações financeiras bem-sucedidas (Faturas Pagas).
  * `--accent-blue` (Azul Corporativo) — Foco em ações primárias, garantindo o "Azul Corporativo" histórico da plataforma.
* **Glassmorphism**: Painéis flutuantes (como os cards do aluno) que oferecem transparência para um look contemporâneo.

### 📽️ Animações (`animations.css`)
* Animações modernas baseadas em keyframes leves (`iconFloat`, `diaAtualPulse`, `fadeUp`) implementadas nos painéis do Gestor e Aluno.

---

## 🧪 6. Garantia de Qualidade & DevOps
No GitHub Actions (`.github/workflows/django.yml`), o pipeline é dividido em jobs paralelos para máxima eficiência:

1.  **🔍 Lint & Style**: Executa `flake8` (com regras customizadas) e `pylint` (modo errors-only) para garantir a saúde do código.
2.  **🔒 Security Scan**: Utiliza `bandit` para análise estática de vulnerabilidades e `pip-audit` para verificar dependências conhecidas.
3.  **🧪 Tests & Coverage**: Sobe um container **MySQL 8**, aplica migrações e executa a suíte de testes com `coverage`.
4.  **🚀 CD (Continuous Deployment)**: Se o CI passar na branch `main`, o deploy é disparado via **SSH** para o servidor de produção automaticamente.

**Métricas Atuais:**
- **Status CI:** 🟢 Passing
- **Cobertura:** 📊 53% → Meta: 75%
- **Python:** 3.14 (compatível com 3.11+)
- **Dados de demonstração:** 30.000+ registros via `seed_db.py`

---

## 🛣️ 7. Documentação Estratégica & Roadmap

> O SIGE mantém três documentos estratégicos na raiz do projeto:

| Documento | Conteúdo |
| :--- | :--- |
| [`ROADMAP.md`](ROADMAP.md) | Roadmap v2.0 completo com fases, prioridades e prazo estimado por feature. Inclui bloqueadores antes do 1º cliente real. |
| [`GAP_ANALYSIS.md`](GAP_ANALYSIS.md) | Análise de gap: SIGE vs. SUAP/SIGEDUC. Score de maturidade por módulo (52% → 90%), esforço em sprints e ordem de ataque. |
| [`SEED_INSTRUCTIONS.md`](SEED_INSTRUCTIONS.md) | Guia completo para rodar o simulador de dados de 10 anos. |

### 🏆 Score de Maturidade Atual (vs. Referências de Mercado)

| Módulo | SIGE Hoje | Meta | SUAP |
| :--- | :---: | :---: | :---: |
| UX / Design System | **90%** 🏆 | 95% | 45% |
| Módulo Financeiro (BI) | 60% | 90% | 75% |
| Gestão Acadêmica | 65% | 95% | 98% |
| Documentos & Protocolos | 30% | 85% | 92% |
| Gestão Institucional | 20% | 80% | 95% |
| **TOTAL** | **52%** | **90%** | **78%** |

> O SIGE supera o SUAP em UX e Design System — diferencial competitivo real no segmento privado.

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

3. **O Super Simulador de Dados (Máquina do Tempo de 10 Anos)**
    Para desenvolvedores testarem os limites da UI com gráficos realistas e densos:
    ```bash
    python manage.py migrate
    python seed_db.py
    ```
    > **Aviso:** O `seed_db.py` é extremamente agressivo. Ele realiza um *hard reset* no banco, conecta-se com a **OpenLibrary API** para baixar centenas de capas de livros em HD e roda loops de 2016 a 2026, gerando pagamentos financeiros, folhas de pagamento, alunos evadidos e diários de notas. Espere gerar +30.000 linhas e aguarde alguns minutos para ele processar tudo.

### 🐳 8.1. Rodando com Docker (Recomendado)
Para subir o ambiente completo (App + MySQL + Redis + Celery):
```bash
docker-compose up --build
```
Acesse o sistema em `http://localhost:8000`.

> Se você estiver atualizando um banco existente, garanta que as migrations mais recentes foram aplicadas:
>
> ```bash
> python manage.py migrate
> ```
>
> As migrations recentes incluem:
> - `academico.0003_atividadeprofessor_gabarito_liberacao`
> - `academico.0004_notificacaoaluno`
> - `academico.0009_notificacao_delete_notificacaoaluno`
> - `biblioteca.0004_livro_data_cadastro`

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
```

> Atualizado em 2026 para refletir a documentação atual do projeto e registrar a criação de README adicionais para cada app.

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
