"""
Admin package initialization for the core app.
Registers all models in the admin panel by importing their modules.
"""

from .perfis import GestorAdmin, ProfessorAdmin, AlunoAdmin
from .academico import TurmaAdmin, DisciplinaAdmin, GradeHorarioAdmin
from .desempenho import FrequenciaAdmin, NotaAdmin
