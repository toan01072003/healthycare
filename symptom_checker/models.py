from django.db import models
from django.conf import settings
import uuid


class Symptom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Disease(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    keywords = models.CharField(max_length=255)
    symptoms = models.ManyToManyField(Symptom)


class AISymptomCheck(models.Model):
    RECOMMENDATION_CHOICES = [
        ('home_care', 'Home Care'),
        ('consult_doctor', 'Consult Doctor'),
        ('emergency', 'Emergency'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    input_text = models.TextField()
    recommendation = models.CharField(max_length=20, choices=RECOMMENDATION_CHOICES)
    shared_with_doctor = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class AISymptomPrediction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    symptom_check = models.ForeignKey(AISymptomCheck, on_delete=models.CASCADE, related_name='predictions')
    condition_name = models.CharField(max_length=255)
    confidence_score = models.FloatField()


class SymptomChecklist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    snomed_code = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)


class EmergencyFlag(models.Model):
    TRIGGER_CHOICES = [
        ('AI', 'AI'),
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    triggered_by = models.CharField(max_length=10, choices=TRIGGER_CHOICES)
    reason = models.TextField()
    related_symptom_check = models.ForeignKey(AISymptomCheck, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

