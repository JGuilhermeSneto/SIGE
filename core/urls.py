from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    # ==================== AUTENTICAÇÃO ====================
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # ==================== PAINÉIS ====================
    path("painel/super/", views.painel_super, name="painel_super"),
    path("painel/gestor/", views.painel_super, name="painel_gestor"),
    path("painel/professor/", views.painel_professor, name="painel_professor"),
    path("painel/aluno/", views.painel_aluno, name="painel_aluno"),

    # ==================== PERFIL ====================
    path("editar/perfil/", views.editar_perfil, name="editar_perfil"),
    path("editar/perfil/remover-foto/", views.remover_foto_perfil, name="remover_foto_perfil"),

    # ==================== PROFESSORES ====================
    path("professores/", views.listar_professores, name="listar_professores"),
    path("professores/cadastrar/", views.cadastrar_professor, name="cadastrar_professor"),
    path("professores/editar/<int:professor_id>/", views.editar_professor, name="editar_professor"),
    path("professores/excluir/<int:professor_id>/", views.excluir_professor, name="excluir_professor"),

    # ==================== DISCIPLINAS ====================
    path("disciplinas/professor/", views.disciplinas_professor, name="disciplinas_professor"),
    path("turmas/<int:turma_id>/disciplinas/", views.disciplinas_turma, name="disciplinas_turma"),
    path("professor/turmas/<int:turma_id>/grade/", views.visualizar_grade_professor, name="visualizar_grade_professor"),
    path("lancar-nota/<int:disciplina_id>/", views.lancar_nota, name="lancar_nota"),

    # ==================== ALUNOS ====================
    path("alunos/", views.listar_alunos, name="listar_alunos"),
    path("alunos/cadastrar/", views.cadastrar_aluno, name="cadastrar_aluno"),
    path("alunos/editar/<int:aluno_id>/", views.editar_aluno, name="editar_aluno"),
    path("alunos/excluir/<int:aluno_id>/", views.excluir_aluno, name="excluir_aluno"),

    # ==================== TURMAS ====================
    path("turmas/", views.listar_turmas, name="listar_turmas"),
    path("turmas/cadastrar/", views.cadastrar_turma, name="cadastrar_turma"),
    path("turmas/editar/<int:turma_id>/", views.editar_turma, name="editar_turma"),
    path("turmas/excluir/<int:turma_id>/", views.excluir_turma, name="excluir_turma"),
    path("turmas/<int:turma_id>/grade/", views.grade_horaria, name="grade_horaria"),

    # ==================== GESTORES ====================
    path("gestores/", views.listar_gestores, name="listar_gestores"),
    path("gestores/cadastrar/", views.cadastrar_gestor, name="cadastrar_gestor"),
    path("gestores/excluir/<int:gestor_id>/", views.excluir_gestor, name="excluir_gestor"),
    path("gestores/<int:gestor_id>/editar/", views.editar_gestor, name="editar_gestor"),

    # ==================== USUÁRIOS ====================
    path("usuarios/", views.usuarios, name="usuarios"),

    # ==================== RESET DE SENHA ====================
    path(
        "senha/resetar/",
        auth_views.PasswordResetView.as_view(
            template_name="core/password_reset.html",
            email_template_name="core/password_reset_email.html",
            subject_template_name="core/password_reset_subject.txt",
            success_url="/senha/resetar/enviado/",
        ),
        name="password_reset",
    ),
    path(
        "senha/resetar/enviado/",
        auth_views.PasswordResetDoneView.as_view(template_name="core/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "senha/resetar/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="core/password_reset_confirm.html",
            success_url="/senha/resetar/completo/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "senha/resetar/completo/",
        auth_views.PasswordResetCompleteView.as_view(template_name="core/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]