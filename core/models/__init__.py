# Importing all models to maintain accessibility and migration compatibility
from .base import PessoaBase, UF_CHOICES, TURNO_CHOICES
from .academico import Turma, Disciplina, GradeHorario
from .perfis import Gestor, Professor, Aluno
from .desempenho import Frequencia, Nota, Presenca
from .calendario import EventoCalendario
