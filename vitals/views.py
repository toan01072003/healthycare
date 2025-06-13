from django.shortcuts import render

# Create your views here.
from .models import VitalSigns
from .serializers import VitalSignsSerializer
from rest_framework import viewsets

class VitalSignsViewSet(viewsets.ModelViewSet):
    queryset = VitalSigns.objects.all()
    serializer_class = VitalSignsSerializer

