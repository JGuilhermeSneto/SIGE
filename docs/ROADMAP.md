# 🚀 SIGE — Roadmap Estratégico v2.0
> **Última atualização:** 12 de Maio de 2026 — Área de TI Avançada & Operações Administrativas
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
- **Área de TI Avançada**: Painel operacional com limpeza de logs, health checks, cache management e operações administrativas.

### 🛠️ Área de TI (Melhorias Recentes)
- **Painel TI Otimizado**: Cache de 5 minutos, queries otimizadas com select_related, botões de refresh manual.
- **Operações Administrativas**: Ferramentas funcionais para limpeza de logs antigos, verificação de saúde do sistema, limpeza de cache e export de configurações.
- **Paginação Inteligente**: Dashboard de segurança com paginação (25/20/15/20 itens por página) para melhor performance.
- **Interface Padronizada**: Estilos CSS organizados, cores consistentes com menu lateral, cards interativos com hover effects.
- **Monitoramento em Tempo Real**: Status cards dinâmicos com timestamps de atualização e indicadores visuais.

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

## 🔵 Fase 5 — IoT & Automação Escolar (Projeto Integrador II)
*Integração de hardware para automação de rotinas escolares e coleta de dados em tempo real.*

### 💡 Propostas de Integração
1. **Frequência Automática (RFID)** ⭐:
   - Registro de presença via ESP32 + Leitor RC522.
   - Sincronização automática com o módulo `apps.academico` via MQTT/API.
2. **Painéis de Aviso Inteligentes**:
   - Displays físicos (TFT/LED) nos corredores consumindo a API do SIGE para horários e comunicados.
3. **Controle de Acesso por QR Code**:
   - Integração com a carteirinha digital do aluno para controle de entrada/saída.
4. **Monitoramento de Ocupação**:
   - Sensores PIR em salas de aula para otimização de uso de infraestrutura.

### 🧪 Diferencial Técnico
O SIGE oferece uma base sólida para IoT devido à sua **infraestrutura de testes automatizados** (Pytest + Mocks). Isso permite:
- Testes unitários para lógica de presença MQTT.
- Mocks de brokers para validação de integração no CI/CD.
- Simulação de hardware para garantir estabilidade antes do deploy físico.

---

---

## 🎯 Próximos Passos (Foco Imediato — Amanhã)

### 🔒 1. Fortalecimento da Camada de Segurança
- **MFA (2FA) Mandatório**: Implementar obrigatoriedade de autenticação em dois fatores para perfis administrativos e financeiros.
- **Data Masking**: Aplicar máscaras dinâmicas no frontend para dados sensíveis (CPF, Telefones) mesmo quando descriptografados, liberando a visão completa apenas sob demanda.
- **Honeypot de API**: Criar endpoints falsos para detectar e bloquear scanners automáticos de vulnerabilidades.

### 🧪 2. Expansão Massiva da Cobertura de Testes
- **Testes de Camada de Serviço (Services)**: Alcançar 100% de cobertura nos serviços críticos do módulo `academico` e `financeiro`.
- **E2E Mobile Simulation**: Implementar testes de integração simulando o fluxo de notificações push do backend para o dispositivo mobile.
- **Stress Test de Criptografia**: Validar a performance do sistema sob alta carga de requisições que exijam descriptografia em tempo real.

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
| 🔵 | IoT Integration (RFID/MQTT) | Automação | Q4/2026 |

---

*Última atualização: 05 de Maio de 2026 — Roadmap de Segurança & Testes Críticos*
