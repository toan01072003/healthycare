from django.db import models
from django.conf import settings
import uuid


class Dispensation(models.Model):
    STATUS_CHOICES = [
        ('dispensed', 'Dispensed'),
        ('partial', 'Partial'),
        ('unavailable', 'Unavailable'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prescription = models.ForeignKey('prescription.PrescriptionHeader', on_delete=models.CASCADE)
    pharmacist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    note = models.TextField(blank=True, null=True)
    dispensed_at = models.DateTimeField(auto_now_add=True)

