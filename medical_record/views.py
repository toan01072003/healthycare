from django.shortcuts import render
from rest_framework import viewsets

# Create your views here.
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer