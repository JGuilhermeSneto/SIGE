from django.urls import path
from .. import views

urlpatterns = [
    path('calendario/', views.visualizar_calendario, name='visualizar_calendario'),
    path('calendario/gerar-base/', views.gerar_base_ano, name='gerar_base_ano'),
    path('calendario/ajustar-dia/', views.ajustar_dia_calendario, name='ajustar_dia_calendario'),
]
