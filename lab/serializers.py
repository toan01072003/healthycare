

from .models import LabTest
from rest_framework import serializers

class LabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = '__all__'