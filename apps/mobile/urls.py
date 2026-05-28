from django.urls import path, include

app_name = 'mobile'

urlpatterns = [
    path('notifications/', include('apps.notifications.urls')),
    # Futuros endpoints mobile podem ser adicionados aqui
]
