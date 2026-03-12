"""
Vistas de la aplicación WhatsApp.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import WhatsAppTemplate, WhatsAppMessage
from .serializers import WhatsAppTemplateSerializer, WhatsAppMessageSerializer


class WhatsAppTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar plantillas de WhatsApp."""
    queryset = WhatsAppTemplate.objects.all()
    serializer_class = WhatsAppTemplateSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'title', 'message_template']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filtra plantillas por negocio."""
        queryset = super().get_queryset()
        business_id = self.request.query_params.get('business_id')
        if business_id:
            queryset = queryset.filter(business_id=business_id)
        return queryset


class WhatsAppMessageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para ver mensajes de WhatsApp enviados."""
    queryset = WhatsAppMessage.objects.all()
    serializer_class = WhatsAppMessageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['phone_number', 'status']
    ordering_fields = ['created_at', 'sent_at', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filtra mensajes por negocio."""
        queryset = super().get_queryset()
        business_id = self.request.query_params.get('business_id')
        status_filter = self.request.query_params.get('status')
        
        if business_id:
            queryset = queryset.filter(business_id=business_id)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Obtiene estadísticas de mensajes enviados."""
        business_id = request.query_params.get('business_id')
        
        queryset = self.get_queryset()
        if business_id:
            queryset = queryset.filter(business_id=business_id)
        
        total_messages = queryset.count()
        sent_messages = queryset.filter(status='sent').count()
        delivered_messages = queryset.filter(status='delivered').count()
        failed_messages = queryset.filter(status='failed').count()
        
        return Response({
            'total_messages': total_messages,
            'sent': sent_messages,
            'delivered': delivered_messages,
            'failed': failed_messages,
            'delivery_rate': round((delivered_messages / total_messages * 100) if total_messages > 0 else 0, 2)
        })

