from django.db import models
from django.conf import settings
import uuid


class LabResult(models.Model):
    TEST_TYPE_CHOICES = [
        ('blood', 'Blood'),
        ('urine', 'Urine'),
        ('MRI', 'MRI'),
    ]

    STATUS_CHOICES = [
        ('normal', 'Normal'),
        ('borderline', 'Borderline'),
        ('abnormal', 'Abnormal'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lab_results')
    test_type = models.CharField(max_length=20, choices=TEST_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    file_url = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

