# Exporting all views for compatibility with current URLs and apps
from .autenticacao import login_view, logout_view
from .paineis import (
    painel_super, painel_professor, painel_aluno, painel_usuarios
)
from .perfis import editar_perfil, remover_foto_perfil
from .cadastros import (
    usuarios, listar_professores, cadastrar_professor, editar_professor, excluir_professor,
    listar_alunos, cadastrar_aluno, editar_aluno, excluir_aluno,
    listar_gestores, cadastrar_editar_gestor, excluir_gestor,
    listar_turmas, cadastrar_turma, editar_turma, excluir_turma,
    listar_desativados, reativar_usuario, desativar_usuario
)
from .calendario import visualizar_calendario, ajustar_dia_calendario, gerar_base_ano
from .academico import (
    visualizar_disciplinas, cadastrar_disciplina_para_turma, editar_disciplina,
    listar_disciplinas_turma, disciplinas_turma, visualizar_grade_professor,
    grade_horaria, disciplinas_professor, excluir_disciplina
)
from .vida_escolar import (
    lancar_nota, lancar_chamada, historico_frequencia, frequencia_aluno,
    _calcular_situacao_aluno, _coletar_notas_aluno
)
