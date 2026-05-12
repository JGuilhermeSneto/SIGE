# 🏗️ Infraestrutura — SIGE

> **Atualizado:** Maio de 2026

Este documento descreve a infraestrutura de cloud, armazenamento, cache e mensageria que sustenta o ecossistema SIGE em produção.

---

## ☁️ 1. Cloud e Hospedagem

O SIGE roda em ambiente **Render** com containers Docker.

| Componente | Tecnologia | Observação |
|---|---|---|
| **Runtime** | Render (Docker) | Região US para menor latência |
| **Banco de Dados** | MySQL via Aiven | SSL/TLS obrigatório |
| **Mídia/Uploads** | Cloudinary CDN | Fotos de perfil e documentos |
| **Assets Estáticos** | WhiteNoise | Servido via Django em produção |

---

## 🗄️ 2. Banco de Dados

- **Produção**: MySQL (Aiven Cloud) com `ssl-mode=REQUIRED`.
- **Desenvolvimento**: SQLite (padrão) ou MySQL local.
- **ORM**: Django ORM com queries otimizadas (`select_related`, `prefetch_related`).

### Configuração via `.env`
```
DATABASE_URL=mysql://usuario:senha@host:3306/SIGE_BANCO
```

---

## ⚡ 3. Cache

O sistema usa Redis quando disponível, com fallback automático para `LocMemCache`:

```python
# Redis (produção)
USE_REDIS=True
REDIS_URL=redis://...

# Fallback local (sem Redis)
USE_REDIS=False
```

Vistas com cache ativo:
- `painel_ti` — 5 minutos
- Dashboards de alto custo — configurável

---

## 📨 4. Mensageria (Celery + RabbitMQ)

Tarefas assíncronas são processadas via **Celery** com broker **RabbitMQ**:
- Envio de e-mails de notificação
- Geração de PDFs (histórico escolar, boletos)
- Sincronização com sistemas externos

```
CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//
```

---

## 📊 5. Monitoramento e Observabilidade

| Ferramenta | Papel |
|---|---|
| **Prometheus** | Coleta de métricas de runtime |
| **Grafana** | Visualização de dashboards em tempo real |
| **Sentry** | Captura e alerta de exceções em produção |
| **django_prometheus** | Exposição de métricas Django via `/metrics/` |

---

## 🌐 6. Variáveis de Ambiente Essenciais

```env
SECRET_KEY=...
DEBUG=False
ALLOWED_HOSTS=meudominio.com
DATABASE_URL=...
CLOUDINARY_CLOUD_NAME=...
REDIS_URL=...
SENTRY_DSN=...
USE_REDIS=True
```

---

## 📡 7. WebSockets (Django Channels)

O SIGE suporta comunicação em tempo real via WebSocket para o painel de TI:
- **Protocolo:** ASGI (via `daphne`)
- **Layer:** Redis (produção) / InMemory (desenvolvimento)
- **Canal:** `ti_notificacoes` — notifica a equipe de TI sobre novos bugs e erros em tempo real

Para rodar com suporte a WebSocket em dev:
```bash
daphne -p 8000 config.asgi:application
```

---

## 🩺 8. Health Check

Endpoint padronizado para monitoramento externo (Render, UptimeRobot, etc.):
```
GET /health/
```
Verifica: Banco de Dados · Cache · Storage · Migrações pendentes

> [!WARNING]
> Nunca versione o `.env` com segredos reais. Use as variáveis de ambiente no painel do Render.

