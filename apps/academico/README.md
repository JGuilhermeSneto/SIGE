# 🎓 Módulo Acadêmico

O coração do **SIGE**. Onde turmas, alunos e professores se interconectam e a mágica matemática decide, em tempo real, se um aluno será promovido ao próximo ano letivo.

## 📐 Estrutura Central (Models)

Dividido em dois sub-módulos principais:

**1. Estrutura Acadêmica (`models/academico.py`)**
- `Turma`: A célula de um ano letivo (Ex: 3º Ano A - 2026).
- `Disciplina`: O vínculo entre uma Turma, uma Matéria e um `Professor`.
- `PlanejamentoAula` & `AtividadeProfessor`: O plano de voo pedagógico do professor.
- `GradeHorario`: Determina qual dia da semana e horário o professor entra em sala.

**2. Desempenho Escolar (`models/desempenho.py`)**
- `Frequencia`: O registro de presenças ou faltas diárias para uma `Disciplina`. 
- `Nota` e `NotaAtividade`: Registros oficiais de notas bimestrais/semestrais.
- `Notificacao`: Canal assíncrono interno entre professores e alunos sobre risco de reprovação ou novas avaliações.

## ⚙️ A "Engine" de Notas

Todas as avaliações chamam o motor localizado em `utils/academico.py`. 
A função de `_calcular_situacao_nota` é executada de forma implacável:
- O aluno precisa atingir média `>= 7,0` e ter Frequência `>= 75%`.
- Se a frequência for de `74,9%` na contagem global de horas-aula, o sistema aplica o status de **Reprovado por Falta**, sobrepondo médias 10,0 intocáveis. (Essa barreira só é contornada mediante abono médico vindo do aplicativo `apps.saude`).

## 🖼️ UX Sem Interrupções (Layout de Tela Cheia)

Para o painel do Aluno, o *sidebar* de navegação universal foi completamente erradicado pela renderização do `base.html`. 
Foi aplicado um conceito de Single Page imersiva em tela cheia para evitar distrações de alunos (eliminando links redundantes no menu). Funções essenciais como a "Carteira de Mensalidades Financeiras" foram integradas dentro dos próprios *cards* de "Resumo Acadêmico" como botões de acesso rápido (`--accent-blue`).
