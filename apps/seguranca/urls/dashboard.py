from django.urls import path
from ..views.dashboard import SecurityDashboardView

urlpatterns = [
    path("dashboard/", SecurityDashboardView.as_view(), name="dashboard"),
]
