from django.shortcuts import render

# Create your views here.
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework import viewsets

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer