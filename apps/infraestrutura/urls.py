from django.urls import path
from . import views

urlpatterns = [
    # Gestão de Infraestrutura (Acesso Gestor/Super)
    path('painel/', views.painel_infraestrutura, name='painel_infraestrutura'),
    path('patrimonio/novo/', views.cadastrar_editar_patrimonio, name='cadastrar_patrimonio'),
    path('patrimonio/editar/<int:pk>/', views.cadastrar_editar_patrimonio, name='editar_patrimonio'),
    path('estoque/movimentar/', views.registrar_movimentacao_estoque, name='registrar_movimentacao'),
]
