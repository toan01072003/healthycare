from rest_framework import serializers
from .models import PrescriptionHeader, PrescriptionItem

class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionItem
        fields = '__all__'

class PrescriptionHeaderSerializer(serializers.ModelSerializer):
    items = PrescriptionItemSerializer(many=True, read_only=True)

    class Meta:
        model = PrescriptionHeader
        fields = ['id', 'patient', 'doctor', 'issued_date', 'status', 'items']

