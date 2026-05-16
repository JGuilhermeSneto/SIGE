from django.contrib import admin
from .models import (
    Turma, Disciplina, GradeHorario, AtividadeProfessor,
    Questao, Alternativa, EntregaAtividade, RespostaAluno,
    PlanejamentoAula, MaterialDidatico, Frequencia, Nota,
    NotaAtividade, Notificacao, RubricaAvaliacao, QuestaoBanco,
    AlternativaBanco, ProvaGerada, RiscoEvasao
)

@admin.register(RiscoEvasao)
class RiscoEvasaoAdmin(admin.ModelAdmin):
    list_display = ("aluno", "score", "ultima_atualizacao")
    list_filter = ("score",)

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ("nome", "turno", "ano")
    list_filter = ("turno", "ano")
    search_fields = ("nome",)

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ("nome", "professor", "turma")
    list_filter = ("turma", "professor")
    search_fields = ("nome",)

@admin.register(GradeHorario)
class GradeHorarioAdmin(admin.ModelAdmin):
    list_display = ("turma", "dia", "horario", "disciplina")
    list_filter = ("turma", "dia")

@admin.register(AtividadeProfessor)
class AtividadeProfessorAdmin(admin.ModelAdmin):
    list_display = ("titulo", "tipo", "disciplina", "data")
    list_filter = ("tipo", "disciplina")
    search_fields = ("titulo",)

@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ("aluno", "disciplina", "media")
    list_filter = ("disciplina",)
    search_fields = ("aluno__nome_completo",)

@admin.register(Frequencia)
class FrequenciaAdmin(admin.ModelAdmin):
    list_display = ("aluno", "disciplina", "data", "presente")
    list_filter = ("disciplina", "data", "presente")

@admin.register(RubricaAvaliacao)
class RubricaAvaliacaoAdmin(admin.ModelAdmin):
    list_display = ("nome", "aluno", "nota", "data_avaliacao")
    list_filter = ("nome", "data_avaliacao")

@admin.register(QuestaoBanco)
class QuestaoBancoAdmin(admin.ModelAdmin):
    list_display = ("enunciado", "disciplina", "nivel", "tipo")
    list_filter = ("disciplina", "nivel", "tipo")
    search_fields = ("enunciado",)

@admin.register(ProvaGerada)
class ProvaGeradaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "disciplina", "turma", "data_geracao")
    list_filter = ("disciplina", "turma")

# Registros simples para os demais
admin.site.register(Questao)
admin.site.register(Alternativa)
admin.site.register(EntregaAtividade)
admin.site.register(RespostaAluno)
admin.site.register(PlanejamentoAula)
admin.site.register(MaterialDidatico)
admin.site.register(NotaAtividade)
admin.site.register(Notificacao)
admin.site.register(AlternativaBanco)
