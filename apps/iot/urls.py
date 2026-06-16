from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RFIDTagViewSet

router = DefaultRouter()
router.register(r'rfid', RFIDTagViewSet, basename='iot-rfid')

urlpatterns = [
    path('', include(router.urls)),
]
