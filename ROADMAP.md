# 🚀 SIGE — Roadmap Estratégico v2.0
> **Última atualização:** 23 de Abril de 2026 — Revisão Estratégica Completa  
> **Status do produto:** Base técnica sólida → Transição para produto vendável

> [!IMPORTANT]
> O maior risco de escalonamento não é tecnológico — é fazer a transição de "sistema bem construído" para "produto vendável" sem perder a qualidade que já existe.

---

## ✅ Concluído — Base Funcional

### 🏗️ Arquitetura & Infraestrutura
- Arquitetura modular Django (MTV) com 10+ apps: `usuarios`, `academico`, `calendario`, `comum`, `comunicacao`, `documentos`, `infraestrutura`, `saude`, `biblioteca`, `financeiro`, `dashboards`.
- Pipeline CI/CD (GitHub Actions), ambiente Docker (App + MySQL + Redis + Celery).
- Processamento assíncrono via Celery + Redis.

### 🎓 Módulo Acadêmico
- Diário de Classe, Frequência, Notas bimestrais e Situação Acadêmica automática.
- Atividades com Quiz (Objetiva/Discursiva), Gabarito e Correção Individualizada.
- Materiais Didáticos por disciplina (Links, Arquivos, Livros da biblioteca).
- Planejamento de Aulas e Grade Horária.

### 💰 Módulo Financeiro (BI Contábil)
- Livro Diário (`Lancamento`) com Centro de Custo e Categorias.
- Controle de Faturas (Mensalidades) com status `PENDENTE`, `PAGO`, `ATRASADO`.
- Folha de Pagamento com reajustes históricos anuais.
- Dashboard Gerencial: DRE, fluxo de caixa, inadimplência e KPIs.

### 🏥 Saúde, 📚 Biblioteca, 🏢 Infraestrutura
- Fichas médicas, atestados com abono automático de faltas, alertas de alergia no diário.
- Acervo físico/digital + Empréstimos + 200 Best-Sellers via OpenLibrary API.
- Patrimônio, manutenção, almoxarifado com alertas de estoque mínimo.

### 🎨 Design System Premium & 🔒 Segurança Enterprise
- Três temas: Indigo Profundo, Cinza Industrial, Azul Corporativo — 100% theme-aware.
- Criptografia AES/Fernet, Trilha de Auditoria (django-simple-history), proteção Brute Force.
- Validação real de CPF/CNPJ, ZXCVBN, prontidão para 2FA.

### 📖 Documentação & Dados
- READMEs técnicos em todos os módulos.
- `seed_db.py`: Simulador de 10 anos de operação escolar com +30.000 registros realistas.

---

## ⚠️ Bloqueadores Atuais (Resolver Antes de Escalar)

> [!CAUTION]
> Estes itens são **bloqueadores práticos** — sem eles, o sistema não pode ser implantado em clientes reais com segurança.

| # | Bloqueador | Risco |
|---|---|---|
| 1 | **Sentry em Produção** | Erros silenciosos em módulos financeiros e de saúde são críticos. Deve ser o **primeiro** item antes de qualquer cliente real. |
| 2 | **PDF Real (ReportLab)** | Boletins e declarações são exigidos frequentemente pelas famílias. A ausência cria dependência de processos manuais paralelos. |
| 3 | **Cobertura de Testes 53% → 75%** | Com 10+ módulos interligados, o débito técnico cresce exponencialmente a cada nova feature. Invisível para o usuário, decisivo para a estabilidade. |
| 4 | **Auditoria de LGPD** | O sistema já cifra CPF/dados sensíveis, mas falta documentar o fluxo de dados, implementar o "direito ao esquecimento" e gerar o RIPD (Relatório de Impacto à Proteção de Dados). **Obrigatório juridicamente antes de escala comercial no Brasil.** |

---

## 🔴 Fase 1 — Ciclo Financeiro Real *(Q2/2026 — Alta Prioridade)*
> **Meta:** Transformar o módulo de um "livro-razão digital" em uma ferramenta de cobrança ativa. Fecha o ciclo financeiro sem intervenção humana.

