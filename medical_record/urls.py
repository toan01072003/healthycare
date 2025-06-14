from .views import (
    MedicalRecordViewSet,
    my_medical_history_view,
    add_medical_record_view,
    search_medical_history_view,
    update_medical_record_view,
)
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'medical-records', MedicalRecordViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('my-history/', my_medical_history_view, name='my-medical-history'),
    path('add/', add_medical_record_view, name='add-medical-record'),
    path('search-history/', search_medical_history_view, name='search-medical-history'),
    path('update/<uuid:record_id>/', update_medical_record_view, name='update-medical-record'),
]
