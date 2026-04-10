# SIGE · Utils

Este pacote contém funções auxiliares, constantes globais e lógicas de baixo nível compartilhadas por toda a aplicação.

## Arquivos e Responsabilidades

- **`constants.py`**: Definições estáticas como horários de turno, nomes de dias da semana e outras configurações que não mudam.
- **`perfis.py`**: Helpers para manipulação de perfis de usuário, captura de nomes de exibição e redirecionamento dinâmico.
- **`academico.py`**: Funções para cálculos de notas, formatação de rendimento, contagem de faltas e processamento de grade horária.
- **`calendario.py`**: Lógica para determinar feriados móveis (ex: Páscoa) e geração de base de dados para o calendário anual.
- **`ui.py`**: Funções relacionadas à formatação de dados para visualização na interface, como geradores de matriz de calendário.
- **`filters.py`**: Lógicas de filtragem de dados (ex: busca por ano letivo) usadas em diversas listagens.
- **`__init__.py`**: Exporta os utilitários mais comuns (ex: `is_super_ou_gestor`) para facilitar o acesso de outros módulos.

## Diretrizes de Uso

- Evite colocar lógica de negócio complexa aqui; use este espaço para funções que podem ser reutilizadas em múltiplas views ou modelos.
- Mantenha funções puras (sem efeitos colaterais em banco de dados) sempre que possível para facilitar testes.
