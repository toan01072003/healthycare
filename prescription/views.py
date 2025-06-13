from django.shortcuts import render
from rest_framework import viewsets

# Create your views here.
from .models import PrescriptionHeader, PrescriptionItem
from .serializers import PrescriptionHeaderSerializer, PrescriptionItemSerializer

class PrescriptionHeaderViewSet(viewsets.ModelViewSet):
    queryset = PrescriptionHeader.objects.all()
    serializer_class = PrescriptionHeaderSerializer


class PrescriptionItemViewSet(viewsets.ModelViewSet):
    queryset = PrescriptionItem.objects.all()
    serializer_class = PrescriptionItemSerializer
