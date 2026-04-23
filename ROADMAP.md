# 🚀 SIGE Roadmap & Evolução

Este documento traça o estado atual do projeto e as prioridades de evolução com base na arquitetura e nos módulos já entregues.

## ✅ Concluído (Base funcional e módulos essenciais)
- Arquitetura modular em Django com apps separados: `usuarios`, `academico`, `calendario`, `comum`, `comunicacao`, `documentos`, `infraestrutura`, `saude`, `biblioteca`, `dashboards`.
- Autenticação com perfis e painéis customizados para **Aluno**, **Professor**, **Gestor** e **Superusuário**.
- Cadastro de turmas, disciplinas, grade horária, planejamento de aulas e controle de frequência.
- Sistema de comunicação interno com murais segmentados e avisos por público.
- Geração de documentos em PDF: boletim escolar e declaração de matrícula.
- Gestão de biblioteca com cadastro de livros, empréstimos e devoluções.
- Ficha médica e atestados com fluxo de aprovação e automação de justificativas.
- Registro de patrimônio e movimentações de estoque.
- Design System e suporte inicial a Vite para front-end moderno.

## 🚧 Em andamento (Foco atual)
- Dashboards de BI para gestores com métricas de evasão, desempenho e saúde escolar.
- Consolidação dos fluxos de infraestrutura e estoque na interface de gestão.
- Ajustes de integração entre Django e Vite para deploy e desenvolvimento.
- Documentação dos apps e padronização de READMEs por módulo.

## 📅 Próximas fases (Evolução Técnica)

### Fase 1: Inteligência Financeira & Gestão de Receita
- **Módulo de Faturamento**: Implementação do app `apps.financeiro` com suporte a `ContasAReceber`.
- **Gateways de Pagamento**: Integração com APIs externas (Asaas/Efí) para emissão de Pix e Boletos.
- **Automação de Baixa**: Webhooks para atualização automática de status de pagamento.

### Fase 2: Experiência 360º do Aluno
- **Histórico Unificado**: Timeline cronológica unificando notas, faltas, atestados e acervo.
- **Portal do Responsável**: Acesso simplificado para acompanhamento de desempenho e financeiro.
- **Secretaria Digital**: Solicitação de documentos e certidões via interface.

### Fase 3: Analytics, Preditivo e Mobile
- **Risco de Evasão**: Motor de análise baseado em tendências de notas e frequência.
- **PWA (Progressive Web App)**: Offline caching, manifest.json e notificações push para mobile.
- **Integrações EdTech**: Sincronização com Google Classroom e Microsoft Teams.

### Fase 4: Infraestrutura de Nuvem (Custo Zero)
- **Deployment Desacoplado**: Frontend no **Vercel** e Backend no **Render/Railway**.
- **Database Serverless**: Migração para **Supabase** ou **Neon** (PostgreSQL).
- **Object Storage**: Cloudinary ou AWS S3 para persistência de PDFs e imagens.

---

*Última atualização: 23 de Abril de 2026*
