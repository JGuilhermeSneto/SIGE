# 🏗️ Guia de Engenharia e Infraestrutura (v7.2.4)

Este documento é a referência técnica definitiva sobre a arquitetura, monitoramento e manutenção do ecossistema SIGE.

---

## ☁️ 1. Arquitetura Cloud e Serviços
O SIGE utiliza uma infraestrutura híbrida focada em alta disponibilidade e escalabilidade.

| Componente | Tecnologia | Papel |
|---|---|---|
| **Runtime** | Render (Docker) | Execução ASGI via Daphne (v4.x) |
| **Banco de Dados** | MySQL (Aiven) | Persistência relacional com SSL obrigatório |
| **Cache & Layers** | Redis | Gerenciamento de cache e Channel Layer para WebSockets |
| **Armazenamento** | Cloudinary CDN | CDN para mídia e documentos estáticos |
| **Mensageria** | Celery + RabbitMQ | Processamento de tarefas assíncronas em background |

---

## 🛠️ 2. Hub de Infraestrutura (Consolidado)
Na **versão v7.2.4**, as operações e o monitoramento de integrações foram unificados em uma única interface em `/ti/infraestrutura/`.

### 🖥️ Monitoramento de Serviços
O sistema realiza checagens constantes de latência e disponibilidade:
- **Health Check Real:** Via `django-health-check`, validando escrita em disco, leitura de cache e conexão DB.
- **Latência:** Exibição em tempo real da resposta de serviços críticos (Redis, SMTP, Cloudinary).

### 💻 Console de Manutenção (Scripts)
Ações de manutenção automatizadas disponíveis via interface:
- **Limpeza de Cache:** Esvazia o Redis para resolver inconsistências de visualização.
- **Gestão de Sessões:** Remove sessões expiradas do banco de dados para otimização de performance.
- **Coleta de Estáticos:** Sincronização de assets em tempo de deploy.

---

## 🛡️ 3. Segurança e Observabilidade (SOC)
O **Security Operations Center (SOC)** é o núcleo de defesa da v7.x.

- **Defesa Ativa:** Blacklist dinâmica de IPs integrada ao middleware de segurança.
- **Auditoria LGPD:** Captura automática de acessos a dados sensíveis (CPF, Saúde, Financeiro).
- **Security Score:** Cálculo dinâmico de saúde de segurança baseado em incidentes ativos.
- **Bug Tracking:** Sistema de triagem `BugReport` para falhas voluntariamente reportadas.

---

## 📡 4. Stack Real-time (WebSockets)
Utilização de **Django Channels** para feedback instantâneo sem necessidade de recarregamento de página.

- **Protocolo:** WSS (WebSocket Secure).
- **Consumer:** `apps/ti/consumers.py`.
- **Eventos:** Alertas de SOC, notificações de novos bugs e logs de manutenção.

---

## 🌸 5. Ferramentas de Monitoramento Externo
- **Flower:** Interface de monitoramento de workers Celery (Porta `:5555`).
- **Endpoint Health:** `/health/` expõe o status JSON para monitores externos (UptimeRobot, etc.).

---

## ⚙️ 6. Configuração de Ambiente (.env)
Variáveis técnicas essenciais para o funcionamento da infraestrutura:
```env
USE_REDIS=True
REDIS_URL=redis://...
DATABASE_URL=mysql://...
CLOUDINARY_URL=...
CELERY_BROKER_URL=...
```

---
> **Aviso:** Alterações de infraestrutura devem ser registradas no log de engenharia. Versionamento v7.2.4 em vigor.
