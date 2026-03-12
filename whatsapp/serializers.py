"""
Serializadores de la aplicación WhatsApp.
"""
from rest_framework import serializers
from .models import WhatsAppTemplate, WhatsAppMessage


class WhatsAppTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatsAppTemplate
        fields = ['id', 'business', 'name', 'title', 'message_template', 'variables', 'is_active', 'created_at', 'updated_at']


class WhatsAppMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatsAppMessage
        fields = ['id', 'business', 'phone_number', 'message_body', 'status', 'twilio_sid', 'error_message', 'sent_at', 'created_at', 'updated_at']
        read_only_fields = ['twilio_sid', 'sent_at', 'created_at', 'updated_at']

