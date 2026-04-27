# 📊 Análise Técnica e Propostas de Melhoria — SIGE v2.5
> **Atualizado em:** 27 de Abril de 2026

---

## ✅ Concluído Nesta Sprint

| Item | Resultado |
|---|---|
| **Testes corrigidos** | 6 falhas → **45/45 passando (100% verde)** |
| **Cobertura** | 53% → **55%** |
| **Cache Local** | Fallback automático para `LocMemCache` sem Redis |
| **Bordas de Cards** | Todos os 20+ tipos de card cobertos nos temas Azul e Cinza |
| **Organização** | Pastas `docs/` e `scripts/` criadas |

---

## 1. 🏗️ Engenharia de Software: Refatoração do Núcleo

O padrão **Clean Architecture** (Services/Selectors) deve ser expandido.

- **Módulo Acadêmico**: Views de notas ainda possuem lógica de decisão.
    - *Proposta*: `academico/services/notas.py` para isolar o cálculo de aprovação.
- **Módulo Financeiro**: Garantir atomicidade total na baixa de faturas.

---

## 2. 🧪 Garantia de Qualidade (QA)

- **Meta 75%** → Próximos alvos de 0% de cobertura:
    - `apps/financeiro/services/financeiro_service.py`
    - `apps/usuarios/services/perfil_service.py`
    - `apps/dashboards/views.py` (28%)
    - `apps/saude/views.py` (25%)
- **Testes de UI (E2E)**: Fluxo de matrícula e lançamento de notas.

---

## 3. 🌐 API & Integrações

- **DRF (Django REST Framework)**: Endpoints para todos os módulos.
- **Webhooks**: Confirmações de pagamento Asaas/Efí em tempo real.
- **Notificações Push**: WhatsApp Business API ou Firebase.

---

## 4. 🏢 Escalabilidade SaaS

- **PostgreSQL + RLS**: Migração do Multi-Tenancy de "filtro por query" para Row Level Security.
- **AWS S3 / Cloudinary**: Externalizar `media/` para deploy serverless.

---

## 🎨 5. Experiência de Produto (UX)

- **Portal do Responsável**: Pagamento (Pix copy-paste) e Alertas de Frequência.
- **Onboarding Automático**: Assistente de configuração inicial da escola.

---

### 🚀 Prioridade Jarviana:
1. **Curto Prazo**: Subir testes para 75% (foco nos Services zerados).
2. **Médio Prazo**: API REST e Gateway de Pagamento.
3. **Longo Prazo**: PostgreSQL RLS (SaaS Scale).
