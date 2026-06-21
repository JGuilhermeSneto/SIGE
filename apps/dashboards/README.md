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

## 📱 Integração Mobile (Junho 2026)
- Os dados de desempenho do aluno são consumidos pelo **SIGE Mobile** via `GET /api/v1/aluno/dashboard/`.
- A resposta inclui médias de notas, frequência e `foto_url` para o card de perfil no app.

## Dependências
- `Chart.js` para visualizações (web)
- `react-native-svg` para gráficos no SIGE Mobile
- `apps.academico`, `apps.financeiro`, `apps.saude` para as fontes de dados

---
> Atualizado em Junho de 2026 — Suporte a consumo via API REST pelo SIGE Mobile.
