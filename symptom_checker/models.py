from django.db import models
from django.conf import settings

# Create your models here.
class Symptom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Disease(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    keywords = models.CharField(max_length=255)
    symptoms = models.ManyToManyField(Symptom)