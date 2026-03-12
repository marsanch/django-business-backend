"""
Configuración de Celery Beat para tareas programadas.
"""
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'send-appointment-reminders': {
        'task': 'reminders.tasks.send_appointment_reminders',
        'schedule': crontab(minute='*/15'),  # Cada 15 minutos
    },
    'cleanup-old-appointments': {
        'task': 'reminders.tasks.cleanup_old_appointments',
        'schedule': crontab(hour=2, minute=0),  # A las 2:00 AM diariamente
    },
}

