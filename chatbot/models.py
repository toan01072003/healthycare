# chatbot/models.py

from django.db import models
from django.conf import settings

class ChatbotSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatbotSession, on_delete=models.CASCADE, related_name='messages')
    is_user = models.BooleanField(default=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
