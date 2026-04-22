# Módulo de Biblioteca

## Visão geral

O app `apps.biblioteca` gerencia o acervo escolar, empréstimos e devoluções de livros.

## Funcionalidades principais

- Cadastro de livros com autor, editora e estoque.
- Empréstimos e devoluções de obras.
- Limite de livros por aluno.
- Painel de gerenciamento de reservas.

## Estrutura de pastas

- `models/` — livros, categorias e empréstimos.
- `views.py` — catálogo, histórico e administração.
- `forms.py` — formulários de cadastro e empréstimos.
- `templates/` — páginas de biblioteca e relatórios.

## Uso principal

Use este app para controlar o fluxo de empréstimo e a disponibilidade do acervo.

## Observações

O sistema aplica limites de reserva e bloqueia tentativas além do estoque disponível.

> Atualizado em 2026-04-22.
