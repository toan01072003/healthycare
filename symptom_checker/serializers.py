from rest_framework import serializers
from .models import Symptom, Disease

class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = '__all__'

class DiseaseSerializer(serializers.ModelSerializer):
    symptoms = SymptomSerializer(many=True, read_only=True)

    class Meta:
        model = Disease
        fields = '__all__'