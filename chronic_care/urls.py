from .views import ChronicConditionViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'chronic-conditions', ChronicConditionViewSet)
urlpatterns = [path('', include(router.urls))]