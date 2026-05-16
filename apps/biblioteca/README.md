# 📚 App: Biblioteca (v1.1)

Módulo de acervo digital e gestão de empréstimos do SIGE.

![Testes](https://img.shields.io/badge/Testes-Parcial-orange?style=flat-square&logo=pytest)
![Cobertura](https://img.shields.io/badge/Cobertura-~60%25-yellow?style=flat-square)

## Responsabilidades
- Catálogo de livros e materiais do acervo escolar
- Controle de empréstimos e devoluções
- Reservas online por alunos
- Relatórios de utilização do acervo

## Modelos Principais
- `Livro`, `Emprestimo`, `Reserva`, `Categoria`

## Permissões
- **Bibliotecário/Gestor**: gestão completa do acervo
- **Professor**: consulta e reserva de materiais
- **Aluno**: consulta, reserva e renovação de empréstimos

## ⚠️ Status QA (v8.0 Apex)
A suíte de testes da biblioteca está em estabilização parcial. Algumas views de cadastro e listagem apresentam falhas de fixture que estão na fila de correção.

| Área | Status |
|---|:---:|
| Listagem básica | ✅ Estável |
| Cadastro/edição | ⚠️ Em correção |
| Empréstimos | ⚠️ Em correção |
