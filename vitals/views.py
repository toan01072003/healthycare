from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
from .models import VitalSigns
from .serializers import VitalSignsSerializer
from rest_framework import viewsets

class VitalSignsViewSet(viewsets.ModelViewSet):
    queryset = VitalSigns.objects.all()
    serializer_class = VitalSignsSerializer


@login_required
def my_vitals_view(request):
    """Display vital sign history for the logged in patient."""
    if request.user.role != "patient":
        messages.error(request, "Bạn không có quyền truy cập.")
        return redirect("home")

    vitals = (
        VitalSigns.objects.filter(patient=request.user)
        .order_by("-recorded_at")
    )
    return render(request, "vitals/my_vitals.html", {"vitals": vitals})


@login_required
def add_vital_sign_view(request):
    """Allow a patient to add new vital sign data."""
    if request.user.role != "patient":
        messages.error(request, "Bạn không có quyền truy cập.")
        return redirect("home")

    if request.method == "POST":
        bp = request.POST.get("blood_pressure", "").strip()
        temp = request.POST.get("temperature")
        hr = request.POST.get("heart_rate")
        spo2 = request.POST.get("oxygen_saturation")
        rr = request.POST.get("respiratory_rate")

        if not all([bp, temp, hr, spo2, rr]):
            messages.error(request, "Vui lòng điền đầy đủ thông tin.")
        else:
            VitalSigns.objects.create(
                patient=request.user,
                recorded_by=request.user,
                recorded_at=timezone.now(),
                blood_pressure=bp,
                temperature=temp,
                heart_rate=hr,
                oxygen_saturation=spo2,
                respiratory_rate=rr,
            )
            messages.success(request, "Đã thêm chỉ số.")
            return redirect("my-vitals")

    return render(request, "vitals/add_vital.html")


@login_required
def vital_detail_view(request, vital_id):
    """Show details for a single vital sign entry."""
    vital = get_object_or_404(VitalSigns, id=vital_id, patient=request.user)
    if request.user.role != "patient":
        messages.error(request, "Bạn không có quyền truy cập.")
        return redirect("home")

    return render(request, "vitals/vital_detail.html", {"vital": vital})

