# 🚀 DevOps e CI/CD — SIGE

> **Atualizado:** Maio de 2026

Este documento descreve o pipeline de integração contínua, entrega contínua e práticas de DevOps adotadas no SIGE.

---

## 🔄 1. Pipeline de CI (GitHub Actions)

Toda alteração enviada ao repositório (`push` ou `pull_request` para `main`) dispara automaticamente os seguintes estágios:

```
Código → Lint → Segurança → Testes → Build → Deploy (Render)
```

### Estágios

| Estágio | Ferramenta | O que verifica |
|---|---|---|
| **Lint / Estilo** | Flake8 + MyPy | PEP8 e tipagem estática |
| **Segurança** | Bandit + Pip-audit | Vulnerabilidades no código e dependências |
| **Testes** | Pytest + Coverage | Cobertura mínima de 50% exigida |
| **Deploy** | Render Webhook | Deploy automático após CI verde |

---

## 🐳 2. Docker

O projeto usa Docker para padronizar o ambiente de build em produção.

### Imagem de Produção
```dockerfile
# Build base Python 3.14
# Instala requirements.txt
# collectstatic
# gunicorn config.wsgi
```

Para rodar localmente com Docker:
```bash
docker-compose up --build
```

---

## ☁️ 3. Deploy no Render

O deploy ocorre automaticamente ao fazer push para `main`.

### Fluxo Manual (Emergência)
```bash
git add .
git commit -m "fix: descrição da correção"
git push origin main
```

### Script de Build (`build.sh`)
O Render executa `build.sh` em cada deploy:
```bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

---

## 🔍 4. Checklist de Deploy

Antes de qualquer deploy em produção, valide:
- [ ] Testes passando localmente (`pytest`)
- [ ] Variáveis de ambiente configuradas no painel do Render
- [ ] Migrations geradas e versionadas (`makemigrations`)
- [ ] `DEBUG=False` no ambiente de produção
- [ ] `ALLOWED_HOSTS` atualizado

---

## 🪵 5. Logs e Diagnóstico

- **Logs do Render**: Acessíveis via painel em `Dashboard → Service → Logs`.
- **Sentry**: Exceções capturadas automaticamente e notificadas por e-mail.
- **Health Check TI**: `/ti/operacoes/` → "Executar Health Check".

> [!TIP]
> Em caso de falha de deploy, verifique primeiro os logs do Render e depois rode o Health Check na área de TI do sistema.