- **Gateway de Pagamento (Asaas/Efí)**: Emissão real de Pix e Boletos bancários integrados ao modelo `Fatura`.
- **Webhook de Confirmação**: Atualização automática de status ao receber confirmação do banco — elimina baixa manual.
- **Carnê Digital no Painel do Aluno**: QR Code Pix com valor e vencimento gerados dinamicamente.
- **Régua de Cobrança**: E-mails/notificações automáticas em D-3, D-1 e D+1 (após vencimento).
- **NF-e de Serviços**: Emissão automática de nota fiscal eletrônica ao liquidar faturas.

> [!TIP]
> **Recomendação de início:** Asaas tem SDK Python nativo e sandbox gratuito. A integração do webhook + atualização do status da `Fatura` é realizável em 1 sprint sem grandes alterações no schema atual.

---

## 🟠 Fase 2 — Portal do Responsável & Comunicação *(Q3/2026)*
> **Meta:** Dar transparência às famílias e reduzir drasticamente o volume de chamados na secretaria.

- **Perfil "Responsável"**: Novo grupo de acesso com visibilidade de Notas, Faltas e Faturas do filho vinculado.
- **WhatsApp Business API**: Notificações push de lembrete de fatura, resultado de prova e atestado aprovado — muito mais eficaz que Web Push no Brasil.
- **Autorização Digital de Saída**: Assinatura digital do responsável para eventos e excursões.
- **Dashboard Simplificado**: Interface limpa e não-técnica para pais — apenas o essencial.

> [!NOTE]
> WhatsApp Business API tem adoção imediata no Brasil. Integração via providers como Twilio ou Z-API. Mais impactante que qualquer PWA no curto prazo.

---

## 🟡 Fase 3 — API REST + Fundação Mobile *(Q3/2026 — Pré-requisito para Fases 4 e 5)*
> **Meta:** Criar a espinha dorsal técnica que habilita todas as integrações e o app mobile. Fazer depois gera retrabalho extenso.

- **API REST Completa**: Endpoints estáveis e versionados com Django REST Framework.
- **Documentação Swagger/OpenAPI**: Auto-gerada via `drf-spectacular` — padrão de mercado.
- **Autenticação JWT**: Substituição de sessões por tokens para consumo via mobile e integrações.
- **Rate Limiting & Throttling**: Proteção da API por perfil de usuário.

> [!IMPORTANT]
> Esta fase é **pré-requisito silencioso** para PWA, app mobile e integração com Google Classroom. Antecipar API antes de construir consumidores evita reescrita do contrato de dados.

---

## 🟢 Fase 4 — Inteligência & Predição *(Q4/2026)*
> **Meta:** Transformar 10 anos de histórico em inteligência preditiva. O dado já existe — o modelo pode ser simples.

- **Motor de Risco de Evasão**: Regressão logística ou Gradient Boosting treinado com `frequencia`, `inadimplencia`, `notas_bimestrais` e `historico_atestados`. Antecipação semestral permite intervenção antes da evasão acontecer.
- **Dashboard de Correlação de Turma**: Frequência × Nota × Volume de Atividades do Professor.
- **Assistente de Planejamento**: Sugestão automática de datas para provas baseada na grade horária e calendário letivo.
- **Relatórios MEC/INEP (Antecipado)**: Exportação no formato do Censo Escolar. Diferencial enorme no segmento público e filantrópico onde os sistemas atuais são notoriamente ruins.

> [!TIP]
> Comece o ML com `scikit-learn` + dados locais. Não é preciso infraestrutura de cloud para um modelo de 240 alunos. A acurácia inicial importa menos que a **utilidade clínica** da previsão.

---

## 🔵 Fase 5 — Mobile Real *(Q1/2027)*
> **Meta:** SIGE funcionando como aplicativo nativo no celular — após a API estar madura.

- **PWA (Progressive Web App)**: Manifest.json, Service Worker e offline caching para professor marcar presença sem internet.
- **Frequência por QR Code**: Professor exibe QR Code projetado; aluno escaneia ao entrar na sala. Alternativa ao reconhecimento facial (privacidade).
- **Modo Offline Inteligente**: Sincronização automática ao reconectar à internet.

---

## ⚫ Fase 6 — Infraestrutura SaaS Multi-Tenant *(Q2/2027)*
> **Meta:** Escalar para múltiplas escolas com isolamento real de dados e custo mínimo.

> [!WARNING]
> **Ordem de migração recomendada — não pule etapas:**

