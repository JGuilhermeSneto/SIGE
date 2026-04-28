# 🚀 Guia de Deploy e Configuração — SIGE

Este documento descreve o processo de deploy do SIGE utilizando a infraestrutura de baixo custo (ou gratuita) com **Render** e **Aiven**.

## 🏗️ Arquitetura de Produção/Homologação

*   **App Server:** [Render](https://render.com/) (PaaS)
*   **Database:** [Aiven](https://aiven.io/) (MySQL 8.0)
*   **Storage:** [Cloudinary](https://cloudinary.com/) (Arquivos estáticos e mídia)
*   **Edge:** [WhiteNoise](https://whitenoise.readthedocs.io/) (Serviço de arquivos estáticos via Django)

---

## 1. Configuração do Banco de Dados (Aiven)

1.  Crie um serviço **MySQL** gratuito no Aiven.
2.  Obtenha a **Service URI** (Ex: `mysql://avnadmin:senha@host:port/defaultdb?ssl-mode=REQUIRED`).
3.  **Importante:** Na seção **IP Allowance**, adicione `0.0.0.0/0` para permitir a conexão do Render.

## 2. Deploy no Render (Via Blueprint ou Manual)

### Configurações de Ambiente
Configure as seguintes variáveis de ambiente no painel do Render:

| Chave | Valor |
| :--- | :--- |
| `DATABASE_URL` | Sua Service URI do Aiven |
| `DEBUG` | `False` |
| `SECRET_KEY` | Uma chave aleatória e segura |
| `PYTHON_VERSION` | `3.12.9` |
| `ALLOWED_HOSTS` | `*` ou o seu domínio final |

### Comandos de Build e Start
*   **Build Command:** `./build.sh`
*   **Start Command:** `gunicorn config.wsgi:application`

---

## 3. Comandos Pós-Deploy (Pelo Desenvolvedor)

Como o plano gratuito do Render não oferece Shell interativo, os comandos de manutenção devem ser executados localmente apontando para o banco de dados remoto:

1.  No seu terminal local, configure o ambiente:
    ```powershell
    $env:DATABASE_URL="sua_uri_do_aiven"
    ```
2.  Para criar o primeiro acesso:
    ```bash
    python manage.py createsuperuser
    ```
3.  Para popular o banco com dados de teste:
    ```bash
    python seed_db.py
    ```

---

## 🌐 4. Domínio Personalizado

Para configurar seu próprio domínio no Render:
1.  Vá em **Settings > Custom Domains**.
2.  Adicione seu domínio (ex: `sige.seudominio.com`).
3.  Configure os registros **CNAME** e **A** no seu provedor de DNS conforme as instruções do Render.
4.  O Render gerará o certificado SSL (HTTPS) automaticamente.

---

## 🛠️ Manutenção

*   **Logs:** Acompanhe os logs em tempo real pelo dashboard do Render.
*   **Migrações:** São executadas automaticamente a cada novo deploy via `build.sh`.
*   **Arquivos Estáticos:** O comando `collectstatic` é executado no build e servido pelo WhiteNoise.
