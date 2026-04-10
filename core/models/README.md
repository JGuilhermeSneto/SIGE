# SIGE · Models

Este pacote contém as definições do banco de dados do sistema, organizadas por domínio de responsabilidade.

## Arquivos e Responsabilidades

- **`base.py`**: Modelos fundamentais e abstratos que servem de base para outros. Inclui a lógica de tipos de usuários e campos comuns.
- **`perfis.py`**: Modelos relacionados aos usuários do sistema (Gestor, Professor, Aluno), contendo informações pessoais e vínculos com o `User` do Django.
- **`academico.py`**: Definições de Turmas e Disciplinas, formando a estrutura básica da organização escolar.
- **`desempenho.py`**: Modelos para Notas e Frequências (Chamadas), lidando com o rendimento e presença dos alunos.
- **`calendario.py`**: Definição de `EventoCalendario`, utilizado para gerir feriados, dias letivos e eventos escolares.
- **`__init__.py`**: Centraliza as exportações dos modelos para garantir que as migrations e imports funcionem de forma transparente.

## Observações para Manutenção

- Ao criar um novo modelo, escolha o arquivo que melhor representa seu domínio.
- Sempre registre o novo modelo no `__init__.py` para que ele seja detectado pelo Django.
