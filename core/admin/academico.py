from django.contrib import admin
from ..models import Turma, Disciplina, GradeHorario

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ["nome", "ano", "turno"]
    list_filter = ["ano", "turno"]
    search_fields = ["nome"]
    ordering = ["-ano", "nome"]

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ["nome", "turma", "professor"]
    list_filter = ["turma", "professor"]
    search_fields = ["nome"]
    ordering = ["turma", "nome"]

@admin.register(GradeHorario)
class GradeHorarioAdmin(admin.ModelAdmin):
    list_display = ["turma", "disciplina", "dia", "horario"]
    list_filter = ["turma", "dia"]
    search_fields = ["disciplina__nome"]
