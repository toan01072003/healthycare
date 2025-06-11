from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class MedicalRecord(models.Model):
    RECORD_TYPE_CHOICES = [
        ('lab', 'Lab'),
        ('scan', 'Scan'),
        ('note', 'Note'),
    ]

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_records')
    file_url = models.URLField()
    type = models.CharField(max_length=10, choices=RECORD_TYPE_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
