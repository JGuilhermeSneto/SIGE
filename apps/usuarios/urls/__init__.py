from django.urls import path, include

urlpatterns = [
    path("", include("apps.usuarios.urls.autenticacao")),
    path("", include("apps.usuarios.urls.perfis")),
]
