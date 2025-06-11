from .views import PrescriptionViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'prescriptions', PrescriptionViewSet)
urlpatterns = [path('', include(router.urls))] 