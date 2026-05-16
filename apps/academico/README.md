# 🎓 App: Acadêmico (v1.6.0)

Módulo responsável por toda a gestão pedagógica do SIGE.

![Testes](https://img.shields.io/badge/Testes-49%2F49%20passed-brightgreen?style=flat-square&logo=pytest)
![Cobertura](https://img.shields.io/badge/Cobertura-~75%25-green?style=flat-square)

## 🚀 Novidades (v8.0 Apex)
- **Suíte de Testes 100% Estável:** Todos os 49 testes passando — views, services, utils, seletores e atividades.
- **Service Layer Pattern:** Lógica de negócios centralizada em `services/` para maior manutenibilidade.
- **Notificações Unificadas:** Sistema `Notificacao` integrado para alunos, professores e gestores.
- **Gestão de Grade Horária:** Sistema inteligente de horários com validação de disponibilidade de professores.
- **Geração de Histórico Escolar:** Relatórios em PDF com QR Code de autenticidade.
- **Banco de Questões & Gabarito:** Controle de liberação manual/automática de gabaritos por atividade.

## 📊 Cobertura de Testes

| Arquivo de Teste | Testes | Status |
|---|:---:|:---:|
| `test_academico_selectors_relatorios.py` | 1 | ✅ |
| `test_academico_service.py` | 3 | ✅ |
| `test_academico_utils.py` | 5 | ✅ |
| `test_academico_utils_filtros.py` | 4 | ✅ |
| `test_academico_utils_interface_usuario.py` | 2 | ✅ |
| `test_academico_views.py` | 8 | ✅ |
| `test_atividade_servico.py` | 7 | ✅ |
| `test_views_academico.py` | 19 | ✅ |
| **Total** | **49** | **✅ 100%** |

## Modelos Principais
- `Turma`, `Disciplina`, `GradeHorario`, `MaterialDidatico`
- `Nota`, `NotaAtividade`, `Frequencia`
- `AtividadeProfessor`, `Questao`, `Alternativa`, `EntregaAtividade`
- `Notificacao`, `RiscoEvasao`, `RubricaAvaliacao`

## Permissões
- **Professor**: lança notas, frequência e atividades das próprias turmas.
- **Gestor/Admin**: visão global e edição de qualquer turma/disciplina.
- **Aluno**: acesso às próprias atividades, entregas e notificações.
