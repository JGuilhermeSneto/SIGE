from django.urls import path
from . import views

urlpatterns = [
    path('aluno/<int:aluno_id>/', views.visualizar_saude_aluno, name='visualizar_saude_aluno'),
    path('aluno/<int:aluno_id>/editar/', views.editar_ficha_medica, name='editar_ficha_medica'),
    path('vacina/adicionar/<int:ficha_id>/', views.adicionar_vacina, name='adicionar_vacina'),
    
    # Atestados
    path('meus-atestados/', views.listar_atestados_aluno, name='listar_atestados_aluno'),
    path('atestados/enviar/', views.enviar_atestado, name='enviar_atestado'),
    path('gestao/atestados/', views.gestao_atestados, name='gestao_atestados'),
    path('gestao/atestados/<int:atestado_id>/revisar/', views.revisar_atestado, name='revisar_atestado'),
]
