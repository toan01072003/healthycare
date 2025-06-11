from django.shortcuts import render
from rest_framework import viewsets

# Create your views here.
from .models import PharmacyItem, DispensedMedicine
from .serializers import PharmacyItemSerializer, DispensedMedicineSerializer

class PharmacyItemViewSet(viewsets.ModelViewSet):
    queryset = PharmacyItem.objects.all()
    serializer_class = PharmacyItemSerializer

class DispensedMedicineViewSet(viewsets.ModelViewSet):
    queryset = DispensedMedicine.objects.all()
    serializer_class = DispensedMedicineSerializer