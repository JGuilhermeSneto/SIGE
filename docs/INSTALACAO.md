# 🛠️ Guia de Instalação — SIGE

> Sistema Integrado de Gestão Escolar — Ambiente de Desenvolvimento

Este documento descreve o processo completo para configurar o ambiente local, instalar dependências, configurar o banco de dados e popular o sistema com dados iniciais.

---

## ✅ Pré-requisitos

| Ferramenta | Versão mínima |
|---|---|
| Python | 3.12+ |
| pip | Atualizado |
| MySQL (Opcional) | 8.0+ |
| Git | Qualquer |

---

## 📦 1. Clonando o Repositório

```bash
git clone https://github.com/JGuilhermeSneto/SIGE.git
cd SIGE
```

---

## 🐍 2. Criando e Ativando o Ambiente Virtual

```bash
# Criar
python -m venv venv

# Ativar — Windows
venv\Scripts\activate

# Ativar — Linux / macOS
source venv/bin/activate
```

---

## 📦 3. Instalando as Dependências

```bash
pip install -r requirements.txt
```

---

## ⚙️ 4. Configurando o Ambiente (`.env`)

Copie o arquivo de exemplo e preencha com seus dados:

```bash
cp .env.example .env
```

**Variáveis mínimas para desenvolvimento:**
```env
SECRET_KEY=django-insecure-troque-isso-em-producao
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

---

## 🗄️ 5. Configurando o Banco de Dados

### Opção A — SQLite (padrão, mais simples)
Não requer configuração extra. O SQLite é criado automaticamente.

### Opção B — MySQL Local
No MySQL Workbench ou terminal, execute:
```sql
CREATE DATABASE SIGE_BANCO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
CREATE USER 'sige_user'@'localhost' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON SIGE_BANCO.* TO 'sige_user'@'localhost';
FLUSH PRIVILEGES;
```

Configure o `.env`:
```env
DATABASE_URL=mysql://sige_user:123456@localhost:3306/SIGE_BANCO
```

---

## 🔄 6. Aplicando Migrações

```bash
python manage.py migrate
```

---

## 👤 7. Criando Superusuário

```bash
python manage.py createsuperuser
```

---

## 🌱 8. Populando o Banco com Dados de Teste

O script `seed_db.py` cria usuários, turmas, disciplinas e faturas para demonstração:

```bash
python seed_db.py
```

**Credenciais criadas (senha: `admin123`):**
| Perfil | Login |
|---|---|
| Gestor | `gestor` |
| Professor | `professor1`, `professor2` |
| Aluno | `aluno1`, `aluno2`, `aluno3` |

---

## ▶️ 9. Iniciando o Servidor de Desenvolvimento

```bash
python manage.py runserver
```

Acesse em: **http://127.0.0.1:8000**

---

## ☁️ 10. Populando o Banco de Produção (Render/Aiven)

Para popular o banco remoto a partir do terminal local:

```powershell
# Windows PowerShell
$env:DATABASE_URL = "sua_url_do_aiven"
python seed_db.py
```

---

> [!WARNING]
> Nunca use os dados de exemplo (`seed_db.py`) em produção com usuários reais. Limpe o banco antes de ativar o sistema para uso real.
