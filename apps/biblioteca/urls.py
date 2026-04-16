from django.urls import path
from . import views

urlpatterns = [
    path('acervo/', views.acervo_biblioteca, name='acervo_biblioteca'),
    path('gestao/', views.gerenciar_emprestimos, name='gerenciar_emprestimos'),
    path('gestao/novo/', views.novo_emprestimo, name='novo_emprestimo'),
    path('acervo/reservar/<int:pk>/', views.reservar_livro, name='reservar_livro'),
    path('gestao/confirmar/<int:pk>/', views.confirmar_retirada, name='confirmar_retirada'),
    path('gestao/devolucao/<int:pk>/', views.registrar_devolucao, name='registrar_devolucao'),
    path('livro/novo/', views.cadastrar_livro, name='cadastrar_livro'),
]
