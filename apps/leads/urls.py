from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeadViewSet, FunnelStageViewSet, LeadInteractionViewSet

router = DefaultRouter()
router.register(r'leads', LeadViewSet)
router.register(r'stages', FunnelStageViewSet)
router.register(r'interactions', LeadInteractionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
