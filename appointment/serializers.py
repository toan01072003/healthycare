from rest_framework import serializers
from .models import Appointment
from user_profile.models import UserProfile

class PatientInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'phone_number', 'gender', 'date_of_birth']

class AppointmentWithPatientSerializer(serializers.ModelSerializer):
    patient_info = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['id', 'date_time', 'status', 'reason', 'notes', 'patient_info']

    def get_patient_info(self, obj):
        try:
            profile = UserProfile.objects.get(user=obj.patient)
            return PatientInfoSerializer(profile).data
        except UserProfile.DoesNotExist:
            return None
