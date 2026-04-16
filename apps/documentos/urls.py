from django.urls import path
from . import views

urlpatterns = [
    path('declaracao/<int:aluno_id>/', views.gerar_declaracao_matricula, name='gerar_declaracao_matricula'),
    path('boletim/<int:aluno_id>/', views.gerar_boletim_pdf, name='gerar_boletim_pdf'),
]
