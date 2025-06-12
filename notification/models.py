from django.db import models
from django.conf import settings
import uuid


class Notification(models.Model):
    TYPE_CHOICES = [
        ('alert', 'Alert'),
        ('reminder', 'Reminder'),
        ('info', 'Info'),
    ]

    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('read', 'Read'),
        ('archived', 'Archived'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='notifications_sent')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications_received')
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    sent_at = models.DateTimeField(auto_now_add=True)

