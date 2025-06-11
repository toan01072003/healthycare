from .views import LabTestViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'lab-tests', LabTestViewSet)
urlpatterns = [path('', include(router.urls))]