# 📊 SIGE → Nível SUAP/SIGEDUC — Análise de Gap Completa
> **Objetivo:** Identificar o que falta, o esforço estimado e a ordem de ataque para atingir excelência institucional.  
> **Referência:** SUAP (IFRN), SIGEDUC (SEDUC-CE), Q-Acadêmico, Lyceum.  
> **Data:** 23 de Abril de 2026

---

## 🗺️ Legenda de Status

| Símbolo | Significado |
|---|---|
| ✅ | Implementado e funcional |
| 🟡 | Parcialmente implementado |
| ❌ | Ausente — requer desenvolvimento do zero |
| 🔴 | Crítico (bloqueador para uso institucional) |
| 🟠 | Alto impacto (diferencial competitivo) |
| 🟡 | Médio impacto (maturidade do produto) |

---

## 📋 1. Gestão Acadêmica Avançada

| Funcionalidade | Status | Criticidade | Esforço | Detalhes Técnicos |
|---|---|---|---|---|
| Cadastro de Turmas, Disciplinas e Grade | ✅ | — | Feito | Completo com horários e professores |
| Notas bimestrais e Frequência | ✅ | — | Feito | Diário digital com situação automática |
| Atividades, Quiz e Gabarito | ✅ | — | Feito | Objetiva/Discursiva com correção |
| Planejamento de Aulas | ✅ | — | Feito | Por disciplina com anexos |
| **Currículo / Matriz Curricular Versionada** | ❌ | 🔴 Crítico | ~3 sprints | Componentes com carga horária, pré-requisitos entre disciplinas, CH total por período. Model `MatrizCurricular` → `ComponenteCurricular` → `PreRequisito`. |
| **Fluxo de Matrícula Completo** | ❌ | 🔴 Crítico | ~4 sprints | Período de matrículas, seleção de disciplinas pelo aluno, fila de espera, deferimento pelo gestor. States: `ABERTO → EM_ANALISE → CONFIRMADO → CANCELADO`. |
| **Histórico Escolar Oficial (PDF assinado)** | 🟡 | 🔴 Crítico | ~2 sprints | Existe boletim simples. Falta: assinatura digital, QR Code de autenticidade, CH acumulada, situação final por ano. |
| **Colegiado / Conselho de Classe Digital** | ❌ | 🟠 Alto | ~2 sprints | Ata eletrônica, deliberações por aluno, aprovação por votação, registro em PDF. |
| **Estágios e TCCs** | ❌ | 🟠 Alto | ~3 sprints | Fluxo: Orientador → Banca → Defesa → Aprovação → Registro no Histórico. |
| Calendário Letivo | ✅ | — | Feito | Com feriados e eventos por turma |
| Mural / Comunicados | ✅ | — | Feito | Segmentado por público |

**Gap crítico:** A ausência de Matriz Curricular torna o sistema academicamente fraco para ensino técnico/superior. O Fluxo de Matrícula é o ponto que mais diferencia um sistema escolar real de uma planilha avançada.

---

## 🔐 2. Identidade, Acesso e Autenticação

| Funcionalidade | Status | Criticidade | Esforço | Detalhes Técnicos |
|---|---|---|---|---|
| Login com usuário/senha | ✅ | — | Feito | Django Auth padrão |
| Perfis: Gestor, Professor, Aluno | ✅ | — | Feito | Groups + OneToOne |
| Trilha de Auditoria | ✅ | — | Feito | django-simple-history |
| Proteção Brute Force | ✅ | — | Feito | django-axes |
| Criptografia de dados sensíveis | ✅ | — | Feito | AES/Fernet |
| **2FA obrigatório (TOTP)** | ❌ | 🔴 Crítico | ~1 sprint | Google Authenticator + backup codes. `django-otp` + `django-two-factor-auth`. Obrigatório para Gestor e Superusuário. |
| **SSO institucional (LDAP/SAML)** | ❌ | 🟠 Alto | ~2 sprints | Login único com credencial da rede da instituição. `django-auth-ldap` para LDAP; `python3-saml` para SAML2. |
| **Perfis granulares por campus/turno** | ❌ | 🟠 Alto | ~2 sprints | Gestor vê dados do seu campus; Coordenador vê sua área de conhecimento. Requer `tenant_id` ou `scope` nos models críticos. |
| **Portal do Responsável** | ❌ | 🟠 Alto | ~2 sprints | Acesso limitado: notas, faltas e faturas do dependente. Novo grupo `Responsavel` com FK para `Aluno`. |
| Timeout de Sessão | ✅ | — | Feito | Configurável em settings.py |

