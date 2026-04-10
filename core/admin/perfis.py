from django.contrib import admin
from ..models import Gestor, Professor, Aluno

@admin.register(Gestor)
class GestorAdmin(admin.ModelAdmin):
    list_display = ["nome_completo", "cpf", "cargo", "cidade", "estado"]
    list_filter = ["cargo", "estado"]
    search_fields = ["nome_completo", "cpf", "cidade"]
    readonly_fields = ["criado_em", "atualizado_em"]
    ordering = ["nome_completo"]
    list_per_page = 20

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ["nome_completo", "cpf", "area_atuacao", "formacao"]
    list_filter = ["area_atuacao", "estado"]
    search_fields = ["nome_completo", "cpf"]
    readonly_fields = ["criado_em", "atualizado_em"]
    ordering = ["nome_completo"]
    list_per_page = 20

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ["nome_completo", "cpf", "turma", "responsavel1"]
    list_filter = ["turma", "estado"]
    search_fields = ["nome_completo", "cpf", "responsavel1"]
    readonly_fields = ["criado_em", "atualizado_em"]
    ordering = ["nome_completo"]
    list_per_page = 20
