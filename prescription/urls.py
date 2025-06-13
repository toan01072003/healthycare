from .views import PrescriptionHeaderViewSet, PrescriptionItemViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'prescription-headers', PrescriptionHeaderViewSet)
router.register(r'prescription-items', PrescriptionItemViewSet)
urlpatterns = [path('', include(router.urls))]
