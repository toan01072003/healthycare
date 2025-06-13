from .views import DispensationViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'dispensations', DispensationViewSet)
urlpatterns = [path('', include(router.urls))]

