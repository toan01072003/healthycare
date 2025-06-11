from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Prescription(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='issued_prescriptions')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_prescriptions')
    medication = models.TextField()
    dosage = models.CharField(max_length=100)
    instructions = models.TextField()
    issued_at = models.DateTimeField(auto_now_add=True)