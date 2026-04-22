# Módulo de Usuários

## Visão geral

O app `apps.usuarios` gerencia a autenticação, perfis e painéis de usuário do SIGE. Ele centraliza o controle de acesso para alunos, professores, gestores e superusuários.

## Funcionalidades principais

- Autenticação e gerenciamento de contas de usuário.
- Perfis customizados por papel: aluno, professor, gestor e superusuário.
- Painéis de controle específicos para cada tipo de usuário.
- Fluxo de planejamento de aulas pelo professor.
- Controle de permissões com decorators como `login_required` e `user_passes_test`.

## Estrutura de pastas

- `views/` — views de autenticação, perfil e painel.
- `models/` — extensão de perfis e relacionamentos com o `User`.
- `forms/` — formulários de login, cadastro e edição.
- `urls/` — rotas e endpoints de usuário.

## Uso principal

Use este app para autenticar usuários, organizar perfis por função e disponibilizar os painéis de acesso adequados.

## Observações

O fluxo de planejamento de aulas depende de nomes de campos consistentes com o backend: `grade_id`, `disciplina_id`, `data_aula` e `conteudo`.

> Atualizado em 2026-04-22.
