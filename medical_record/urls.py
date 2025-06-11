from .views import MedicalRecordViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'medical-records', MedicalRecordViewSet)
urlpatterns = [path('', include(router.urls))]