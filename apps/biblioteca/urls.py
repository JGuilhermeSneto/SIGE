from django.urls import path
from . import views

urlpatterns = [
    path('acervo/', views.acervo_biblioteca, name='acervo_biblioteca'),
    path('acervo/livro/<int:pk>/', views.detalhe_livro, name='detalhe_livro'),
    path('gestao/', views.gerenciar_emprestimos, name='gerenciar_emprestimos'),
    path('gestao/novo/', views.novo_emprestimo, name='novo_emprestimo'),
    path('acervo/reservar/<int:pk>/', views.reservar_livro, name='reservar_livro'),
    path('gestao/confirmar/<int:pk>/', views.confirmar_retirada, name='confirmar_retirada'),
    path('gestao/devolucao/<int:pk>/', views.registrar_devolucao, name='registrar_devolucao'),
    path('livro/novo/', views.cadastrar_livro, name='cadastrar_livro'),
    path('api/status-leitura/', views.atualizar_status_leitura, name='atualizar_status_leitura'),
]
