# 🎓 App: Acadêmico

Módulo responsável por toda a gestão pedagógica do SIGE.

## Responsabilidades
- Cadastro e gestão de Turmas e Disciplinas
- Lançamento de Notas Bimestrais
- Registro de Frequência (Diário Digital)
- Cálculo automático de situação do aluno (Aprovado/Reprovado/Recuperação)
- Geração de Histórico Escolar em PDF (ReportLab + QR Code)

## Modelos Principais
- `Turma`, `Disciplina`, `MatrizCurricular`
- `Nota`, `Frequencia`, `Matricula`

## Permissões
- **Professor**: lança notas e frequência das próprias turmas.
- **Gestor**: visão global e edição de qualquer turma.
