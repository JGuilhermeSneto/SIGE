# 🎓 Módulo Acadêmico

O coração do **SIGE**. Onde turmas, alunos e professores se interconectam e a lógica de negócio decide, em tempo real, a situação acadêmica dos discentes.

## 📐 Estrutura Central (Models)

### 1. Estrutura Acadêmica (`models/academico.py`)
- `Turma`: A célula de um ano letivo (Ex: 3º Ano A - 2026).
- `Disciplina`: O vínculo entre Turma, Matéria e Professor.
- `PlanejamentoAula` & `AtividadeProfessor`: O plano de voo pedagógico.
- `GradeHorario`: Gestão de horários e conflitos.

### 2. Desempenho Escolar (`models/desempenho.py`)
- `Frequencia`: Registro diário de presença. 
- `Nota` e `NotaAtividade`: Registros oficiais de avaliações.
- **Notificacao (Unificada)**: Engine global de notificações que atende a todos os módulos do sistema.

## 🚀 Engenharia e Performance

- **NotificacaoServico**: Camada de serviço global para envio de alertas automáticos para usuários, turmas, gestores e toda a instituição.
- **Selectors Pattern**: Camada de consultas otimizadas em `selectors/` que reduz consultas N+1 de O(n) para O(1).
- **Service Layer**: Lógica de negócio centralizada em `services/` (Cálculo de médias, situações automáticas e integração de notificações).
- **Integração BI**: Os dados acadêmicos alimentam o **Hub de Inteligência** (`apps.dashboards`) via Seletores compartilhados.

## 📄 Emissão de Documentos
- Integração com o novo motor **ReportLab** para geração de:
    - Boletins Escolares com QR Code.
    - Declarações de Matrícula.
    - Histórico Escolar Consolidado.

## 🧠 Regras de Aprovação
- **Aprovação**: Média `>= 7,0` E Frequência `>= 75%`.
- **Reprovado por Falta**: Frequência `< 75%` (Sobrepõe qualquer nota).
- **Abono**: Apenas via fluxo oficial no módulo `apps.saude` com notificação automática.

> Atualizado em Maio de 2026 — Notificações Unificadas e Shield v1.2 integrados.
