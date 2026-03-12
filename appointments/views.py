"""
Vistas de la aplicación de citas.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Business, Service, Customer, Appointment
from .serializers import (
    BusinessSerializer,
    ServiceSerializer,
    CustomerSerializer,
    AppointmentSerializer,
    AppointmentDetailSerializer
)


class BusinessViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar negocios."""
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'phone']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']


class ServiceViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar servicios."""
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'duration_minutes']

    def get_queryset(self):
        """Filtra servicios por negocio si se proporciona."""
        queryset = super().get_queryset()
        business_id = self.request.query_params.get('business_id')
        if business_id:
            queryset = queryset.filter(business_id=business_id)
        return queryset


class CustomerViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar clientes."""
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'phone', 'email']
    ordering_fields = ['first_name', 'last_name', 'created_at']
    ordering = ['first_name', 'last_name']

    def get_queryset(self):
        """Filtra clientes por negocio si se proporciona."""
        queryset = super().get_queryset()
        business_id = self.request.query_params.get('business_id')
        if business_id:
            queryset = queryset.filter(business_id=business_id)
        return queryset


class AppointmentViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar citas."""
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['customer__first_name', 'customer__last_name', 'service__name', 'status']
    ordering_fields = ['scheduled_at', 'created_at', 'status']
    ordering = ['-scheduled_at']

    def get_serializer_class(self):
        """Usa serializador detallado para acciones retrieve."""
        if self.action == 'retrieve':
            return AppointmentDetailSerializer
        return AppointmentSerializer

    def get_queryset(self):
        """Filtra citas por negocio y aplica filtros adicionales."""
        queryset = super().get_queryset()
        business_id = self.request.query_params.get('business_id')
        status_filter = self.request.query_params.get('status')
        
        if business_id:
            queryset = queryset.filter(business_id=business_id)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Obtiene las citas próximas."""
        queryset = self.get_queryset().filter(
            status__in=['pending', 'confirmed'],
            scheduled_at__gte=timezone.now()
        ).order_by('scheduled_at')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pending_reminders(self, request):
        """Obtiene citas pendientes de recordatorio."""
        business_id = request.query_params.get('business_id')
        
        queryset = Appointment.objects.filter(
            status__in=['pending', 'confirmed'],
            reminder_sent=False,
            scheduled_at__gte=timezone.now()
        )
        
        if business_id:
            queryset = queryset.filter(business_id=business_id)
        
        queryset = queryset.order_by('scheduled_at')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_reminder_sent(self, request, pk=None):
        """Marca una cita como recordatorio enviado."""
        appointment = self.get_object()
        appointment.reminder_sent = True
        appointment.reminder_sent_at = timezone.now()
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancela una cita."""
        appointment = self.get_object()
        appointment.status = 'cancelled'
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirma una cita."""
        appointment = self.get_object()
        appointment.status = 'confirmed'
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)

