"""
Views de autenticação JWT para o backend SIGE.

Esse módulo expõe:
- `POST /api/token/` para obter access/refresh tokens via e-mail, matrícula ou username.
- `POST /api/token/refresh/` para renovar um access token.
"""

from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class SIGETokenObtainPairView(APIView):
    """
    View customizada para obtenção de tokens JWT.
    Suporta login via:
    - E-mail
    - Matrícula (para alunos)
    - Username (padrão)
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        identifier = (
            request.data.get("username")
            or request.data.get("email")
            or request.data.get("matricula")
        )
        password = request.data.get("password")

        if not identifier or not password:
            return Response(
                {"detail": "Identificador (e-mail/matrícula) e senha são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # O authenticate() utiliza os backends configurados em settings.py,
        # incluindo o MatriculaAuthBackend para validar matrículas.
        user = authenticate(request, username=identifier, password=password)

        if not user:
            return Response(
                {"detail": "Credenciais inválidas ou conta inativa."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        # Dados básicos do perfil para o frontend mobile
        perfil = "desconhecido"
        if hasattr(user, "gestor"):
            perfil = "gestor"
        elif hasattr(user, "professor"):
            perfil = "professor"
        elif hasattr(user, "aluno"):
            perfil = "aluno"
        elif hasattr(user, "responsavel"):
            perfil = "responsavel"
        elif user.is_superuser:
            perfil = "admin"

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "perfil": perfil,
                    "nome": user.get_full_name() or user.username
                }
            }
        )
