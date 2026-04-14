"""
Rotas de notas e frequência (lançamento e histórico por disciplina).

O que é: expõe as views em ``views.vida_escolar`` para professores registrarem
chamada e notas vinculadas a ``Disciplina``.
"""

from django.urls import path
from ..views import vida_escolar

urlpatterns = [
    # Notas
    path("lancar-nota/<int:disciplina_id>/", vida_escolar.lancar_nota, name="lancar_nota"),
    
    # Frequência
    path(
        "frequencia/disciplina/<int:disciplina_id>/chamada/",
        vida_escolar.lancar_chamada,
        name="lancar_chamada",
    ),
    path(
        "frequencia/disciplina/<int:disciplina_id>/historico/",
        vida_escolar.historico_frequencia,
        name="historico_frequencia",
    ),
    path("frequencia/aluno/", vida_escolar.frequencia_aluno, name="frequencia_aluno"),
]
