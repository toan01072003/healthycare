from django.shortcuts import render

# Create your views here.
from .models import Vitals
from .serializers import VitalsSerializer
from rest_framework import viewsets

class VitalsViewSet(viewsets.ModelViewSet):
    queryset = Vitals.objects.all()
    serializer_class = VitalsSerializer
