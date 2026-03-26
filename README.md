<div align="center">

# 🏫 SIGE
### Sistema Integrado de Gestão Escolar

<br/>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.x-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![Flake8](https://img.shields.io/badge/Flake8-10.00%2F10-brightgreen?style=for-the-badge)
![MyPy](https://img.shields.io/badge/MyPy-typed-blue?style=for-the-badge)
![License](https://img.shields.io/badge/Licença-MIT-yellow?style=for-the-badge)

<br/>

> **SIGE** é um sistema web completo para gestão escolar, desenvolvido com **Django** e focado em qualidade de código, cobertura de testes e entrega contínua via **GitHub Actions**.

<br/>

[🚀 Instalação](#-instalação-passo-a-passo) · [📂 Estrutura](#-estrutura-do-projeto) · [🧪 Testes](#-testes-e-qualidade-de-código) · [🔄 CI/CD](#-cicd--github-actions) · [📖 Referências](#-referências)

</div>

---

## 📌 Sobre o Projeto

O **SIGE** (Sistema Integrado de Gestão Escolar) é uma aplicação web construída para facilitar a administração de uma instituição de ensino. Ele centraliza o gerenciamento de **alunos**, **professores**, **turmas**, **disciplinas**, **notas** e **usuários** em um único sistema, com controle de acesso por perfis (Super Admin, Gestor, Professor e Aluno).

### ✨ Principais funcionalidades

| Módulo | Descrição |
|---|---|
| 🔐 **Autenticação** | Login, logout e reset de senha por e-mail |
| 👤 **Perfis de Acesso** | Super Admin, Gestor, Professor e Aluno |
| 🎓 **Gestão de Alunos** | Cadastro, edição, exclusão e listagem |
| 👨‍🏫 **Gestão de Professores** | Cadastro com área de atuação, edição e exclusão |
| 🏛️ **Gestão de Turmas** | Criação de turmas com grade horária |
| 📚 **Gestão de Disciplinas** | Disciplinas vinculadas a turmas e professores |
| 📝 **Lançamento de Notas** | Professores lançam notas por disciplina |
| 🗂️ **Gestão de Gestores** | Cadastro e controle de gestores institucionais |
| 🖼️ **Foto de Perfil** | Upload e remoção de foto de perfil |
| 📊 **Painéis por perfil** | Painel personalizado para cada tipo de usuário |

---

## 🛠️ Tecnologias Utilizadas

```
SIGE usa um stack moderno e bem definido para garantir qualidade e manutenibilidade.
```

| Camada | Tecnologia | Versão | Finalidade |
|---|---|---|---|
| Linguagem | Python | 3.11 | Backend |
| Framework | Django | 4.x | MVC / ORM / Auth |
| Banco de Dados | PostgreSQL / MySQL | — | Persistência |
| Front-end | HTML + CSS + JavaScript | — | Interface do usuário |
| Linting de estilo | Flake8 | latest | Conformidade com PEP8 |
| Análise de qualidade | Pylint | latest | Métricas de código |
| Tipagem estática | Mypy + django-stubs | latest | Checagem de tipos |
| Testes | Pytest / Django TestCase | — | Unitários e integração |
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
│   │   ├── get_item.py
│   │   ├── dict_get.py
│   │   └── custom_tags.py
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
├── .github/
│   └── workflows/               # 🔄 Pipelines de CI/CD
│
├── manage.py                    # CLI do Django
├── requirements.txt             # Dependências do projeto
├── pyproject.toml               # Configuração de ferramentas (mypy, etc.)
└── README.md                    # Documentação
```

---

## 🔐 Perfis de Acesso

O SIGE possui quatro níveis de acesso com permissões distintas:

```
┌─────────────────────────────────────────────────────────┐
│                     HIERARQUIA DE ACESSO                │
│                                                         │
│   👑 Super Admin  →  Acesso total ao sistema            │
│   🏛️  Gestor       →  Gerencia turmas, alunos e profs.  │
│   👨‍🏫 Professor    →  Lança notas e visualiza turmas     │
│   🎓 Aluno        →  Consulta notas e grade horária     │
└─────────────────────────────────────────────────────────┘
```

---

## 🧪 Testes e Qualidade de Código

O projeto mantém um padrão rigoroso de qualidade. Todos os comandos abaixo podem ser executados localmente ou são disparados automaticamente no CI/CD.

```bash
# Executa todos os testes Django
python manage.py test

# Verifica conformidade com PEP8 (nota atual: 10.00/10 ✅)
flake8 .

# Análise estática de qualidade
pylint **/*.py

# Verificação de tipos estáticos
mypy .
```

> 💡 **Dica:** Sempre rode `flake8 .` e `mypy .` antes de qualquer commit para evitar falhas no pipeline.

---

## 🔄 CI/CD — GitHub Actions

A cada `push` ou `pull request` para a branch `main`, o pipeline é ativado automaticamente:

```
┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐
│  git push  │────▶│  flake8 .  │────▶│  mypy .    │────▶│  pytest    │
└────────────┘     └────────────┘     └────────────┘     └────────────┘
                        ✅ PEP8            ✅ Tipos          ✅ Testes
                        
                   Se qualquer etapa falhar → ❌ merge bloqueado
```

Os workflows ficam em `.github/workflows/` e garantem que nenhum código com erros seja integrado à branch principal.

---

## 🚀 Instalação — Passo a Passo

### Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- [PostgreSQL](https://www.postgresql.org/) (ou MySQL)

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

Para as ferramentas de desenvolvimento (linting, tipagem):

```bash
pip install flake8 pylint mypy django-stubs
```

---

### 4️⃣ Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Banco de dados
DB_ENGINE=django.db.backends.postgresql
DB_NAME=sige_db
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
```

---

### 5️⃣ Configure o banco de dados

Abra `notas/settings.py` e ajuste o bloco `DATABASES`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # ou mysql
        'NAME': 'sige_db',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',  # MySQL: '3306'
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
| `flake8 .` | Verifica estilo PEP8 |
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
- 🔬 [Pylint Docs](https://pylint.pycqa.org/en/latest/)
- 🔷 [MyPy Docs](https://mypy.readthedocs.io/en/stable/)
- ⚙️ [GitHub Actions Docs](https://docs.github.com/en/actions)
- 🐘 [PostgreSQL Docs](https://www.postgresql.org/docs/)

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
