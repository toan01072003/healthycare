from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import User
from django.views.decorators.csrf import csrf_exempt  # ✅ Giữ lại
from django.contrib.auth import get_user_model
import json

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'patient')

        if role != 'patient':
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
                if user.status != 'approved':
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
    return render(request, 'home.html')


@login_required
def profile_view(request):
    """Render page for viewing or editing the logged in user's profile"""
    return render(request, 'profile.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')
