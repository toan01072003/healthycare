

from .models import Dispensation
from rest_framework import serializers

class DispensationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispensation
        fields = '__all__'
