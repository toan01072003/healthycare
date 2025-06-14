from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, MyProfileView

router = DefaultRouter()
router.register(r'user-profiles', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('me/', MyProfileView.as_view(), name='my-profile'),
]