from django.urls import path
from . import views

urlpatterns = [
    # Gestão (Acesso Gestor/Super)
    path('gestao/', views.listar_comunicados, name='listar_comunicados_gestao'),
    path('gestao/novo/', views.cadastrar_editar_comunicado, name='cadastrar_comunicado'),
    path('gestao/editar/<int:pk>/', views.cadastrar_editar_comunicado, name='editar_comunicado'),
    path('gestao/excluir/<int:pk>/', views.excluir_comunicado, name='excluir_comunicado'),
]
