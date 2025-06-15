from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User
from django.views.decorators.csrf import csrf_exempt  # ✅ Giữ lại
from django.contrib.auth import get_user_model
from user_profile.models import UserProfile
from vitals.models import VitalSigns
from medical_record.models import MedicalRecord
import json

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'patient')

        allowed_roles = ['patient', 'doctor', 'nurse', 'lab_staff']
        if role not in allowed_roles:
            return JsonResponse({'error': 'You are not allowed to register as ' + role}, status=403)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)

        user = User.objects.create_user(email=email, password=password, role=role)
        return JsonResponse({'message': 'Registered successfully'})

    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        User = get_user_model()

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                if user.status != 'approved' and not (user.is_staff or user.role == 'admin'):
                    return JsonResponse({'error': 'Tài khoản chưa được duyệt'}, status=403)

                # Allow login for any role so that staff accounts created via the
                # admin site behave like normal accounts.  Views can still
                # restrict access based on ``request.user.role``.

                login(request, user)
                return JsonResponse({'message': 'Login successful', 'role': user.role})
            else:
                return JsonResponse({'error': 'Sai mật khẩu'}, status=401)

        except (User.DoesNotExist, ValueError):
            return JsonResponse({'error': 'Không tìm thấy tài khoản'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def home_view(request):
    if request.user.role == 'doctor':
        return redirect('/doctor/schedule/')
    if request.user.role == 'nurse':
        return redirect('/auth/nurse/')
    if request.user.role == 'lab_staff':
        return redirect('/auth/lab/')
    return render(request, 'home.html')


@login_required
def nurse_home_view(request):
    """Simple landing page for nurses"""
    return render(request, 'nurse_home.html')


@login_required
def nurse_patient_list_view(request):
    """Show all patients for nurses to manage."""
    if request.user.role != 'nurse':
        messages.error(request, "Bạn không có quyền truy cập.")
        return redirect('home')

    patients = UserProfile.objects.filter(user__role='patient').select_related('user').order_by('full_name')
    return render(request, 'nurse_patient_list.html', {'patients': patients})


@login_required
def nurse_patient_detail_view(request, patient_id):
    """Display details, vitals and medical records for a patient."""
    if request.user.role != 'nurse':
        messages.error(request, "Bạn không có quyền truy cập.")
        return redirect('home')

    patient = get_object_or_404(User, id=patient_id, role='patient')
    profile = UserProfile.objects.filter(user=patient).first()
    vitals = VitalSigns.objects.filter(patient=patient).order_by('-recorded_at')
    records = MedicalRecord.objects.filter(patient=patient).order_by('-date_uploaded')
    context = {
        'patient': patient,
        'profile': profile,
        'vitals': vitals,
        'records': records,
    }
    return render(request, 'nurse_patient_detail.html', context)


@login_required
def lab_home_view(request):
    """Landing page for lab staff"""
    return render(request, 'lab_home.html')


@login_required
def profile_view(request):
    """Render page for viewing or editing the logged in user's profile"""
    return render(request, 'profile.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')
