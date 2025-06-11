

from .models import ChronicCondition
from rest_framework import serializers

class ChronicConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChronicCondition
        fields = '__all__'