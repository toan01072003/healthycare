from django.shortcuts import render

# Create your views here.
from .models import ChronicCondition
from .serializers import ChronicConditionSerializer
from rest_framework import viewsets

class ChronicConditionViewSet(viewsets.ModelViewSet):
    queryset = ChronicCondition.objects.all()
    serializer_class = ChronicConditionSerializer