"""
Serializadores de la aplicación de recordatorios.
"""
from rest_framework import serializers
from .models import ReminderLog


class ReminderLogSerializer(serializers.ModelSerializer):
    appointment_customer = serializers.CharField(source='appointment.customer.full_name', read_only=True)
    appointment_scheduled_at = serializers.DateTimeField(source='appointment.scheduled_at', read_only=True)

    class Meta:
        model = ReminderLog
        fields = ['id', 'appointment', 'appointment_customer', 'appointment_scheduled_at', 'status', 'message', 'error_message', 'attempt_count', 'sent_at', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

