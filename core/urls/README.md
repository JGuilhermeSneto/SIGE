# SIGE · URLs

Organização das rotas do sistema, divididas por módulos para facilitar a localização de endpoints.

## Arquivos e Responsabilidades

- **`autenticacao.py`**: Rotas de acesso (login/logout) e fluxo de recuperação de senha.
- **`cadastros.py`**: URLs para gestão de usuários, turmas e professores.
- **`academico.py`**: Rotas para visualização de disciplinas e grade horária.
- **`calendario.py`**: Endpoints relacionados ao calendário escolar.
- **`desempenho.py`**: URLs para lançamento de notas e histórico de frequências.
- **`perfis.py`**: Rotas de edição de perfil e dashboards de usuários.
- **`__init__.py`**: Centraliza a inclusão de todos os arquivos de URL acima, sendo incluído pelo `SIGE/urls.py` principal.

## Como Adicionar Nova Rota

1. Identifique o módulo correspondente.
2. Adicione o `path` no arquivo específico utilizando o padrão de `name` para reversão de URL fácil.
3. Se o arquivo estiver correto, o import já estará configurado no `__init__.py`.
