"""
Vistas de la aplicación de recordatorios.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ReminderLog
from .serializers import ReminderLogSerializer
from appointments.models import Appointment
from .services import WhatsAppService
from django.utils import timezone

class ReminderLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para ver el historial de recordatorios."""
    queryset = ReminderLog.objects.all()
    serializer_class = ReminderLogSerializer

    def get_queryset(self):
        """Filtra logs por negocio y cita."""
        queryset = super().get_queryset()
        appointment_id = self.request.query_params.get('appointment_id')
        business_id = self.request.query_params.get('business_id')
        
        if appointment_id:
            queryset = queryset.filter(appointment_id=appointment_id)
        if business_id:
            queryset = queryset.filter(appointment__business_id=business_id)
        
        return queryset


class ReminderViewSet(viewsets.ViewSet):
    """ViewSet para gestionar recordatorios manualmente."""
    
    @action(detail=False, methods=['post'])
    def send_now(self, request):
        """Envía un recordatorio inmediato a una cita específica."""
        appointment_id = request.data.get('appointment_id')
        
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response(
                {'error': 'Cita no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            whatsapp_service = WhatsAppService()
            if whatsapp_service.send_reminder(appointment):
                appointment.reminder_sent = True
                appointment.reminder_sent_at = timezone.now()
                appointment.save()
                
                return Response({
                    'status': 'success',
                    'message': 'Recordatorio enviado correctamente'
                })
            else:
                return Response(
                    {'error': 'No se pudo enviar el recordatorio'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def send_batch(self, request):
        """Envía recordatorios a múltiples citas."""
        appointment_ids = request.data.get('appointment_ids', [])
        
        if not appointment_ids:
            return Response(
                {'error': 'No se proporcionaron IDs de citas'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            appointments = Appointment.objects.filter(id__in=appointment_ids)
            whatsapp_service = WhatsAppService()
            sent_count = 0
            
            for appointment in appointments:
                try:
                    if whatsapp_service.send_reminder(appointment):
                        appointment.reminder_sent = True
                        appointment.reminder_sent_at = timezone.now()
                        appointment.save()
                        sent_count += 1
                except Exception as e:
                    print(f'Error enviando recordatorio: {str(e)}')
            
            return Response({
                'status': 'success',
                'sent_count': sent_count,
                'total': len(appointments)
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

