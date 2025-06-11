from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
class Vitals(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recorded_at = models.DateTimeField(auto_now_add=True)
    heart_rate = models.IntegerField()
    blood_pressure = models.CharField(max_length=10)  # e.g., 120/80
    temperature = models.FloatField()
    spo2 = models.IntegerField()  # oxygen saturation