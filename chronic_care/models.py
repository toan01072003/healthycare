from django.db import models
from django.conf import settings
import uuid


class ChronicCareLog(models.Model):
    METRIC_CHOICES = [
        ('glucose', 'Glucose'),
        ('bp', 'Blood Pressure'),
        ('weight', 'Weight'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    metric_type = models.CharField(max_length=20, choices=METRIC_CHOICES)
    value = models.FloatField()
    note = models.TextField(blank=True, null=True)
    recorded_at = models.DateTimeField()

