

from .models import AuditLog
from rest_framework import serializers
class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'
