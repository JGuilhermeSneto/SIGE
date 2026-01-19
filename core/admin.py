
from django.contrib import admin
from .models import Gestor

@admin.register(Gestor)
class GestorAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'cpf', 'cargo', 'cidade', 'uf']
    list_filter = ['cargo', 'uf']
    search_fields = ['nome_completo', 'cpf', 'cidade']
    readonly_fields = ['criado_em', 'atualizado_em']