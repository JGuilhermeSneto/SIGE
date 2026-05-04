# 🚀 SIGE — Roadmap Estratégico v2.0
> **Última atualização:** 04 de Maio de 2026 — Central de Segurança & Telemetria de Erros (Shield v1.0)
> **Status do produto:** Governança de dados robusta → SaaS-Ready

> [!IMPORTANT]
> O SIGE agora possui stack de observabilidade industrial, testes corrigidos (45/45 ✅) e Design System reforçado com bordas universais nos temas Azul e Cinza.

---

## ✅ Concluído — Base Funcional & Infra de Elite

### 🏗️ Arquitetura & Infraestrutura
- Arquitetura modular Django (MTV) com 11 apps integrados.
- **Observabilidade Total**: Monitoramento em tempo real via **Grafana + Prometheus**.
- **Mensageria Industrial**: Broker Celery migrado para **RabbitMQ**.
- **Clean Architecture**: Service Layer + Selectors em todos os módulos críticos.
- **Cache Inteligente**: Fallback automático para `LocMemCache` quando Redis não está disponível (modo local).
- **Cloud Deployment**: Pipeline de deploy contínuo em produção via **Render + Aiven (MySQL)** com SSL automático e domínio próprio. *(Migrado para região US para mitigar timeouts).*
- **Organização de Projeto**: Estrutura `docs/` e `scripts/` criadas para separar documentação e utilitários.

### 🧪 Qualidade de Software
- **45 testes passando (100% verde)** — Corrigidos: Mock exaurido (Selectors), table name errado (Finance), Axes/Request (Login), CPF inválido (Perfis), script conflitante (API).
- **Cobertura: 53% → 55%** — Progressão em andamento para meta de 75%.

### 🎨 Design System
- **Premium Glassmorphism**: Interface fluida com bordas 48px e temas dinâmicos.
- **Bordas de Cards Universais**: Todos os 20+ tipos de card cobertos nos temas **Azul Corporativo** e **Cinza Industrial**.

### 🧠 Inteligência & Dados
- **Hub de Inteligência Unificado**: BI Acadêmico + Relatórios em uma interface única.
- Evasão Preditiva, Saúde & Inclusão, Performance por Turma.
- `seed_db.py`: Simulador de 10 anos com +30.000 registros.

### 🔒 Segurança & Auditoria
- **Central de Segurança "Shield v1.0"**: Dashboard unificado para monitoramento de conformidade.
- **Auditoria LGPD**: Registro atômico de acessos a áreas sensíveis (Financeiro, Saúde, Admin).
- **Telemetria de Erros**: Sistema interno de captura de exceções (500) com traceback técnico para debug rápido.
- **Monitoramento de Governança**: Acompanhamento de adoção de MFA (2FA), sessões ativas e auditoria de ações administrativas (LogEntry).
- **Proteção Ativa**: Brute Force protection (Axes) integrado ao painel de intrusões.

---

## ⚠️ Bloqueadores Atuais (Foco Imediato)

| # | Bloqueador | Risco | Status |
|---|---|---|---|
| 1 | **Cobertura de Testes 55% → 75%** | Débito técnico em Services (0% cobertura) | 🟠 Em andamento |
| 2 | **Refatoração Módulo Acadêmico** | Lógica de notas ainda nas Views | 🟡 Planejado |

---

## 🔴 Fase 1 — Ciclo Financeiro Real *(Q2/2026)*
- **Gateway Asaas/Efí**: Pix e Boletos reais.
- **Webhook**: Baixa automática de faturas.
- **NF-e de Serviços**: Nota fiscal eletrônica automática.

---

## 🟠 Fase 2 — Portal do Responsável *(Q3/2026)*
- [x] Portal base implementado.
- **WhatsApp Business API**: Notificações push.
- **Autorização Digital**: Assinatura para eventos.

---

## 🟡 Fase 3 — API REST + Fundação Mobile *(Q3/2026)*
- **DRF completo** com endpoints versionados.
- **Swagger** auto-gerado.
- **JWT** para autenticação mobile.

---

## 🟢 Fase 4 — IA & Predição *(Q4/2026)*
- **Motor de Evasão V2**: ML com `scikit-learn`.
- **Relatórios MEC/INEP**: Exportação para Censo Escolar.

---

## 📊 Matriz de Prioridade

| Status | Item | Impacto | Quando |
|---|---|---|---|
| ✅ | Observabilidade (Grafana + Prometheus) | Estabilidade | 27/04/2026 |
| ✅ | RabbitMQ Integration | Escalabilidade | 27/04/2026 |
| ✅ | Hub de Inteligência | UX Gestão | 27/04/2026 |
| ✅ | 45 Testes Verdes (100%) | Confiabilidade | 27/04/2026 |
| ✅ | Cloud Deployment (Render + Aiven) | Infra de Produção | 28/04/2026 |
| ✅ | Shield v1.0 (Segurança & Erros) | Governança & LGPD | 04/05/2026 |
| 🟠 | Cobertura 75% | Estabilidade futura | Q2/2026 |
| 🟠 | Gateway Pagamento (Asaas) | Receita real | Q2/2026 |
| 🟡 | API REST + JWT | Fundação Mobile | Q3/2026 |

---

*Última atualização: 04 de Maio de 2026 — Central de Segurança & Telemetria de Erros (Shield v1.0)*
