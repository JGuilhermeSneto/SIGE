from django.urls import path
from . import views

urlpatterns = [
    path('aluno/<int:aluno_id>/', views.visualizar_saude_aluno, name='visualizar_saude_aluno'),
    path('aluno/<int:aluno_id>/editar/', views.editar_ficha_medica, name='editar_ficha_medica'),
    path('vacina/adicionar/<int:ficha_id>/', views.adicionar_vacina, name='adicionar_vacina'),
]
