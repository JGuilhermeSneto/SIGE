from django.urls import re_path
from ..views.seguranca_acoes import honeypot_view

urlpatterns = [
    re_path(r'^.*$', honeypot_view, name="honeypot_trap"),
]
