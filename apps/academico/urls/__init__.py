from django.urls import path, include

urlpatterns = [
    path("", include("apps.academico.urls.academico")),
    path("", include("apps.academico.urls.desempenho")),
    path("relatorios/", include("apps.academico.urls.relatorios")),
]
