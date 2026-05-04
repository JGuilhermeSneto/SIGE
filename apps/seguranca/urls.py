from django.urls import path
from .views import SecurityDashboardView

app_name = "seguranca"

urlpatterns = [
    path("dashboard/", SecurityDashboardView.as_view(), name="dashboard"),
]
