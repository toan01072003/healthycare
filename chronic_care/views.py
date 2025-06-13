from rest_framework import viewsets
from .models import ChronicCareLog
from .serializers import ChronicCareLogSerializer

class ChronicCareLogViewSet(viewsets.ModelViewSet):
    queryset = ChronicCareLog.objects.all()
    serializer_class = ChronicCareLogSerializer

