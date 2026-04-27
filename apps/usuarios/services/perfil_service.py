from django.contrib.auth.models import User
from django.db import transaction
from ..models.perfis import Aluno, Professor, Gestor

class PerfilService:
    @staticmethod
    @transaction.atomic
    def criar_aluno(user_data, aluno_data):
        """
        Cria um usuário e seu respectivo perfil de Aluno.
        """
        user = User.objects.create_user(**user_data)
        aluno = Aluno.objects.create(user=user, **aluno_data)
        return aluno

    @staticmethod
    @transaction.atomic
    def criar_professor(user_data, professor_data):
        """
        Cria um usuário e seu respectivo perfil de Professor.
        """
        user = User.objects.create_user(**user_data)
        professor = Professor.objects.create(user=user, **professor_data)
        return professor
