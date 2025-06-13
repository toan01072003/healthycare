from .views import ChronicCareLogViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'chronic-care-logs', ChronicCareLogViewSet)
urlpatterns = [path('', include(router.urls))]