### Passo 1 — Multi-Tenancy Nativo (PRIMEIRO)
- **Schema separado por escola** no PostgreSQL com Row Level Security (RLS) — ou filtro `escola_id` em todas as queries do ORM.
- ⚠️ Adicionar multi-tenancy depois de escalar é **cirurgia em todo o codebase**. Deve ser desenhado antes do segundo cliente.

### Passo 2 — Banco de Dados para PostgreSQL/Supabase
- MySQL em Docker é risco em produção multiescola.
- PostgreSQL + RLS permite isolar dados de escolas diferentes na mesma instância — modelo SaaS econômico.

### Passo 3 — Separação de Assets
- **Cloudinary**: Imagens de perfil, capas de livros.
- **AWS S3 ou Cloudflare R2**: PDFs de boletins, declarações e arquivos de atividades.
- Resolve o problema de filesystem efêmero em plataformas como Railway e Render.

### Passo 4 — Deploy Desacoplado
- **Backend**: Railway ou Render com auto-scaling.
- **Frontend (Vite/React)**: Vercel com CDN global.
- Só faz sentido **após a API REST estar madura** — separação prematura aumenta complexidade sem benefício.

### Passo 5 — Observabilidade Completa
- **Sentry**: Rastreamento de erros em produção (⚠️ deveria estar ativo desde o **Bloqueador #1**).
- **Grafana + Prometheus**: Métricas de performance, latência de queries e uso por escola.
- **Uptime Robot / BetterStack**: Alertas de disponibilidade 24/7.

---

## 📊 Matriz de Prioridade Revisada

| Prioridade | Item | Impacto | Esforço | Quando |
|---|---|---|---|---|
| 🔴 Crítico | Sentry em Produção | Segurança operacional | Baixo (1 dia) | Antes do 1º cliente |
| 🔴 Crítico | PDF Real (ReportLab) | Bloqueador de uso diário | Médio | Q2/2026 |
| 🔴 Crítico | Auditoria LGPD + RIPD | Obrigatório juridicamente | Médio | Q2/2026 |
| 🟠 Alta | Cobertura de Testes 75% | Estabilidade futura | Alto | Q2/2026 |
| 🟠 Alta | Gateway Pagamento (Asaas) | Fecha ciclo financeiro | Médio | Q2/2026 |
| 🟡 Média | Portal do Responsável | Diferencial competitivo | Alto | Q3/2026 |
| 🟡 Média | WhatsApp Business API | Adoção imediata no BR | Baixo | Q3/2026 |
| 🟡 Média | API REST + JWT + Swagger | Pré-requisito para mobile | Alto | Q3/2026 |
| 🟢 Normal | Motor de Risco de Evasão (ML) | Usa histórico existente | Alto | Q4/2026 |
| 🟢 Normal | Censo Escolar / MEC | Diferencial segmento público | Médio | Q4/2026 |
| 🔵 Futuro | Multi-Tenancy Nativo | SaaS escalável | Muito Alto | Q1/2027 |
| 🔵 Futuro | PWA + Offline | Experiência mobile | Alto | Q1/2027 |
| ⚫ Longo Prazo | Google Classroom / Teams | Integração EdTech | Alto | Q2/2027 |
| ⚫ Longo Prazo | Deploy Nuvem SaaS | Escala multi-escola | Alto | Q2/2027 |

---

## 🧭 Oportunidades Estratégicas Não Mapeadas Anteriormente

> [!NOTE]
> Estas oportunidades foram identificadas na revisão estratégica e representam diferenciais reais de mercado.

1. **Multi-Tenancy como design first** — Se a visão é vender para múltiplas escolas, isso deve ser arquitetado **antes** do segundo cliente, não depois.
2. **Segmento público/filantrópico** — Relatórios MEC/INEP é um diferencial enorme onde sistemas como eSocial/SIGEAM são notoriamente ruins. Antecipação estratégica.
3. **LGPD como vantagem comercial** — Documentar compliance com LGPD (RIPD, políticas de retenção, anonimização) antes de concorrentes é argumento de vendas, não só obrigação legal.
4. **Integrações bancárias abertas (Open Finance)** — Com o avanço do Open Finance no Brasil, dados bancários das famílias podem alimentar análises de risco de inadimplência de forma regulamentada.

---

*Última atualização: 23 de Abril de 2026 — Revisão Estratégica Completa*  
*Baseado em análise técnica e de produto da arquitetura atual do SIGE*
