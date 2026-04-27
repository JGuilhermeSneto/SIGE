from django.contrib import admin
from .models.perfis import Gestor, Professor, Aluno, Responsavel
from simple_history.admin import SimpleHistoryAdmin

@admin.register(Gestor)
class GestorAdmin(SimpleHistoryAdmin):
    list_display = ("nome_completo", "cargo", "instituicao")
    list_filter = ("cargo", "instituicao")
    search_fields = ("nome_completo", "cpf", "user__email")

@admin.register(Professor)
class ProfessorAdmin(SimpleHistoryAdmin):
    list_display = ("nome_completo", "area_atuacao", "instituicao")
    list_filter = ("instituicao",)
    search_fields = ("nome_completo", "cpf", "user__email")

@admin.register(Aluno)
class AlunoAdmin(SimpleHistoryAdmin):
    list_display = ("nome_completo", "turma", "status_matricula", "instituicao")
    list_filter = ("status_matricula", "turma", "instituicao")
    search_fields = ("nome_completo", "cpf", "user__email")

@admin.register(Responsavel)
class ResponsavelAdmin(SimpleHistoryAdmin):
    list_display = ("nome_completo", "parentesco", "instituicao")
    list_filter = ("parentesco", "instituicao")
    search_fields = ("nome_completo", "cpf", "user__email")
    filter_horizontal = ("alunos",)
