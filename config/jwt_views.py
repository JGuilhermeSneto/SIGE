"""
Views de autenticação JWT para o backend SIGE.

Esse módulo expõe:
- `POST /api/token/` para obter access/refresh tokens via e-mail e senha.
- `POST /api/token/refresh/` para renovar um access token.
"""

from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class EmailTokenObtainPairView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"detail": "E-mail e senha são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "Credenciais inválidas."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = authenticate(username=user_obj.username, password=password)
        if not user or not user.is_active:
            return Response(
                {"detail": "Credenciais inválidas."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        )
