# Roadmap de Implementação — SIGE (Sistema Integrado de Gestão Escolar)

Este documento serve como guia de maturidade para o desenvolvimento do sistema, com features agrupadas de acordo com as entregas consolidadas e as fases futuras.

## ✅ Entregas Recentes (Concluídas)
Foco massivo em usabilidade, segurança patrimonial, assistência e comunicação.

### 1. Comunicação, Murais e Design System 
*   **Mural de Avisos Dinâmico**: Postagens visíveis segmentadas com highlight visual (Gestores, Professores, Alunos e Global).
*   **Notificações de Sistema**: Lógica de logs visuais com ícones interativos e **badges globais** em tempo real no menu lateral.
*   **Design System Premium**: Unificação de todos os painéis utilizando os `tokens.css` (Mural Sidebar, UI de inputs flutuantes nativa, splash screen temática).

### 2. Emissão de Documentos Digitais
*   **Boletim Escolar PDF**: Geração via `ReportLab` garantindo layout de alta resolução, pronto para Secretaria.
*   **Declaração de Matrícula**: Documentação formal validada pelo sistema.

### 3. Assistência Acadêmica & Saúde (V3.0 Adiantada)
*   **Atestados Universais**: Workflow para todos os perfis (Alunos, Professores, Gestores).
*   **Automação Pedagógica**: Suspensão automática de aulas e justificativa de faltas via processamento de atestados.
*   **Biblioteca Digital**: Gestão de acervo expandida e páginas de catálogo de detalhes ricos de livros (cadastros, datas etc.).
*   **Saúde Escolar (Ficha Médica)**: Prontuário, medicamentos e alertas com visão de segurança segmentada.

---

## 🚀 Fase Atual (Em Desenvolvimento - Sprint Ativo)
Nossa equipe de desenvolvimento volta seu foco primário para a inteligência de dados (Dashboards BI).

### 1. Dashboards de Análise (Business Intelligence)
*   **Dashboard Gerencial Avançado**: Integração de gráficos robustos nativos e painéis de dados.
*   **Mesa de Comando do Diretor**: Relatórios numéricos em tempo real sobre evasão, cancelamentos, matrículas ativas e controle de atestados.
*   **Integração Visual**: Gráficos acoplados perfeitamente ao *Design System Premium* interativo.

### 2. Patrimônio e Históricos (Backlog Imediato)
*   **Histórico Escolar Parcial**: Relatório acumulativo do discente (pendente de consolidação na secretaria).
*   **Gestão de Estoque Total**: Fechar o fluxo do controle de Insumos da infraestrutura no painel gerencial.

---

## 📅 Versões Futuras: Ecossistema Completo

### Versão 2.0: Financeiro e RH Escolar
*   Geração de Boletos e recebimentos automatizados via API PIX.
*   Gestão de Inadimplência, acionamento de devedores e planos de pagamento.
*   Folha de pagamento atrelada à carga horária e alocação do docente.

### Versão 3.0: Convênios Internos
*   Gestão de Estágios, Termos de Compromisso e Convênios.
*   Expansão de Ficha Multidisciplinar (Psicologia e Nutrição).

### Versão 4.0: Integrações Avançadas e IA
*   Sincronização Bidirecional (Microsoft Teams / Google Classroom).
*   **Health Score Preditivo**: Rede Neural avaliando o cruzamento de faltas e comportamento avaliativo para prevenir evasão *antes* que ocorra.
*   App Mobile Nativo (PWA instalado nas lojas) com uso de caching local.
