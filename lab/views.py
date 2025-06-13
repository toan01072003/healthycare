from django.shortcuts import render

# Create your views here.
from .models import LabResult
from .serializers import LabResultSerializer
from rest_framework import viewsets

class LabResultViewSet(viewsets.ModelViewSet):
    queryset = LabResult.objects.all()
    serializer_class = LabResultSerializer

