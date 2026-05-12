from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    path(
        "dashboard/",
        RedirectView.as_view(pattern_name="ti:seguranca", query_string=False),
        name="dashboard",
    ),
]
