from django.contrib import admin
from ..models import Frequencia, Nota, Presenca

@admin.register(Frequencia)
class FrequenciaAdmin(admin.ModelAdmin):
    list_display = ["aluno", "disciplina", "data", "presente"]
    list_filter = ["presente", "data", "disciplina"]
    search_fields = ["aluno__nome_completo", "disciplina__nome"]
    date_hierarchy = "data"

@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ["aluno", "disciplina", "media"]
    list_filter = ["disciplina"]
    search_fields = ["aluno__nome_completo", "disciplina__nome"]
    readonly_fields = ["media"]

