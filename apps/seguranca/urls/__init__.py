from django.urls import include, path

app_name = "seguranca"

urlpatterns = [
    path("", include("apps.seguranca.urls.dashboard")),
    path("", include("apps.seguranca.urls.acoes")),
]
