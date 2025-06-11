from .views import SymptomViewSet, DiseaseViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'symptoms', SymptomViewSet)
router.register(r'diseases', DiseaseViewSet)
urlpatterns = [path('', include(router.urls))]