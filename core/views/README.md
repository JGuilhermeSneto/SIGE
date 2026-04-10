# SIGE · Views

Este pacote contém a lógica de visualização e processamento de requisições, dividida por funcionalidades.

## Arquivos e Responsabilidades

- **`paineis.py`**: Dashboards principais para cada tipo de usuário (Superusuário, Professor, Aluno).
- **`autenticacao.py`**: Lógica de login, logout e controle de sessão.
- **`cadastros.py`**: Gerenciamento completo de usuários (listagem, criação, edição, exclusão e reativação).
- **`academico.py`**: Gestão de disciplinas, turmas e grade horária.
- **`calendario.py`**: Visualização e gerenciamento do calendário acadêmico.
- **`vida_escolar.py`**: Lógica para lançamento de notas e chamadas (frequência).
- **`perfis.py`**: Edição de perfil do usuário e gestão de fotos de perfil.
- **`__init__.py`**: Exporta todas as views para manter a compatibilidade com os caminhos de URL existentes.

## Observações para Manutenção

- Novas views devem ser colocadas no arquivo correspondente ao seu domínio funcional.
- Utilize os decoradores `@login_required` e `@user_passes_test` para garantir a segurança dos acessos.
- Funções auxiliares pesadas devem ser movidas para o pacote `utils`.
