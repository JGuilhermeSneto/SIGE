"""
Rotas do módulo de relatórios (painel, PDF, busca AJAX de alunos).

O que é: prefixo ``/academico/relatorios/`` definido no ``urls`` do app;
delega a ``views.relatorios``.
"""

from django.urls import path
from ..views import relatorios

urlpatterns = [
    path('', relatorios.painel_relatorios, name='painel_relatorios'),
    path('historico/<int:aluno_id>/', relatorios.exportar_historico_pdf, name='exportar_historico'),
    path('buscar-alunos/', relatorios.buscar_alunos_ajax, name='buscar_alunos_ajax'),
]
