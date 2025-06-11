
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from django.urls import path
from .views import doctor_schedule_view, update_appointment_view

urlpatterns = [
    path('schedule/', doctor_schedule_view, name='doctor-schedule'),
    path('schedule/update/<uuid:appointment_id>/', update_appointment_view, name='update-appointment'),
]
