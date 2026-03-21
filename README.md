# 🏫 SIGE - Sistema de Gestão Escolar

![Banner](https://img.shields.io/badge/Django-4.x-green) ![Python](https://img.shields.io/badge/Python-3.11-blue) ![CI/CD](https://img.shields.io/badge/CI/CD-GitHub%20Actions-yellow)

O **SIGE** é um sistema completo de gestão escolar desenvolvido em **Django**, com foco em **qualidade de código**, **testes automatizados** e **integração contínua (CI/CD)**.

Este README serve como guia completo para configurar, desenvolver, testar e manter o projeto.

---

## 🌐 Tecnologias e Bibliotecas

| Categoria           | Tecnologias/Bibliotecas | Função                               |
|--------------------|-----------------------|-------------------------------------|
| Linguagem           | Python 3.11           | Backend                              |
| Framework           | Django 4.x            | Estrutura MVC                        |
| Banco de Dados      | PostgreSQL / MySQL    | Armazenamento de dados               |
| Front-end           | HTML, CSS, Bootstrap  | Interface do usuário                 |
| Testes              | `pytest`, `unittest`  | Testes unitários e integração        |
| Linting             | `flake8`, `pylint`    | Verificação de estilo e qualidade    |
| Tipagem             | `mypy`                | Verificação estática de tipos        |
| Controle de Versão  | Git, GitHub           | Versionamento de código              |
| CI/CD               | GitHub Actions        | Workflow automático                  |

---

## 📂 Estrutura do Projeto

```text
SIGE/
├─ core/                   # Aplicação principal
│  ├─ admin.py             # Registro de models no admin
│  ├─ forms.py             # Formulários do Django
│  ├─ models.py            # Models (Banco de Dados)
│  ├─ views.py             # Views e lógica de negócio
│  ├─ urls.py              # Rotas da aplicação
│  ├─ templatetags/        # Tags customizadas do Django
│  └─ tests.py             # Testes unitários
├─ notas/                  # Configurações do Django
│  ├─ settings.py          # Configurações do projeto
│  ├─ urls.py              # URLs globais
│  └─ wsgi.py              # Servidor WSGI
├─ migrations/             # Migrations do banco
├─ requirements.txt        # Dependências do projeto
└─ README.md               # Documentação
```



## ⚙️ Configuração do Ambiente
1️⃣ Clonar o repositório
```
git clone https://github.com/SEU_USUARIO/SIGE.git
cd SIGE
```

## 2️⃣ Criar ambiente virtual
# Linux / macOS

```
python -m venv venv
source venv/bin/activate
```
# Windows
```
python -m venv venv
venv\Scripts\activate
```

## 3️⃣ Instalar dependências
```
pip install -r requirements.txt
```

## 4️⃣ Configurar banco de dados

Abra settings.py e configure PostgreSQL ou MySQL:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # ou mysql
        'NAME': 'nome_do_banco',
        'USER': 'usuario',
        'PASSWORD': 'senha',
        'HOST': 'localhost',
        'PORT': '5432',  # ou 3306 para MySQL
    }
}
```

## 5️⃣ Criar migrations e aplicar no banco
```
python manage.py makemigrations
python manage.py migrate
```


## 6️⃣ Criar superusuário Django
```
python manage.py createsuperuser
```
## 7️⃣ Rodar servidor local

```
python manage.py runserver
```
Acesse http://127.0.0.1:8000/
 para testar o projeto.

 
## 🧪 Testes e Comandos Úteis

Todos os comandos podem ser executados **localmente no terminal** ou **automaticamente pelo workflow do GitHub Actions**.

| Comando                  | Função                           | Onde Executar       |
|--------------------------|---------------------------------|------------------|
| `python manage.py test`  | Executa todos os testes Django  | Local / Workflow CI |
| `flake8 .`               | Verifica estilo PEP8            | Local / Workflow CI |
| `pylint **/*.py`         | Análise de qualidade do código  | Local / Workflow CI |
| `mypy .`                 | Checagem de tipos estáticos     | Local / Workflow CI |

## 💡 Dicas:

Sempre rode flake8 e pylint antes de commitar.
Testes locais ajudam a detectar problemas antes do CI.

## ⚡ Git e GitHub

| Comando | Função |
|---------|--------|
| `git status` | Verifica alterações não commitadas |
| `git add .` | Adiciona alterações para commit |
| `git commit -m "mensagem"` | Cria commit com mensagem |
| `git push origin main` | Envia alterações para GitHub |
| `git pull` | Atualiza branch local com remoto |


## 🔄 Workflow CI/CD - GitHub Actions
Sempre que uma branch é atualizada ou um pull request é criado, o workflow é ativado.
O workflow executa:
```
flake8 .          # Validação de estilo
pylint **/*.py    # Qualidade do código
mypy .            # Checagem de tipos
python manage.py test  # Execução de testes Django
```
Se algum comando falhar, o workflow marca como failed no GitHub, impedindo merge até corrigir.

Visualização do Workflow:
```
Push / PR → GitHub Actions → Linting & Tests → Status OK / Failed
```

## 📖 Referências

- [Django Documentation](https://docs.djangoproject.com/)
- [Flake8](https://flake8.pycqa.org/en/latest/)
- [Pylint](https://pylint.pycqa.org/en/latest/)
- [MyPy](https://mypy.readthedocs.io/en/stable/)
- [GitHub Actions](https://docs.github.com/en/actions)
