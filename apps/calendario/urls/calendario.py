from django.urls import path
from ..views import calendario

urlpatterns = [
    path('calendario/', calendario.visualizar_calendario, name='visualizar_calendario'),
    path('calendario/gerar-base/', calendario.gerar_base_ano, name='gerar_base_ano'),
    path('calendario/ajustar-dia/', calendario.ajustar_dia_calendario, name='ajustar_dia_calendario'),
]
