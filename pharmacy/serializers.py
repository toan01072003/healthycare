

from .models import PharmacyItem, DispensedMedicine
from rest_framework import serializers

class PharmacyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacyItem
        fields = '__all__'

class DispensedMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispensedMedicine
        fields = '__all__'