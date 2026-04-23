# 💰 Módulo Financeiro (SIGE)

O módulo **Financeiro** é responsável pela gestão de faturamento, mensalidades e indicadores econômicos da instituição. Ele permite que alunos visualizem suas faturas e gestores acompanhem a saúde financeira global do campus.

## 🚀 Funcionalidades Principais

- **Gestão de Faturas**: Listagem dinâmica de faturas com filtros por status (Pendente, Pago, Atrasado).
- **Dashboard de BI (Gestor)**: KPIs financeiros em tempo real:
  - Total Arrecadado.
  - Total a Receber.
  - Índice de Inadimplência.
- **Automação de Status**: Transição automática para `ATRASADO` baseada na data de vencimento.
- **Interface Premium**: Design consistente com o sistema de tokens, incluindo gráficos de barras CSS e badges vibrantes.

## 🛠️ Detalhes Técnicos

- **Models**: `Fatura` e `Pagamento`.
- **Views**: 
  - `listar_faturas`: Dashboard do aluno e lista geral para gestores.
  - `relatorio_financeiro`: Painel analítico exclusivo para alta gestão.
- **Segurança**: Isolamento de dados (Alunos só veem suas próprias faturas).

## 📊 Gráficos
O módulo utiliza uma implementação personalizada de gráficos via CSS (sem bibliotecas pesadas) para garantir performance e alinhamento visual com o tema dark do SIGE.
