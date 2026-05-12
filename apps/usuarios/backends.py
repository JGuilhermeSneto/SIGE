from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models.perfis import Aluno

User = get_user_model()


class MatriculaAuthBackend(ModelBackend):
    """
    Backend de autenticação que permite que Alunos façam login usando sua matrícula.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)

        # Primeiro tenta autenticar como usuário padrão (username/email)
        user = super().authenticate(
            request, username=username, password=password, **kwargs
        )
        if user:
            return user

        # Se falhar, tenta buscar pela matrícula do aluno
        try:
            aluno = Aluno.objects.get(matricula=username)
            user = aluno.user
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Aluno.DoesNotExist:
            return None

        return None
