from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class PharmacyItem(models.Model):
    name = models.CharField(max_length=100)
    stock = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class DispensedMedicine(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(PharmacyItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    dispensed_at = models.DateTimeField(auto_now_add=True)
