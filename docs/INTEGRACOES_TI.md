# 🔌 Novas Integrações da Área de TI

> **Implementado:** Maio de 2026

Este documento descreve as três novas bibliotecas integradas ao SIGE para potencializar a Área de TI.

---

## 1. 🩺 django-health-check — Health Checks Reais

**Pacote:** `django-health-check>=3.18.1`

Transforma o Health Check do painel de TI de uma verificação simulada em um diagnóstico real e padronizado, exposto via endpoint HTTP.

### O que verifica
| Checagem | Classe | Descrição |
|---|---|---|
| **Banco de Dados** | `DatabaseBackend` | Executa um `SELECT 1` no DB principal |
| **Cache** | `CacheBackend` | Lê e escreve no Redis/LocMemCache |
| **Armazenamento** | `DefaultFileStorageHealthCheck` | Escreve e apaga um arquivo temporário |
| **Espaço em Disco** | `DiskUsage` | Alerta se disco > 90% |
| **Memória** | `MemoryUsage` | Alerta se RAM > 80% |
| **Celery** | `CeleryHealthCheck` | Verifica se workers estão online |

### Endpoint
```
GET /health/  →  JSON com status de cada checagem
```

### Como usar no painel de TI
O painel em `/ti/` consome este endpoint via JavaScript para exibir o status em tempo real nos cards de métricas.

---

## 2. 📡 Django Channels — WebSockets em Tempo Real

**Pacotes:** `channels>=4.2.0`, `channels-redis>=4.2.0`, `daphne>=4.1.0`

Permite comunicação bidirecional em tempo real entre o servidor Django e o painel de TI via WebSocket. Quando um novo bug é reportado ou um erro crítico acontece, a notificação aparece automaticamente no painel — sem necessidade de refresh da página.

### Arquitetura
```
Usuário reporta bug
       ↓
  Django View salva BugReport
       ↓
  channel_layer.group_send("ti_sala")
       ↓
  TIConsumer envia WebSocket ao painel
       ↓
  JavaScript atualiza o card de "Bugs Novos"
```

### Canal de Notificações TI
- **Grupo:** `ti_notificacoes`
- **Consumer:** `apps/ti/consumers.py → TINotificacoesConsumer`
- **URL WebSocket:** `ws://host/ws/ti/`

---

## 3. 🌸 Flower — Dashboard de Monitoramento do Celery

**Pacote:** `flower>=2.0.1`

Interface web para monitorar as filas e tarefas Celery em tempo real.

### Como iniciar
```bash
# Com RabbitMQ
celery -A config flower --port=5555

# Com Redis
celery -A config flower --broker=redis://localhost:6379/0 --port=5555
```

### Acessar
```
http://localhost:5555
```

### O que monitora
- Tarefas em execução, pendentes e falhas
- Histórico de execuções com tempo e resultado
- Workers online e capacidade de processamento
- Gráficos de throughput e latência

> [!TIP]
> Em produção, proteja o Flower com autenticação básica via `--basic_auth=usuario:senha`.

---

## 🔗 Resumo de URLs Adicionadas

| URL | Descrição | Acesso |
|---|---|---|
| `/health/` | Health Check JSON (django-health-check) | Público / Monitoring |
| `/ws/ti/` | WebSocket para notificações TI (Channels) | Autenticado |
| `porta :5555` | Dashboard Flower (Celery) | Equipe TI (externo) |
