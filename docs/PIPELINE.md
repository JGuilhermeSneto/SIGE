# 🚀 Guia do Pipeline CI/CD — SIGE

Este documento descreve o funcionamento, a arquitetura e as instruções de manutenção do pipeline de Integração e Entrega Contínua (CI/CD) do projeto SIGE, configurado via **GitHub Actions**.

---

## 🏗️ 1. Arquitetura do Workflow

O arquivo de configuração reside em `.github/workflows/django.yml` e é acionado em todo **push** ou **pull request** para a branch `main`.

O workflow é dividido em **4 estágios (jobs)**:

### A. 🔍 Lint & Style (Paralelo)
- **Objetivo**: Garantir que o código segue os padrões de estilo e não possui erros de sintaxe.
- **Ferramentas**: `flake8` e `pylint`.
- **Comportamento**: Falha o build se encontrar erros de sintaxe ou imports indefinidos. Ignora avisos de estilo puramente estéticos (como tamanho de linha) para evitar bloqueios desnecessários.

### B. 🔒 Security Scan (Paralelo)
- **Objetivo**: Identificar vulnerabilidades de segurança no código e dependências.
- **Ferramentas**: `bandit` (análise estática) e `pip-audit` (verificação de CVEs em bibliotecas).
- **Comportamento**: Reporta vulnerabilidades, mas está configurado com `continue-on-error: true` para permitir o fluxo enquanto a equipe revisa os alertas.

### C. 🧪 Tests & Coverage (Depende de 'Lint')
- **Objetivo**: Validar a lógica de negócio e garantir que novas mudanças não quebraram funcionalidades existentes.
- **Ambiente**: Sobe um container real de **MySQL 8.0**.
- **Comportamento**: Executa `python manage.py test`. Gera um relatório de cobertura (`coverage.xml`) que é salvo como artefato do build.

### D. 🚀 Deploy to Production (Depende de 'Lint' e 'Test')
- **Objetivo**: Realizar o deploy automático no servidor de produção.
- **Condição**: Só executa se os jobs anteriores passarem **E** o push for na branch `main`.
- **Método**: SSH direto para o servidor remoto.

---

## 🔐 2. Configuração de Secrets

Para que o **CD (Deploy)** funcione, você deve configurar os seguintes **Secrets** no GitHub (`Settings > Secrets and variables > Actions`):

| Secret | Descrição | Exemplo |
| :--- | :--- | :--- |
| `SSH_HOST` | Endereço IP ou domínio do servidor de produção. | `200.150.x.x` ou `sige.com.br` |
| `SSH_USER` | Usuário com permissão de acesso via SSH. | `ubuntu` ou `deploy` |
| `SSH_PRIVATE_KEY` | Conteúdo da sua chave privada SSH (`id_rsa`). | `-----BEGIN OPENSSH PRIVATE KEY----- ...` |
| `SSH_PORT` | Porta do serviço SSH no servidor (padrão 22). | `22` |
| `DEPLOY_PATH` | Caminho absoluto da pasta do projeto no servidor. | `/var/www/SIGE` |
| `SECRET_KEY` | A Secret Key do Django para o ambiente de produção. | `django-insecure-xxx...` |

---

## 🛠️ 3. Como Rodar as Verificações Localmente

Antes de enviar um commit, você pode rodar os mesmos comandos do pipeline na sua máquina:

```bash
# 1. Lint
flake8 .
pylint apps/ --errors-only

# 2. Segurança
bandit -r apps/
pip-audit

# 3. Testes
python manage.py test
coverage run manage.py test
coverage report -m
```

---

## ❓ 4. Resolução de Problemas Comuns

### O Pipeline falhou no Job de 'Test'
- Verifique se você criou novas migrações e esqueceu de incluí-las no commit.
- O pipeline roda `python manage.py migrate` antes dos testes. Se houver erro de banco, a causa costuma ser migrações inconsistentes.

### O Pipeline falhou no Job de 'Lint'
- O `flake8` está configurado para ser rígido com erros de lógica (`E9`, `F63`, `F7`, `F82`). Corrija-os antes de tentar novamente.

### O Job de 'Deploy' não iniciou
- Verifique se você está na branch `main`. O deploy é restrito a esta branch para garantir a estabilidade da produção.

---

*Documentação atualizada em: 2026-04-22*
