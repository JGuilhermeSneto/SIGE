"""
URLs do Health Check da Área de TI — compatível com django-health-check v4.x.

A v4.x usa uma view configurável ao invés de submódulos no INSTALLED_APPS.
"""
from django.urls import path
from health_check.views import HealthCheckView


class ELISEHealthCheckView(HealthCheckView):
    """
    Health check customizado para a ELISE.
    Verifica: Banco de dados, Cache e Storage.

    Acesso: GET /health/
    Formatos: HTML (padrão), JSON (?format=json), texto (?format=text)
    """
    checks = (
        "health_check.checks.Database",
        "health_check.checks.Cache",
        "health_check.checks.Storage",
    )


urlpatterns = [
    path("", ELISEHealthCheckView.as_view(), name="health-check"),
]
