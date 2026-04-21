from django.urls import path
from . import views

urlpatterns = [
    path('bi/', views.dashboard_bi_academico, name='dashboard_bi_academico'),
    path('inclusao/', views.dashboard_saude_inclusao, name='dashboard_saude_inclusao'),
    path('exportar/notas/', views.exportar_notas_csv, name='exportar_notas_csv'),
    path('exportar/evasao/', views.exportar_relatorio_evasao, name='exportar_relatorio_evasao'),
    path('exportar/master/pdf/', views.exportar_master_pdf, name='exportar_master_pdf'),
]
