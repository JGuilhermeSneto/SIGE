"""
Views JSON mínimas para integração com o front-end (Vite/React).

Rotas sob ``/api/`` permitem verificar conectividade sem autenticação.
"""

from apps.academico.models.academico import Disciplina, Turma
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def ping(_request: Request) -> Response:
    """Resposta simples para o front confirmar que o back-end está no ar."""
    return Response({"ok": True, "service": "SIGE"})


@api_view(["GET"])
@permission_classes([AllowAny])
def dashboard_resumo(_request: Request) -> Response:
    """Totais e amostra de turmas lidos do banco (dados reais do SIGE)."""
    turmas_qs = Turma.objects.order_by("-ano", "nome")[:12]
    turmas = [
        {
            "id": t.id,
            "nome": t.nome,
            "turno": t.get_turno_display(),
            "ano": t.ano,
        }
        for t in turmas_qs
    ]
    return Response(
        {
            "totais": {
                "turmas": Turma.objects.count(),
                "disciplinas": Disciplina.objects.count(),
            },
            "turmas": turmas,
        }
    )
