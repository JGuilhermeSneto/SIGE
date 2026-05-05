# 📅 Módulo de Calendário & Gestão de Tempo

O app `apps.calendario` organiza o ecossistema temporal da instituição, integrando cronogramas acadêmicos, eventos institucionais e horários de aula.

## 📐 Estrutura de Dados (Models)
- `Evento`: Cadastro de datas críticas (Provas, Feriados, Reuniões).
- `HorarioAula`: Definição de grades horárias por turma e disciplina.
- `PeriodoLetivo`: Controle de semestres e trimestres com datas de trancamento.

## 🚀 Engenharia e UI
- **Calendário Dinâmico**: Interface baseada em JavaScript para visualização mensal/semanal com suporte a drag-and-drop para gestores.
- **Integração de Horários**: O sistema cruza os horários de aula com o planejamento dos professores (`apps.academico`) para evitar conflitos de sala.
- **Temas**: Visualização adaptável a todos os temas do SIGE, com destaque para eventos críticos usando `--accent-amber`.

## 🔗 Hub de Inteligência
- Exporta dados de ocupação de salas e densidade de eventos para o **Hub de Inteligência**.
- Sincronização automática com o mural de comunicados (`apps.comunicacao`).

> Atualizado em Maio de 2026 — Integração total com Grade Horária Acadêmica.