**Gap crítico:** 2FA é requisito mínimo para qualquer sistema que manipule dados de saúde e financeiros de menores. LGPD exige isso. Um sprint resolve.

---

## 📄 3. Protocolo, Documentos e Processos

| Funcionalidade | Status | Criticidade | Esforço | Detalhes Técnicos |
|---|---|---|---|---|
| Atestados médicos com fluxo de aprovação | ✅ | — | Feito | Envio → Triagem → Abono automático |
| Comunicados internos | ✅ | — | Feito | Mural segmentado |
| **Protocolo de Requerimentos** | ❌ | 🔴 Crítico | ~2 sprints | Aluno abre solicitação (cancelamento, revisão de nota, trancamento), gestor defere/indefere com prazo automatizado. Model `Requerimento` com `status`, `tipo`, `prazo_resposta` e `celery_task_id`. |
| **Boletim e Declarações em PDF oficial** | 🟡 | 🔴 Crítico | ~1 sprint | Existe geração básica. Falta: timbre institucional, assinatura do diretor, QR Code de autenticidade com hash do documento no banco. ReportLab + `qrcode`. |
| **Assinatura Digital (ICP-Brasil / DocuSign)** | ❌ | 🟠 Alto | ~3 sprints | Documentos com validade jurídica sem papel. ITI-BR para ICP-Brasil; alternativa: hash + timestamp RFC3161 como "proto-assinatura". |
| **GED — Gestão Eletrônica de Documentos** | ❌ | 🟠 Alto | ~3 sprints | Versionamento de documentos, categorias, permissões por tipo de documento, índice de busca. Model `Documento` com `versao`, `categoria`, `acesso_por_grupo`. |
| Exportação de Dados (CSV/Excel) | 🟡 | 🟡 Médio | ~1 sprint | Existe em alguns módulos. Falta padronização global. |

**Gap crítico:** Protocolo de Requerimentos é o que mais reduz trabalho manual da secretaria. É a funcionalidade mais solicitada em qualquer sistema escolar real.

---

## 🏛️ 4. Gestão Institucional e Multi-Campus

| Funcionalidade | Status | Criticidade | Esforço | Detalhes Técnicos |
|---|---|---|---|---|
| Cadastro de Unidades/Campus | 🟡 | — | Parcial | Existe `Unidade` no modelo de infraestrutura |
| Patrimônio por unidade | ✅ | — | Feito | Por campus com responsável |
| **Multi-Tenant Nativo** | ❌ | 🔴 Crítico | ~5 sprints | Múltiplas escolas/campus isoladas na mesma instância. PostgreSQL RLS (Row Level Security) ou `django-tenants` (schema por tenant). **Maior esforço técnico do roadmap — deve ser desenhado antes do 2º cliente.** |
| **Organograma e Estrutura de Cargos** | ❌ | 🟠 Alto | ~2 sprints | Hierarquia institucional (Reitor → Diretor → Coordenador → Professor) com delegação de acesso contextual. |
| **Relatórios MEC/INEP (Censo Escolar)** | ❌ | 🟠 Alto | ~3 sprints | Exportação no formato EducaCenso (XML/layout fixo) e SAEB. Diferencial enorme no segmento público. Falta mapeamento de campos do Django para o layout oficial. |
| **Configurações Globais por Instituição** | ❌ | 🟡 Médio | ~1 sprint | Logo, nome, CNPJ, regime de avaliação (notas 0-10 vs. conceitual), data de início do ano letivo — por tenant. |

**Gap arquitetural:** Multi-tenant é o único item que exige decisão **antes** de qualquer outro da Fase 4+. Adicionar depois é refatoração de todo o ORM.

---

## 🤖 5. Inteligência, BI e Predição

