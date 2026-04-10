# SIGE · Templates

Repositório de arquivos HTML que formam a interface do usuário. A estrutura segue a organização dos domínios da aplicação.

## Estrutura de Pastas

- **`core/`**: Templates globais do sistema (Painéis principais, Listagem de usuários, Calendário).
- **`auth/`**: Fluxo de autenticação e redefinição de senha premium.
- **`aluno/`**: Páginas específicas para visão e ações do aluno.
- **`professor/`**: Interfaces de gestão para o corpo docente.
- **`turma/`**: Listagens e gerenciamento de turmas e grade horária.
- **`disciplina/`**: Detalhes e gestão de disciplinas acadêmicas.
- **`gestor/`**: Áreas administrativas exclusivas para a gestão escolar.

## Base e Herança

- **`core/base.html`**: O arquivo base mestre que contém o layout, menus e carregamento de assets globais. Todos os outros templates devem estender (`{% extends %}`) este arquivo.
- **`core/usuarios.html`**: Exemplo de implementação premium que serve de base estética para novos módulos.

## Convenções UI/UX

1. Use sempre Semantic HTML.
2. Identifique elementos interativos com IDs únicos para testes.
3. Utilize as variáveis do `tokens.css` via classes utilitárias ou estilos inline se necessário apenas para ajustes finos.
