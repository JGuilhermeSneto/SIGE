from django.urls import path
from . import views

urlpatterns = [
    path('bi/', views.dashboard_bi_academico, name='dashboard_bi_academico'),
    path('exportar/notas/', views.exportar_notas_csv, name='exportar_notas_csv'),
]
