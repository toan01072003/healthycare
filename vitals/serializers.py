
from rest_framework import serializers
from .models import Vitals

class VitalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vitals
        fields = '__all__'
