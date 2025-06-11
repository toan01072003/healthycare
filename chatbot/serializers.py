# chatbot/serializers.py

from rest_framework import serializers
from .models import ChatMessage, ChatbotSession

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'session', 'is_user', 'content', 'timestamp']

class ChatbotSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatbotSession
        fields = ['id', 'user', 'started_at', 'messages']
