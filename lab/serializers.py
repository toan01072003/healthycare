

from .models import LabResult
from rest_framework import serializers

class LabResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResult
        fields = '__all__'
