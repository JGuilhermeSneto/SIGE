from django.urls import path
from .. import views

urlpatterns = [
    # Dashboards (Painéis)
    path("painel/super/", views.painel_super, name="painel_super"),
    path("painel/gestor/", views.painel_super, name="painel_gestor"),
    path("painel/professor/", views.painel_professor, name="painel_professor"),
    path("painel/aluno/", views.painel_aluno, name="painel_aluno"),
    path("usuarios/", views.usuarios, name="usuarios"),
    path("usuarios/desativados/", views.listar_desativados, name="listar_desativados"),
    path("usuarios/desativar/<int:user_id>/", views.desativar_usuario, name="desativar_usuario"),
    path("usuarios/reativar/<int:user_id>/", views.reativar_usuario, name="reativar_usuario"),
    
    # Perfis
    path("editar/perfil/", views.editar_perfil, name="editar_perfil"),
    path(
        "editar/perfil/remover-foto/",
        views.remover_foto_perfil,
        name="remover_foto_perfil",
    ),
    
    # Professores
    path("professores/", views.listar_professores, name="listar_professores"),
    path("professores/cadastrar/", views.cadastrar_professor, name="cadastrar_professor"),
    path("professores/editar/<int:professor_id>/", views.editar_professor, name="editar_professor"),
    path("professores/excluir/<int:professor_id>/", views.excluir_professor, name="excluir_professor"),
    
    # Alunos
    path("alunos/", views.listar_alunos, name="listar_alunos"),
    path("alunos/cadastrar/", views.cadastrar_aluno, name="cadastrar_aluno"),
    path("alunos/editar/<int:aluno_id>/", views.editar_aluno, name="editar_aluno"),
    path("alunos/excluir/<int:aluno_id>/", views.excluir_aluno, name="excluir_aluno"),
    
    # Gestores
    path("gestores/", views.listar_gestores, name="listar_gestores"),
    path("gestores/cadastrar/", views.cadastrar_editar_gestor, name="cadastrar_gestor"),
    path("gestores/<int:gestor_id>/editar/", views.cadastrar_editar_gestor, name="editar_gestor"),
    path("gestores/excluir/<int:gestor_id>/", views.excluir_gestor, name="excluir_gestor"),
]
