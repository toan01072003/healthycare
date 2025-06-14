from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from user_profile.models import UserProfile

# Create your views here.
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer


@login_required
def my_medical_history_view(request):
    """Display medical record history for the logged in patient."""
    if request.user.role != "patient":
        messages.error(request, "Bạn không có quyền truy cập.")
        return redirect("home")

    records = (
        MedicalRecord.objects.filter(patient=request.user)
        .order_by("-date_uploaded")
    )
    return render(request, "medical_record/my_history.html", {"records": records})


@login_required
def search_medical_history_view(request):
    """Allow doctors to search for a patient's medical record history by name."""
    if request.user.role != "doctor":
        messages.error(request, "Bạn không có quyền truy cập.")
        return redirect("home")

    query = request.GET.get("q", "").strip()
    patients = []
    if query:
        patients = UserProfile.objects.filter(full_name__icontains=query).select_related("user")
        for p in patients:
            p.records = (
                MedicalRecord.objects.filter(patient=p.user).order_by("-date_uploaded")
            )

    return render(
        request,
        "medical_record/search_history.html",
        {"patients": patients, "query": query},
    )


@login_required
def update_medical_record_view(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id)
    if request.user.role != "doctor" and request.user != record.uploaded_by:
        messages.error(request, "Bạn không có quyền cập nhật hồ sơ này.")
        return redirect("home")

    if request.method == "POST":
        record.file_url = request.POST.get("file_url", record.file_url)
        record.summary = request.POST.get("summary", record.summary)
        rtype = request.POST.get("type", record.type)
        if rtype in dict(MedicalRecord.RECORD_TYPE_CHOICES):
            record.type = rtype
        record.save()
        messages.success(request, "Đã cập nhật hồ sơ.")
        return redirect("search-medical-history")

    return render(request, "medical_record/update_record.html", {"record": record})
