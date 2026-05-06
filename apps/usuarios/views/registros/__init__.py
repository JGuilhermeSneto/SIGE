"""
Pacote de views para registros administrativos.
"""

from .comum import usuarios, listar_desativados, reativar_usuario, desativar_usuario
from .professor import listar_professores, cadastrar_professor, editar_professor, excluir_professor
from .aluno import listar_alunos, cadastrar_aluno, editar_aluno, excluir_aluno
from .gestor import listar_gestores, cadastrar_editar_gestor, excluir_gestor
