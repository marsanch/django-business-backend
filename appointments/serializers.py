"""
Serializadores de la aplicación de citas.
"""
from rest_framework import serializers
from .models import Business, Service, Customer, Appointment


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['id', 'name', 'phone', 'whatsapp_number', 'email', 'address', 'timezone', 'created_at', 'updated_at']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'business', 'name', 'description', 'duration_minutes', 'price', 'active', 'created_at', 'updated_at']


class CustomerSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'business', 'first_name', 'last_name', 'full_name', 'phone', 'whatsapp_number', 'email', 'notes', 'created_at', 'updated_at']


class AppointmentSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    is_upcoming = serializers.BooleanField(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'business', 'customer', 'customer_name', 'service', 'service_name', 'scheduled_at', 'status', 'notes', 'reminder_sent', 'reminder_sent_at', 'is_upcoming', 'created_at', 'updated_at']
        read_only_fields = ['reminder_sent', 'reminder_sent_at', 'created_at', 'updated_at']


class AppointmentDetailSerializer(AppointmentSerializer):
    """Serializador detallado de citas con información completa."""
    customer = CustomerSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

