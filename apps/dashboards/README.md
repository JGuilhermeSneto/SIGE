# 📊 App: Dashboards

Hub de Inteligência e Business Intelligence (BI) do SIGE.

## Responsabilidades
- Dashboard unificado com métricas acadêmicas e financeiras
- Motor de Risco de Evasão (predição baseada em frequência e notas)
- Relatórios de desempenho por turma e por aluno
- Gráficos interativos com Chart.js e dados em tempo real

## Modelos Principais
- Não possui modelos próprios — consome dados dos outros módulos via queries otimizadas.

## Permissões
- **Professor**: visualiza métricas das próprias turmas.
- **Gestor**: acesso ao hub completo com visão institucional.

## Dependências
- `Chart.js` para visualizações
- `apps.academico`, `apps.financeiro`, `apps.saude` para as fontes de dados
