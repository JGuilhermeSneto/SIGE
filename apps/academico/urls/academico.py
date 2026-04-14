from django.urls import path
from ..views import academico, vida_escolar

urlpatterns = [
    # Turmas
    path("turmas/", academico.listar_turmas, name="listar_turmas"),
    path("turmas/cadastrar/", academico.cadastrar_turma, name="cadastrar_turma"),
    path("turmas/editar/<int:turma_id>/", academico.editar_turma, name="editar_turma"),
    path("turmas/excluir/<int:turma_id>/", academico.excluir_turma, name="excluir_turma"),
    path("turmas/<int:turma_id>/grade/", academico.grade_horaria, name="grade_horaria"),
    
    # Disciplinas
    path("disciplinas/professor/", academico.disciplinas_professor, name="disciplinas_professor"),
    path("turmas/<int:turma_id>/disciplinas/", academico.disciplinas_turma, name="disciplinas_turma"),
    path("turmas/<int:turma_id>/disciplinas/cadastrar/", academico.cadastrar_disciplina_para_turma, name="cadastrar_disciplina_turma"),
    path("turmas/<int:turma_id>/disciplinas/listar/", academico.listar_disciplinas_turma, name="listar_disciplinas_turma"),
    path("disciplinas/<int:disciplina_id>/visualizar/", academico.visualizar_disciplinas, name="visualizar_disciplinas"),
    path("disciplinas/<int:disciplina_id>/editar/", academico.editar_disciplina, name="editar_disciplina"),
    path("disciplinas/<int:disciplina_id>/excluir/", academico.excluir_disciplina, name="excluir_disciplina"),
    path("professor/turmas/<int:turma_id>/grade/", academico.visualizar_grade_professor, name="visualizar_grade_professor"),
    
    # Atividades / Provas (Professor)
    path("disciplinas/<int:disciplina_id>/atividades/", academico.listar_atividades, name="listar_atividades"),
    path("disciplinas/<int:disciplina_id>/atividades/cadastrar/", academico.cadastrar_atividade, name="cadastrar_atividade"),
    path("disciplinas/<int:disciplina_id>/atividades/<int:atividade_id>/notas/", academico.lancar_notas_atividade, name="lancar_notas_atividade"),
    path("disciplinas/<int:disciplina_id>/atividades/<int:atividade_id>/questoes/", academico.gerenciar_questoes, name="gerenciar_questoes"),
    path("disciplinas/<int:disciplina_id>/atividades/<int:atividade_id>/corrigir/<int:entrega_id>/", academico.corrigir_entrega, name="corrigir_entrega"),

    # Portal do Aluno (Atividades)
    path("meu-painel/atividades/", academico.listar_atividades_aluno, name="listar_atividades_aluno"),
    path("meu-painel/atividades/<int:atividade_id>/entregar/", academico.entregar_atividade, name="entregar_atividade"),
]

