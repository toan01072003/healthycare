from rest_framework import viewsets
from .models import Dispensation
from .serializers import DispensationSerializer

class DispensationViewSet(viewsets.ModelViewSet):
    queryset = Dispensation.objects.all()
    serializer_class = DispensationSerializer

