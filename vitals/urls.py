from .views import VitalSignsViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'vital-signs', VitalSignsViewSet)
urlpatterns = [path('', include(router.urls))]
