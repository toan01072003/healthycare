from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

from .models import Appointment
from .serializers import AppointmentWithPatientSerializer
from user_profile.models import UserProfile


@login_required
def doctor_schedule_view(request):
    if request.user.role != "doctor":
        messages.error(request, "Bạn không có quyền truy cập.")
        return redirect("home")

    upcoming = (
        Appointment.objects.filter(doctor=request.user, date_time__gte=timezone.now())
        .order_by("date_time")
        .select_related("patient")
    )
    history = (
        Appointment.objects.filter(doctor=request.user, date_time__lt=timezone.now())
        .order_by("-date_time")
        .select_related("patient")
    )

    for appt in list(upcoming) + list(history):
        appt.patient_profile = UserProfile.objects.filter(user=appt.patient).first()

    return render(
        request,
        "doctor_schedule.html",
        {
            "upcoming": upcoming,
            "history": history,
        },
    )


@login_required
def update_appointment_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user)

    if request.method == "POST":
        new_status = request.POST.get("status")
        notes = request.POST.get("notes")

        if new_status in dict(Appointment.STATUS_CHOICES).keys():
            appointment.status = new_status

        appointment.notes = notes
        appointment.save()
        messages.success(request, "Cập nhật thành công.")
        return redirect("doctor-schedule")

    return redirect("doctor-schedule")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def doctor_appointments_view(request):
    user = request.user
    if user.role != "doctor":
        return Response({"error": "Only doctors can access this view."}, status=403)

    appointments = Appointment.objects.filter(doctor=user).order_by("date_time")
    serializer = AppointmentWithPatientSerializer(appointments, many=True)
    return Response(serializer.data)


from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Appointment
from rest_framework.response import Response


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_appointment_status(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id, doctor=request.user)
    except Appointment.DoesNotExist:
        return Response({"error": "Không tìm thấy lịch hẹn."}, status=404)

    new_status = request.data.get("status")
    notes = request.data.get("notes")

    if new_status:
        if new_status not in dict(Appointment.STATUS_CHOICES).keys():
            return Response({"error": "Trạng thái không hợp lệ."}, status=400)
        if new_status == "cancelled":
            appointment.delete()
            return Response({"message": "Đã hủy lịch hẹn."})
        appointment.status = new_status

    if notes is not None:
        appointment.notes = notes

    appointment.save()
    return Response({"message": "Cập nhật thành công."})


# views.py (chatbot hoặc appointment/views.py)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from appointment.models import Appointment
from user_profile.models import (
    UserProfile,
)  # Sử dụng UserProfile nếu đây là model người dùng tùy chỉnh của bạn
from django.utils.dateparse import parse_datetime


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_appointment_from_chatbot(request):
    data = request.data
    doctor_name = data.get("doctor_name")
    date_time_str = data.get("date_time")
    reason = data.get("reason", "Đặt lịch qua chatbot")

    # Chỉ cho phép bệnh nhân đặt lịch qua chatbot
    if request.user.role != "patient":
        return Response({"error": "Chỉ bệnh nhân mới được phép đặt lịch."}, status=403)

    try:
        doctor_profile = UserProfile.objects.get(
            full_name__icontains=doctor_name, user__role="doctor"
        )
        doctor = doctor_profile.user
    except UserProfile.DoesNotExist:
        return Response({"error": "Không tìm thấy bác sĩ"}, status=404)

    date_time = parse_datetime(date_time_str)
    if not date_time:
        return Response({"error": "Thời gian không hợp lệ"}, status=400)

    # Không cho phép bác sĩ và bệnh nhân trùng nhau
    if request.user == doctor:
        return Response(
            {"error": "Bác sĩ và bệnh nhân không được trùng nhau."}, status=400
        )

    # Tạo lịch hẹn
    appointment = Appointment.objects.create(
        patient=request.user,
        doctor=doctor,
        date_time=date_time,
        reason=reason,
        status="pending",
    )
    return Response(
        {
            "message": "Lịch hẹn đã được tạo",
            "appointment_id": str(appointment.id),
            "doctor": doctor_profile.full_name,
            "date_time": date_time,
            "status": appointment.status,
        }
    )


# appointment/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Appointment
from .serializers import AppointmentWithPatientSerializer
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def doctor_schedule_view_html(request):
    if request.user.role != "doctor":
        return Response({"error": "Only doctors can view this"}, status=403)
    appointments = Appointment.objects.filter(doctor=request.user).order_by("date_time")
    serializer = AppointmentWithPatientSerializer(appointments, many=True)
    return Response(serializer.data)


@login_required
def patient_schedule_view(request):
    if request.user.role != "patient":
        messages.error(request, "Bạn không có quyền truy cập.")
        return redirect("home")

    upcoming = (
        Appointment.objects.filter(patient=request.user, date_time__gte=timezone.now())
        .order_by("date_time")
        .select_related("doctor")
    )
    history = (
        Appointment.objects.filter(patient=request.user, date_time__lt=timezone.now())
        .order_by("-date_time")
        .select_related("doctor")
    )

    for appt in list(upcoming) + list(history):
        appt.doctor_profile = UserProfile.objects.filter(user=appt.doctor).first()

    return render(
        request,
        "patient_schedule.html",
        {
            "upcoming": upcoming,
            "history": history,
        },
    )


@login_required
def cancel_appointment(request, appointment_id):
    """Allow a patient to cancel their appointment."""
    appointment = get_object_or_404(
        Appointment, id=appointment_id, patient=request.user
    )
    if request.method == "POST":
        # Remove the appointment entirely when a patient cancels
        appointment.delete()
        messages.success(request, "Đã hủy lịch hẹn.")
    return redirect("patient-schedule")


@login_required
def respond_appointment(request, appointment_id, action):
    """Doctor accepts or rejects an appointment."""
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user)
    if request.method == "POST":
        if action == "accept":
            appointment.status = "confirmed"
            appointment.save()
            messages.success(request, "Đã chấp nhận lịch hẹn.")
        elif action == "reject":
            # Delete the appointment when a doctor rejects it
            appointment.delete()
            messages.success(request, "Đã từ chối lịch hẹn.")
            return redirect("doctor-schedule")
    return redirect("doctor-schedule")
