"""
Pacote de views para painéis (dashboards).
"""

from .gestor import painel_super, painel_gestor
from .professor import painel_professor
from .aluno import painel_aluno, painel_responsavel, toggle_controle_parental, perfil_aluno
from .comum import painel_usuarios, dashboard_redirect
