from django.shortcuts import render

# Create your views here.
from .models import LabTest
from .serializers import LabTestSerializer
from rest_framework import viewsets

class LabTestViewSet(viewsets.ModelViewSet):
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer
