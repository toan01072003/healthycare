from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import uuid

# Create your models here.
class MedicalRecord(models.Model):
    RECORD_TYPE_CHOICES = [
        ('lab', 'Lab'),
        ('scan', 'Scan'),
        ('note', 'Note'),
        ('referral', 'Referral'),
        ('prescription', 'Prescription'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_records')
    file_url = models.URLField()
    type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES)
    summary = models.TextField()
    date_uploaded = models.DateTimeField(auto_now_add=True)
