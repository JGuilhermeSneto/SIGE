# 🎓 App: Acadêmico (v1.6.0)

Módulo responsável por toda a gestão pedagógica do SIGE.

## 🚀 Novidades
- **Service Layer Pattern:** Lógica de negócios centralizada em `services/` para maior manutenibilidade.
- **Suíte de Testes Estável:** Cobertura de testes automatizados para fluxos críticos de turmas e notas.
- **Gestão de Grade Horária:** Sistema inteligente de horários com validação de disponibilidade de professores.
- **Geração de Histórico Escolar:** Relatórios em PDF com QR Code de autenticidade.

## Modelos Principais
- `Turma`, `Disciplina`, `MatrizCurricular`
- `Nota`, `Frequencia`, `Matricula`

## Permissões
- **Professor**: lança notas e frequência das próprias turmas.
- **Gestor**: visão global e edição de qualquer turma.
