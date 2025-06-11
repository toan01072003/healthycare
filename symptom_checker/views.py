from django.shortcuts import render
from rest_framework import viewsets

# Create your views here.
from .models import Symptom, Disease
from .serializers import SymptomSerializer, DiseaseSerializer

class SymptomViewSet(viewsets.ModelViewSet):
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer

class DiseaseViewSet(viewsets.ModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer