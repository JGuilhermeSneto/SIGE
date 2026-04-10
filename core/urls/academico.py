from django.urls import path
from .. import views

urlpatterns = [
    # Turmas
    path("turmas/", views.listar_turmas, name="listar_turmas"),
    path("turmas/cadastrar/", views.cadastrar_turma, name="cadastrar_turma"),
    path("turmas/editar/<int:turma_id>/", views.editar_turma, name="editar_turma"),
    path("turmas/excluir/<int:turma_id>/", views.excluir_turma, name="excluir_turma"),
    path("turmas/<int:turma_id>/grade/", views.grade_horaria, name="grade_horaria"),
    
    # Disciplinas
    path("disciplinas/professor/", views.disciplinas_professor, name="disciplinas_professor"),
    path("turmas/<int:turma_id>/disciplinas/", views.disciplinas_turma, name="disciplinas_turma"),
    path("turmas/<int:turma_id>/disciplinas/cadastrar/", views.cadastrar_disciplina_para_turma, name="cadastrar_disciplina_turma"),
    path("turmas/<int:turma_id>/disciplinas/listar/", views.listar_disciplinas_turma, name="listar_disciplinas_turma"),
    path("disciplinas/<int:disciplina_id>/visualizar/", views.visualizar_disciplinas, name="visualizar_disciplinas"),
    path("disciplinas/<int:disciplina_id>/editar/", views.editar_disciplina, name="editar_disciplina"),
    path("disciplinas/<int:disciplina_id>/excluir/", views.excluir_disciplina, name="excluir_disciplina"),
    path("professor/turmas/<int:turma_id>/grade/", views.visualizar_grade_professor, name="visualizar_grade_professor"),
]
