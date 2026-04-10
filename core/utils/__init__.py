"""
Utility package initialization for the core app.
Exports all utility functions and constants.
"""

from .constants import HORARIOS, DIAS_SEMANA, NOMES_DIAS
from .perfis import (
    get_nome_exibicao, get_user_profile, get_foto_perfil, redirect_user
)
from .ui import gerar_calendario
from .filters import _get_anos_filtro, _get_ano_filtro_professor
from .academico import (
    _calcular_situacao_nota, _formatar_nota, _get_turno_key,
    _get_grade_horario_turma, _get_ocupados_por_professor,
    _contar_notas_lancadas, _calcular_detalhes_disciplina,
    _acumular_notas_professor
)

# Helper function for common permission check used in views
def is_super_ou_gestor(u):
    return u.is_superuser or hasattr(u, "gestor")
