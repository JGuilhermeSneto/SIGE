"""
Admin configuration for core app models.

Define as configurações de exibição, filtros e buscas para os modelos
registrados no painel administrativo do Django.
"""

from django.contrib import admin

from .models import Gestor


@admin.register(Gestor)
class GestorAdmin(admin.ModelAdmin):
    """
    Classe de administração para o modelo Gestor.

    Controla como os registros de gestores são exibidos,
    filtrados e pesquisados no Django Admin.
    """

    # Define os campos exibidos na listagem principal do admin
    list_display = [
        "nome_completo",  # Nome completo do gestor
        "cpf",  # CPF do gestor
        "cargo",  # Cargo ocupado
        "cidade",  # Cidade de atuação
        "estado",  # Estado (corrigido de 'uf' para 'estado')
    ]

    # Define os filtros disponíveis na lateral do admin
    list_filter = [
        "cargo",  # Filtro por cargo
        "estado",  # Filtro por estado (corrigido)
    ]

    # Define os campos utilizados na busca
    search_fields = [
        "nome_completo",  # Busca por nome
        "cpf",  # Busca por CPF
        "cidade",  # Busca por cidade
    ]

    # Define campos apenas para leitura (não editáveis no admin)
    readonly_fields = [
        "criado_em",  # Data de criação do registro
        "atualizado_em",  # Data da última atualização
    ]

    # Define a ordenação padrão da listagem
    ordering = [
        "nome_completo",  # Ordena pelo nome do gestor
    ]

    # Define quantos registros aparecem por página
    list_per_page = 20
