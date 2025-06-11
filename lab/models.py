from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class LabTest(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=100)
    test_date = models.DateField()
    result = models.TextField()
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_tests')
