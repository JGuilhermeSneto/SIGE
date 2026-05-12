# 📚 App: Biblioteca

Módulo de gerenciamento do acervo bibliográfico da instituição.

## Responsabilidades
- Cadastro de livros e periódicos (ISBN, autor, editora)
- Controle de empréstimos e devoluções
- Histórico de empréstimos por usuário
- Alertas de atraso na devolução

## Modelos Principais
- `Livro`, `Exemplar`
- `Emprestimo`, `ReservaLivro`

## Permissões
- **Aluno**: pode consultar o acervo e solicitar reservas.
- **Bibliotecário / Gestor**: gerencia empréstimos e cadastro de obras.
