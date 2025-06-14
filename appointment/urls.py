
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    doctor_schedule_view,
    update_appointment_view,
    patient_schedule_view,
    cancel_appointment,
    respond_appointment,
)

urlpatterns = [
    path('schedule/', doctor_schedule_view, name='doctor-schedule'),
    path('schedule/update/<uuid:appointment_id>/', update_appointment_view, name='update-appointment'),
    path('my/', patient_schedule_view, name='patient-schedule'),
    path('cancel/<uuid:appointment_id>/', cancel_appointment, name='cancel-appointment'),
    path('schedule/respond/<uuid:appointment_id>/<str:action>/', respond_appointment, name='respond-appointment'),
]
