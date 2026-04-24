from django.urls import path
from . import views

app_name = "financeiro"

urlpatterns = [
    path("faturas/", views.listar_faturas, name="listar_faturas"),
    path("faturas/<int:fatura_id>/", views.detalhes_fatura, name="detalhes_fatura"),
    path("despesas/", views.gestao_despesas, name="gestao_despesas"),
    path("lancamento/novo/", views.criar_lancamento, name="criar_lancamento"),
    path("faturas/<int:fatura_id>/pagar/", views.registrar_pagamento, name="registrar_pagamento"),
    path("faturas/<int:fatura_id>/notificar/", views.notificar_fatura, name="notificar_fatura"),
    path("painel/", views.painel_financeiro, name="painel_financeiro"),
]
