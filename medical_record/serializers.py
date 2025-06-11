
from .models import MedicalRecord
from rest_framework import serializers

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'
