from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class ChronicCondition(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    diagnosis_date = models.DateField()
    treatment_plan = models.TextField()