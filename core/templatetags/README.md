# SIGE · Template Tags

Tags e filtros customizados para estender as capacidades de lógica nos templates HTML do Django.

## Bibliotecas Disponíveis

- **`get_item.py`**: Filtro essencial (`|get_item:key`) para acessar dicionários em templates, muito usado para buscar notas de alunos em dicts indexados por ID.

## Como Adicionar Nova Tag

1. Crie o arquivo `.py` no diretório.
2. Utilize o decorador `@register.filter` ou `@register.simple_tag`.
3. Certifique-se de que a biblioteca está importada no `__init__.py` para carregamento automático ou use `{% load nome_do_arquivo %}` no seu template.
