<div align="center">

# 🏫 SIGE
### Sistema Integrado de Gestão Escolar — Em progresso...

<br/>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![Flake8](https://img.shields.io/badge/Flake8-10.00%2F10-brightgreen?style=for-the-badge)
![MyPy](https://img.shields.io/badge/MyPy-typed-blue?style=for-the-badge)
![Coverage](https://img.shields.io/badge/Coverage-coverage.py-orange?style=for-the-badge)
![License](https://img.shields.io/badge/Licença-MIT-yellow?style=for-the-badge)

<br/>

> **SIGE** é um sistema web completo para gestão escolar, desenvolvido com **Django** e focado em qualidade de código, cobertura de testes e entrega contínua via **GitHub Actions**.

<br/>

[🚀 Instalação](#-instalação-passo-a-passo) · [📂 Estrutura](#-estrutura-do-projeto) · [🧪 Testes](#-testes-e-qualidade-de-código) · [🔄 CI/CD](#-cicd--github-actions) · [📖 Referências](#-referências)

</div>

---

## 📌 Sobre o Projeto

O **SIGE** (Sistema Integrado de Gestão Escolar) é uma aplicação web construída para facilitar a administração de uma instituição de ensino. Ele centraliza o gerenciamento de **alunos**, **professores**, **turmas**, **disciplinas**, **notas**, **frequência** e **usuários** em um único sistema, com controle de acesso por perfis (Super Admin, Gestor, Professor e Aluno).

### ✨ Principais funcionalidades

| Módulo | Descrição |
|---|---|
| 🔐 **Autenticação** | Login, logout e reset de senha por e-mail |
| 👤 **Perfis de Acesso** | Super Admin, Gestor, Professor e Aluno |
| 🎓 **Gestão de Alunos** | Cadastro, edição, exclusão e listagem |
| 👨‍🏫 **Gestão de Professores** | Cadastro com área de atuação, edição e exclusão |
| 🏛️ **Gestão de Turmas** | Criação de turmas com grade horária por turno |
| 📚 **Gestão de Disciplinas** | Disciplinas vinculadas a turmas e professores |
| 📝 **Lançamento de Notas** | Professores e gestores lançam notas por bimestre |
| ✅ **Frequência** | Chamada diária por disciplina com histórico e percentual de presença |
| 🗂️ **Gestão de Gestores** | Cadastro e controle de gestores institucionais com cargos |
| 🖼️ **Foto de Perfil** | Upload e remoção de foto de perfil |
| 📊 **Painéis por perfil** | Painel personalizado para cada tipo de usuário |
| 📅 **Grade Horária** | Configuração visual da grade por turma e turno |
| 📄 **Relatórios** | Geração de relatórios em PDF com ReportLab |

---

## 🛠️ Tecnologias Utilizadas

```
SIGE usa um stack moderno e bem definido para garantir qualidade e manutenção.
```

| Camada | Tecnologia | Versão | Finalidade |
|---|---|---|---|
| Linguagem | Python | 3.11 | Backend |
| Framework | Django | 5.2.12 | MVC / ORM / Auth |
| Banco de Dados | MySQL | 8.0 | Persistência |
| Driver MySQL | mysqlclient | 2.2.8 | Conexão com o banco |
| Front-end | HTML + CSS + JavaScript | — | Interface do usuário |
| Imagens | Pillow | 12.1.1 | Upload de fotos de perfil |
| PDF | ReportLab | 4.4.10 | Geração de relatórios |
| Variáveis de ambiente | python-decouple / python-dotenv | 3.8 / 1.2.2 | Configuração segura |
| Linting de estilo | Flake8 | 7.3.0 | Conformidade com PEP8 |
| Formatação | Black | 26.3.1 | Formatação automática de código |
| Ordenação de imports | isort | 8.0.1 | Organização de imports |
| Análise de qualidade | Pylint + pylint-django | 4.0.5 | Métricas de código |
| Tipagem estática | Mypy + django-stubs | 6.0.1 | Checagem de tipos |
| Cobertura de testes | coverage.py | 7.13.5 | Relatório de cobertura |
| CI/CD | GitHub Actions | — | Automação de pipeline |
| Controle de versão | Git + GitHub | — | Versionamento |

---

## 📂 Estrutura do Projeto

```
SIGE/
│
├── core/                        # 🔑 Aplicação principal do sistema
│   ├── migrations/              # Histórico de alterações no banco
│   ├── templatetags/            # Tags customizadas para templates
│   │   ├── get_item.py          # Filtro para acessar dicts por chave
│   │   ├── dict_get.py          # Filtro auxiliar de dicionários
│   │   └── custom_tags.py       # Tags gerais (has_attr, etc.)
│   ├── templates/               # Templates HTML organizados por módulo
│   │   ├── auth/                # Login, logout, reset de senha
│   │   ├── core/                # Base, perfil, grade horária, usuários
│   │   ├── aluno/               # Painel e CRUD de alunos
│   │   ├── professor/           # Painel, disciplinas e lançamento de notas
│   │   ├── gestor/              # CRUD de gestores
│   │   ├── turma/               # CRUD de turmas
│   │   ├── disciplina/          # CRUD e visualização de disciplinas
│   │   ├── superusuario/        # Painel do super admin
│   │   └── frequencia/          # Chamada, histórico e frequência do aluno
│   ├── admin.py                 # Registro de models no painel admin
│   ├── apps.py                  # Configuração do app
│   ├── forms.py                 # Formulários Django
│   ├── models.py                # Models (entidades do banco)
│   ├── urls.py                  # Rotas do app core
│   └── views.py                 # Lógica de negócio e views
│
├── notas/                       # ⚙️ Configurações globais do projeto
│   ├── settings.py              # Configurações gerais
│   ├── urls.py                  # Roteamento global
│   ├── wsgi.py                  # Entry point WSGI (produção)
│   └── asgi.py                  # Entry point ASGI (async)
│
├── fotos/                       # 📁 Uploads de fotos de perfil
│
├── .github/
│   └── workflows/               # 🔄 Pipelines de CI/CD
│
├── .coveragerc                  # Configuração de cobertura de testes
├── .flake8                      # Configuração do Flake8
├── .pylintrc                    # Configuração do Pylint
├── manage.py                    # CLI do Django
├── requirements.txt             # Dependências do projeto
├── pyproject.toml               # Configuração de ferramentas (mypy, black, isort)
├── instruções.md                # Guia interno de contribuição
└── README.md                    # Documentação
```

---

## 🔐 Perfis de Acesso

O SIGE possui quatro níveis de acesso com permissões distintas:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        HIERARQUIA DE ACESSO                         │
│                                                                     │
│   👑 Super Admin  →  Acesso total ao sistema                        │
│   🏛️  Gestor       →  Gerencia turmas, alunos, professores e notas  │
│   👨‍🏫 Professor    →  Lança notas, chamada e visualiza suas turmas   │
│   🎓 Aluno        →  Consulta notas, frequência e grade horária     │
└─────────────────────────────────────────────────────────────────────┘
```

### Permissões detalhadas por perfil

| Funcionalidade | Super Admin | Gestor | Professor | Aluno |
|---|:---:|:---:|:---:|:---:|
| Painel de controle | ✅ | ✅ | ✅ | ✅ |
| Gerenciar alunos | ✅ | ✅ | ❌ | ❌ |
| Gerenciar professores | ✅ | ✅ | ❌ | ❌ |
| Gerenciar turmas | ✅ | ✅ | ❌ | ❌ |
| Gerenciar disciplinas | ✅ | ✅ | ❌ | ❌ |
| Gerenciar gestores | ✅ | ❌ | ❌ | ❌ |
| Lançar notas | ✅ | ✅ | ✅ | ❌ |
| Lançar chamada | ❌ | ❌ | ✅ | ❌ |
| Ver histórico de frequência | ✅ | ✅ | ✅ | ❌ |
| Ver própria frequência | ❌ | ❌ | ❌ | ✅ |
| Editar grade horária | ✅ | ✅ | ❌ | ❌ |
| Editar perfil próprio | ✅ | ✅ | ✅ | ✅ |

---

## 🧪 Testes e Qualidade de Código

O projeto mantém um padrão rigoroso de qualidade. Todos os comandos abaixo podem ser executados localmente ou são disparados automaticamente no CI/CD.

```bash
# Executa todos os testes Django
python manage.py test

# Executa testes com relatório de cobertura
coverage run manage.py test
coverage report
coverage html  # gera relatório em HTML

# Verifica conformidade com PEP8 (nota atual: 10.00/10 ✅)
flake8 .

# Formata o código automaticamente
black .

# Organiza os imports
isort .

# Análise estática de qualidade
pylint **/*.py

# Verificação de tipos estáticos
mypy .
```

> 💡 **Dica:** Sempre rode `flake8 .`, `black .` e `mypy .` antes de qualquer commit para evitar falhas no pipeline.

---

## 🔄 CI/CD — GitHub Actions

A cada `push` ou `pull request` para a branch `main`, o pipeline é ativado automaticamente:

```
┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐
│  git push  │────▶│  flake8 .  │────▶│  mypy .    │────▶│  pylint    │────▶│  coverage  │
└────────────┘     └────────────┘     └────────────┘     └────────────┘     └────────────┘
                        ✅ PEP8            ✅ Tipos         ✅ Qualidade       ✅ Cobertura

                   Se qualquer etapa falhar → ❌ merge bloqueado
```

Os workflows ficam em `.github/workflows/` e garantem que nenhum código com erros seja integrado à branch principal.

---

## 🚀 Instalação — Passo a Passo

### Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- [MySQL 8.0+](https://dev.mysql.com/downloads/) (ou MariaDB)

---

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/JGuilhermeSneto/SIGE.git
cd SIGE
```

---

### 2️⃣ Crie e ative o ambiente virtual

**Linux / macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

O `requirements.txt` já inclui todas as dependências de produção e desenvolvimento:

```
Django==5.2.12          # Framework principal
mysqlclient==2.2.8      # Driver do banco de dados
Pillow==12.1.1           # Upload de imagens
reportlab==4.4.10        # Geração de PDFs
python-decouple==3.8     # Variáveis de ambiente
python-dotenv==1.2.2     # Leitura do .env
coverage==7.13.5         # Cobertura de testes
flake8==7.3.0            # Linting PEP8
black==26.3.1            # Formatação de código
isort==8.0.1             # Organização de imports
pylint==4.0.5            # Análise de qualidade
pylint-django==2.7.0     # Plugin Django para Pylint
mypy==*                  # Tipagem estática
django-stubs==6.0.1      # Stubs de tipos para Django
```

---

### 4️⃣ Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Banco de dados
DB_ENGINE=django.db.backends.mysql
DB_NAME=sige_db
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=3306
```

---

### 5️⃣ Configure o banco de dados

Abra `notas/settings.py` e ajuste o bloco `DATABASES`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sige_db',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---

### 6️⃣ Execute as migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 7️⃣ Crie o superusuário

```bash
python manage.py createsuperuser
```

> Siga as instruções no terminal para definir nome de usuário, e-mail e senha.

---

### 8️⃣ Inicie o servidor de desenvolvimento

```bash
python manage.py runserver
```

Acesse no navegador: **http://127.0.0.1:8000/login/**

O painel administrativo está disponível em: **http://127.0.0.1:8000/admin/**

---

## 📋 Comandos Úteis

| Comando | Descrição |
|---|---|
| `python manage.py runserver` | Inicia o servidor local |
| `python manage.py makemigrations` | Gera novas migrations |
| `python manage.py migrate` | Aplica migrations no banco |
| `python manage.py createsuperuser` | Cria usuário administrador |
| `python manage.py test` | Executa os testes |
| `coverage run manage.py test` | Testes com medição de cobertura |
| `coverage report` | Exibe relatório de cobertura no terminal |
| `coverage html` | Gera relatório de cobertura em HTML |
| `flake8 .` | Verifica estilo PEP8 |
| `black .` | Formata o código automaticamente |
| `isort .` | Organiza os imports |
| `mypy .` | Checa tipos estáticos |
| `pylint **/*.py` | Analisa qualidade do código |

---

## 🔗 Git — Fluxo de Trabalho

```bash
git status                        # Verifica arquivos alterados
git add .                         # Adiciona tudo ao stage
git commit -m "feat: descrição"   # Commita com mensagem clara
git push origin main              # Envia para o GitHub
git pull                          # Atualiza branch local
```

> 💡 Use mensagens de commit no padrão [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `refactor:`, etc.

---

## 📖 Referências

- 📘 [Django Documentation](https://docs.djangoproject.com/)
- 🔍 [Flake8 Docs](https://flake8.pycqa.org/en/latest/)
- 🖤 [Black Docs](https://black.readthedocs.io/en/stable/)
- 🔬 [Pylint Docs](https://pylint.pycqa.org/en/latest/)
- 🔷 [MyPy Docs](https://mypy.readthedocs.io/en/stable/)
- 📊 [Coverage.py Docs](https://coverage.readthedocs.io/)
- 📄 [ReportLab Docs](https://docs.reportlab.com/)
- ⚙️ [GitHub Actions Docs](https://docs.github.com/en/actions)
- 🐬 [MySQL Docs](https://dev.mysql.com/doc/)

---

## 🎓 Autores

Este projeto foi desenvolvido com dedicação por:

| | Nome |
|---|---|
| 👤 | **Suanderson Santos Silva** |
| 👤 | **João Batista do Nascimento Júnior** |
| 👤 | **José Guilherme da Silva Neto** |
| 👤 | **Israel Cipriano Ribeiro Filho** |
| 👤 | **Pedro Henrique de Oliveira Querino** |
| 👤 | **Vanessa Gonçalves** |

---

<div align="center">

Fork de [Henrriks/SIGE](https://github.com/Henrriks/SIGE) · Desenvolvido com ❤️ por seus autores

</div>