| Funcionalidade | Status | Criticidade | Esforço | Detalhes Técnicos |
|---|---|---|---|---|
| Dashboard financeiro (DRE, KPIs) | ✅ | — | Feito | Completo com gráficos Chart.js |
| Métricas de infraestrutura | ✅ | — | Feito | Por categoria e estado |
| BI básico de frequência e notas | 🟡 | — | Parcial | Existe por disciplina, falta consolidado |
| **Motor de Risco de Evasão (ML)** | ❌ | 🟠 Alto | ~4 sprints | Regressão logística / Gradient Boosting treinado com: `frequencia_acumulada`, `notas_por_bimestre`, `inadimplencia_meses`, `atestados_count`. Antecipação semestral. Bibliotecas: `scikit-learn` + `joblib`. |
| **BI Consolidado Multi-Módulo** | ❌ | 🟠 Alto | ~2 sprints | DRE + Desempenho Acadêmico + Frequência + Risco de Evasão em um painel executivo unificado. Requer `DataWarehouse` local ou views materializadas no banco. |
| **Alertas Inteligentes Automatizados** | 🟡 | 🟠 Alto | ~2 sprints | Notificações proativas: aluno com >3 faltas consecutivas, fatura 5 dias antes de vencer, estoque abaixo do mínimo. Celery Beat para agendamento. Parcialmente implementado via notificações, falta automação por threshold. |
| **Relatório Comparativo de Turmas** | ❌ | 🟡 Médio | ~1 sprint | Ranking de turmas por aprovação, frequência e inadimplência. |

---

## 🗺️ Roadmap de Ataque — Ordem Sugerida

> [!IMPORTANT]
> Ordem baseada em: **desbloqueio de dependências** → **impacto imediato** → **diferencial competitivo**.

```
AGORA (Antes do 1º cliente real)
├── 2FA obrigatório para Gestor/Super          ~1 sprint   🔴 Crítico
├── PDF Oficial (boletim + QR autenticidade)   ~1 sprint   🔴 Crítico
├── Auditoria LGPD + RIPD                      ~1 sprint   🔴 Crítico
└── Sentry em produção                         ~1 dia      🔴 Crítico

SPRINT 1-2 (Base de produto vendável)
├── Protocolo de Requerimentos                 ~2 sprints  🔴 Crítico
├── Portal do Responsável                      ~2 sprints  🟠 Alto
└── Cobertura de Testes 53% → 75%             contínuo    🟠 Alto

SPRINT 3-6 (Diferencial acadêmico)
├── Matriz Curricular Versionada               ~3 sprints  🔴 Crítico
├── Histórico Escolar Oficial                  ~2 sprints  🔴 Crítico
└── Conselho de Classe Digital                 ~2 sprints  🟠 Alto

SPRINT 7-10 (Ciclo financeiro real)
├── Gateway Pagamento (Asaas/Efí) + Webhook   ~2 sprints  🟠 Alto
├── Régua de Cobrança automatizada             ~1 sprint   🟠 Alto
└── NF-e de Serviços                           ~2 sprints  🟠 Alto

SPRINT 11-14 (API + Integrações)
├── API REST completa (DRF + JWT + Swagger)    ~3 sprints  🟠 Alto
├── SSO/LDAP institucional                     ~2 sprints  🟠 Alto
└── Relatórios MEC/INEP (Censo Escolar)        ~3 sprints  🟠 Alto

SPRINT 15-18 (Inteligência)
├── Alertas automáticos (Celery Beat)          ~2 sprints  🟠 Alto
├── BI Consolidado multi-módulo                ~2 sprints  🟠 Alto
└── Motor de Risco de Evasão (ML)              ~4 sprints  🟠 Alto

SPRINT 19+ (Escala SaaS)
├── Multi-Tenant nativo (PostgreSQL RLS)        ~5 sprints  🔴 Arquitetural
├── Organograma e Cargos                        ~2 sprints  🟡 Médio
├── GED + Assinatura Digital (ICP-Brasil)       ~6 sprints  🟠 Alto
└── Estágios / TCCs / Fluxos de Defesa         ~3 sprints  🟠 Alto
```

---

## 🏗️ Arquitetura Alvo — Visão de Módulos

