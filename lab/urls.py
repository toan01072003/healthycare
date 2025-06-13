from .views import LabResultViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'lab-results', LabResultViewSet)
urlpatterns = [path('', include(router.urls))]
