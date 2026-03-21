# 🗄️ Configuração do Banco de Dados — Ambiente IF (SIGE_IF)

Este documento descreve como **instalar as dependências**, **criar o banco de dados** e **conectar o projeto SIGE ao MySQL no ambiente do IF**, utilizando **:contentReference[oaicite:0]{index=0}** e **:contentReference[oaicite:1]{index=1}**.

---

## 📦 Instalação das Dependências

Com o ambiente virtual ativado, execute:

```bash
pip install -r requirements.txt

Isso instalará todas as bibliotecas necessárias para o funcionamento do projeto.

🧠 Observação Importante
O MySQL já está instalado no ambiente do IF
Cada aluno utiliza seu próprio banco de dados
Cada aluno possui seu próprio usuário local
O banco não é remoto e não é compartilhado
🗄️ Criação do Banco de Dados e Usuário

No MySQL Workbench ou no terminal MySQL, execute:

CREATE DATABASE SIGE_BANCO
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;

CREATE USER 'sige_user'@'localhost'
  IDENTIFIED BY '123456';

GRANT ALL PRIVILEGES ON SIGE_BANCO.* TO 'sige_user'@'localhost';
FLUSH PRIVILEGES;

📌 O nome do banco e do usuário podem ser alterados, desde que a alteração seja refletida no arquivo settings.py.

⚙️ Configuração do settings.py

No arquivo settings.py do projeto, configure a conexão com o banco:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'SIGE_BANCO',
        'USER': 'sige_user',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
🔄 Criação das Tabelas do Projeto

Execute as migrations do Django:

python manage.py makemigrations
python manage.py migrate

✔️ As tabelas serão criadas automaticamente no banco local.

▶️ Execução do Projeto

Inicie o servidor de desenvolvimento:

python manage.py runserver

Acesse no navegador:

http://127.0.0.1:8000
👀 Verificação no MySQL Workbench

Para confirmar que o banco está sendo atualizado corretamente:

SHOW TABLES;
SELECT * FROM nome_da_tabela;

📌 As alterações feitas no Django refletem automaticamente no banco de dados.
