
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import doctor_schedule_view, update_appointment_view, patient_schedule_view

urlpatterns = [
    path('schedule/', doctor_schedule_view, name='doctor-schedule'),
    path('schedule/update/<uuid:appointment_id>/', update_appointment_view, name='update-appointment'),
    path('my/', patient_schedule_view, name='patient-schedule'),
]
