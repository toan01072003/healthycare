from .views import AuditLogViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'audit-logs', AuditLogViewSet)
urlpatterns = [path('', include(router.urls))]