```
┌─────────────────────────────────────────────────────────────┐
│                    SIGE — Arquitetura Alvo v3.0             │
├─────────────────────────────────────────────────────────────┤
│  CAMADA DE APRESENTAÇÃO                                     │
│  ┌──────────┐  ┌────────────┐  ┌───────────┐  ┌─────────┐ │
│  │ Painel   │  │  Portal    │  │ PWA/Mobile │  │ API     │ │
│  │ Gestor   │  │Responsável │  │  (Aluno/  │  │ REST    │ │
│  │ (Django) │  │  (Django)  │  │  Prof.)   │  │ (DRF)   │ │
│  └──────────┘  └────────────┘  └───────────┘  └─────────┘ │
├─────────────────────────────────────────────────────────────┤
│  CAMADA DE SERVIÇOS                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────┐ │
│  │Acadêmico │  │Financeiro│  │  Saúde   │  │Documentos │ │
│  │+ Matriz  │  │+ Gateway │  │  + LGPD  │  │  + GED    │ │
│  │+ Matrícu.│  │+ NF-e    │  │          │  │ + ICP-BR  │ │
│  └──────────┘  └──────────┘  └──────────┘  └───────────┘ │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────┐ │
│  │Biblioteca│  │  Infra   │  │  Pessoas │  │    BI     │ │
│  │+ OpenLib │  │+ Estoque │  │ + SSO    │  │ + ML      │ │
│  │          │  │          │  │ + 2FA    │  │ + Evasão  │ │
│  └──────────┘  └──────────┘  └──────────┘  └───────────┘ │
├─────────────────────────────────────────────────────────────┤
│  CAMADA DE INFRAESTRUTURA                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────┐ │
│  │PostgreSQL│  │  Redis   │  │  Celery  │  │  Sentry   │ │
│  │+ RLS     │  │  Cache   │  │  + Beat  │  │ + Grafana │ │
│  │Multi-Ten.│  │          │  │  Tasks   │  │           │ │
│  └──────────┘  └──────────┘  └──────────┘  └───────────┘ │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────┐ │
│  │   AWS S3 │  │Cloudinary│  │  Vercel  │  │ Railway   │ │
│  │  (PDFs)  │  │ (Images) │  │   CDN    │  │ (Backend) │ │
│  └──────────┘  └──────────┘  └──────────┘  └───────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 📈 Score de Maturidade — SIGE vs. Referências de Mercado

| Módulo | SIGE Atual | SIGE Alvo | SUAP | SIGEDUC |
|---|---|---|---|---|
| Gestão Acadêmica | 65% | 95% | 98% | 85% |
| Módulo Financeiro | 60% | 90% | 75% | 70% |
| Identidade & Acesso | 70% | 95% | 90% | 80% |
| Documentos & Protocolos | 30% | 85% | 92% | 78% |
| Gestão Institucional | 20% | 80% | 95% | 85% |
| Inteligência & BI | 45% | 85% | 60% | 40% |
| Infraestrutura SaaS | 35% | 90% | 70% | 50% |
| UX/Design System | **90%** | 95% | 45% | 50% |
| **TOTAL** | **52%** | **90%** | **78%** | **67%** |

> [!NOTE]
> UX e Design System são os únicos pontos onde o SIGE **já supera** o SUAP. Os sistemas do governo têm funcionalidade ampla mas interfaces datadas. Isso é uma vantagem competitiva real no segmento privado.

---

## ⏱️ Estimativa Total de Esforço

| Prioridade | Total de Sprints | Prazo Estimado (1 dev sênior) |
|---|---|---|
| Bloqueadores imediatos | ~4 sprints | ~1 mês |
| Base de produto (Fase 1-2) | ~8 sprints | ~2 meses |
| Diferencial acadêmico (Fase 3) | ~7 sprints | ~1,5 meses |
| Ciclo financeiro real (Fase 4) | ~5 sprints | ~1,5 meses |
| API + Integrações (Fase 5) | ~8 sprints | ~2 meses |
| Inteligência e BI (Fase 6) | ~8 sprints | ~2 meses |
| Escala SaaS (Fase 7+) | ~16 sprints | ~4 meses |
| **TOTAL para nível SUAP** | **~56 sprints** | **~14 meses** |

> [!TIP]
> Com 2 devs (1 sênior + 1 pleno) em paralelo, o prazo cai para ~8 meses para atingir paridade funcional com o SUAP.  
> O SIGE já tem 52% do caminho feito — e a base é tecnicamente superior em design e arquitetura moderna.

---

*Documento gerado em 23 de Abril de 2026 — Sprint de Análise Estratégica*  
*Referências: SUAP (IFRN), SIGEDUC (SEDUC-CE), Q-Acadêmico 7.x, Lyceum 9.x*
