from django.urls import path
from . import views

urlpatterns = [
    path("faturas/", views.listar_faturas, name="listar_faturas"),
    path("relatorio/", views.relatorio_financeiro, name="relatorio_financeiro"),
]
