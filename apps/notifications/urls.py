from django.urls import path
from .views import RegisterDeviceTokenView, UnregisterDeviceTokenView

app_name = 'notifications'

urlpatterns = [
    path('register-token/', RegisterDeviceTokenView.as_view(), name='register_token'),
    path('unregister-token/', UnregisterDeviceTokenView.as_view(), name='unregister_token'),
]
