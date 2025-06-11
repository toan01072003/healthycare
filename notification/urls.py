from .views import NotificationViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet)
urlpatterns = [path('', include(router.urls))]