from django.db import models
from django.conf import settings
import uuid


class VitalSigns(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='vitals_recorded')
    recorded_at = models.DateTimeField()
    blood_pressure = models.CharField(max_length=20)
    temperature = models.FloatField()
    heart_rate = models.IntegerField()
    oxygen_saturation = models.FloatField()
    respiratory_rate = models.IntegerField()

