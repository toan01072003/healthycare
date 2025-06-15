from .views import (
    VitalSignsViewSet,
    my_vitals_view,
    add_vital_sign_view,
    vital_detail_view,
)
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'vital-signs', VitalSignsViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('my/', my_vitals_view, name='my-vitals'),
    path('add/', add_vital_sign_view, name='add-vital-sign'),
    path('detail/<uuid:vital_id>/', vital_detail_view, name='vital-detail'),
]
