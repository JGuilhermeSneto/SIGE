from django.urls import path
from .. import views

urlpatterns = [
    # Notas
    path("lancar-nota/<int:disciplina_id>/", views.lancar_nota, name="lancar_nota"),
    
    # Frequência
    path(
        "frequencia/disciplina/<int:disciplina_id>/chamada/",
        views.lancar_chamada,
        name="lancar_chamada",
    ),
    path(
        "frequencia/disciplina/<int:disciplina_id>/historico/",
        views.historico_frequencia,
        name="historico_frequencia",
    ),
    path("frequencia/aluno/", views.frequencia_aluno, name="frequencia_aluno"),
]
