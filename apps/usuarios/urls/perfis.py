"""
Rotas de painéis por perfil, cadastro de usuários (aluno, professor, gestor)
e edição de perfil.

O que é: concentra URLs “funcionais” do SIGE após o login (dashboards e CRUD
de pessoas), ligadas às views ``paineis``, ``registros`` e ``perfis``.
"""

from django.urls import path
from ..views import perfis, react_app, registros, paineis

urlpatterns = [
    # React (Vite) dentro do layout SIGE
    path("app/vite/", react_app.app_vite_shell, name="app_vite"),
    # Dashboards (Painéis)
    path("painel/super/", paineis.painel_super, name="painel_super"),
    path("painel/gestor/", paineis.painel_super, name="painel_gestor"),
    path("painel/professor/", paineis.painel_professor, name="painel_professor"),
    path("painel/aluno/", paineis.painel_aluno, name="painel_aluno"),
    path("usuarios/", registros.usuarios, name="usuarios"),
    path("usuarios/desativados/", registros.listar_desativados, name="listar_desativados"),
    path("usuarios/desativar/<int:user_id>/", registros.desativar_usuario, name="desativar_usuario"),
    path("usuarios/reativar/<int:user_id>/", registros.reativar_usuario, name="reativar_usuario"),
    
    # Perfis
    path("editar/perfil/", perfis.editar_perfil, name="editar_perfil"),
    path(
        "editar/perfil/remover-foto/",
        perfis.remover_foto_perfil,
        name="remover_foto_perfil",
    ),
    path(
        "editar/perfil/atualizar-foto/",
        perfis.atualizar_foto_perfil,
        name="atualizar_foto_perfil",
    ),
    
    # Professores
    path("professores/", registros.listar_professores, name="listar_professores"),
    path("professores/cadastrar/", registros.cadastrar_professor, name="cadastrar_professor"),
    path("professores/editar/<int:professor_id>/", registros.editar_professor, name="editar_professor"),
    path("professores/excluir/<int:professor_id>/", registros.excluir_professor, name="excluir_professor"),
    
    # Alunos
    path("alunos/", registros.listar_alunos, name="listar_alunos"),
    path("alunos/cadastrar/", registros.cadastrar_aluno, name="cadastrar_aluno"),
    path("alunos/editar/<int:aluno_id>/", registros.editar_aluno, name="editar_aluno"),
    path("alunos/excluir/<int:aluno_id>/", registros.excluir_aluno, name="excluir_aluno"),
    
    # Gestores
    path("gestores/", registros.listar_gestores, name="listar_gestores"),
    path("gestores/cadastrar/", registros.cadastrar_editar_gestor, name="cadastrar_gestor"),
    path("gestores/<int:gestor_id>/editar/", registros.cadastrar_editar_gestor, name="editar_gestor"),
    path("gestores/excluir/<int:gestor_id>/", registros.excluir_gestor, name="excluir_gestor"),
]
