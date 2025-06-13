

from .models import ChronicCareLog
from rest_framework import serializers

class ChronicCareLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChronicCareLog
        fields = '__all__'
