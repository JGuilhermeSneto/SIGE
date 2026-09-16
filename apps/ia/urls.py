from django.urls import path
from . import views

app_name = "ia"

urlpatterns = [
    path("status/", views.assistente_status, name="status"),
]
