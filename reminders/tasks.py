"""
Tareas de Celery para recordatorios de citas.
"""
from celery import shared_task
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from appointments.models import Appointment
from .services import WhatsAppService

@shared_task
def send_appointment_reminders():
    """
    Tarea programada para enviar recordatorios de citas.
    Se ejecuta cada cierto tiempo para enviar recordatorios.
    """
    try:
        hours_before = settings.REMINDER_HOURS_BEFORE
        reminder_threshold = timezone.now() + timedelta(hours=hours_before)
        
        # Obtiene citas que necesitan recordatorio
        appointments = Appointment.objects.filter(
            status__in=['pending', 'confirmed'],
            reminder_sent=False,
            scheduled_at__gte=timezone.now(),
            scheduled_at__lte=reminder_threshold
        )
        
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
                print(f'Error enviando recordatorio para cita {appointment.id}: {str(e)}')
        
        return {
            'status': 'success',
            'reminders_sent': sent_count,
            'total_processed': len(appointments)
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }


@shared_task
def cleanup_old_appointments():
    """
    Tarea programada para limpiar citas antiguas (completadas o canceladas hace más de 90 días).
    """
    try:
        cutoff_date = timezone.now() - timedelta(days=90)
        deleted_count, _ = Appointment.objects.filter(
            status__in=['completed', 'cancelled'],
            updated_at__lt=cutoff_date
        ).delete()
        
        return {
            'status': 'success',
            'deleted_count': deleted_count
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }

