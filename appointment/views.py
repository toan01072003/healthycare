from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Appointment
from user_profile.models import UserProfile
from .serializers import AppointmentWithPatientSerializer

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment
from user_profile.models import UserProfile
from django.contrib import messages

@login_required
def doctor_schedule_view(request):
    if request.user.role != 'doctor':
        messages.error(request, "Bạn không có quyền truy cập.")
        return redirect('home')

    appointments = Appointment.objects.filter(doctor=request.user).order_by('date_time')
    patient_profiles = {a.patient.id: UserProfile.objects.filter(user=a.patient).first() for a in appointments}
    return render(request, 'doctor_schedule.html', {
        'appointments': appointments,
        'patient_profiles': patient_profiles,
    })

@login_required
def update_appointment_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('notes')

        if new_status in dict(Appointment.STATUS_CHOICES).keys():
            appointment.status = new_status

        appointment.notes = notes
        appointment.save()
        messages.success(request, "Cập nhật thành công.")
        return redirect('doctor-schedule')

    return redirect('doctor-schedule')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_appointments_view(request):
    user = request.user
    if user.role != 'doctor':
        return Response({"error": "Only doctors can access this view."}, status=403)

    appointments = Appointment.objects.filter(doctor=user).order_by('date_time')
    serializer = AppointmentWithPatientSerializer(appointments, many=True)
    return Response(serializer.data)


from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Appointment
from rest_framework.response import Response

@api_view(['PATCH'])
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
from user_profile.models import UserProfile  # Sử dụng UserProfile nếu đây là model người dùng tùy chỉnh của bạn
from django.utils.dateparse import parse_datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_appointment_from_chatbot(request):
    data = request.data
    doctor_name = data.get('doctor_name')
    date_time_str = data.get('date_time')
    reason = data.get('reason', 'Đặt lịch qua chatbot')

    try:
        doctor = UserProfile .objects.get(role='doctor', email__icontains=doctor_name)
    except UserProfile .DoesNotExist:
        return Response({"error": "Không tìm thấy bác sĩ"}, status=404)

    date_time = parse_datetime(date_time_str)
    if not date_time:
        return Response({"error": "Thời gian không hợp lệ"}, status=400)

    # Tạo lịch hẹn
    appointment = Appointment.objects.create(
        patient=request.user,
        doctor=doctor,
        date_time=date_time,
        reason=reason,
        status='pending'
    )
    return Response({
        "message": "Lịch hẹn đã được tạo",
        "appointment_id": str(appointment.id),
        "doctor": doctor.email,
        "date_time": date_time,
        "status": appointment.status
    })


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
