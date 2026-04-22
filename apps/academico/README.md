# Módulo Acadêmico

## Visão geral

O app `apps.academico` concentra as regras de negócio acadêmicas do SIGE: turmas, disciplinas, grade horária, atividades, notas, frequência e relatórios.

## Funcionalidades principais

- Cadastro e gestão de turmas, séries e turnos.
- Associação de disciplinas a turmas e professores.
- Planejamento e registro de aulas.
- Controle de frequência e justificativas.
- Lançamento de notas e cálculo de situação acadêmica.
- Relatórios por turma, aluno e disciplina.

## Estrutura de pastas

- `models/` — entidades como `Turma`, `Disciplina`, `Grade`, `Atividade` e `Nota`.
- `views/` — views para gestão acadêmica e relatórios.
- `forms/` — formulários de cadastro de conteúdo acadêmico.
- `services/` — lógica de negócio e cálculos.
- `selectors/` — consultas otimizadas ao banco.

## Uso principal

Este módulo é o núcleo do processo acadêmico: dados de turma, planejamento de aulas e cálculo de situação escolar.

## Observações

As views do módulo validam parâmetros de grade e disciplina e esperam que o frontend envie `grade_id`, `disciplina_id`, `data_aula` e `conteudo` quando o professor salvar seu planejamento.

> Atualizado em 2026-04-22.
