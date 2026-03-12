"""
Funciones de utilidad para el proyecto.
"""
import re
from datetime import timedelta
from django.utils import timezone


def format_phone_number(phone_number: str) -> str:
    """
    Formatea un número de teléfono para WhatsApp.

    Args:
        phone_number: Número de teléfono a formatear

    Returns:
        Número formateado para WhatsApp
    """
    # Elimina caracteres no numéricos excepto '+'
    clean_number = re.sub(r'[^\d+]', '', phone_number)

    # Si no comienza con '+', lo añade
    if not clean_number.startswith('+'):
        clean_number = '+' + clean_number

    return f'whatsapp:{clean_number}'


def validate_phone_number(phone_number: str) -> bool:
    """
    Valida un número de teléfono.

    Args:
        phone_number: Número a validar

    Returns:
        True si es válido, False en caso contrario
    """
    # Acepta números con formato internacional
    pattern = r'^\+?[\d\s\-\(\)]{10,}$'
    return bool(re.match(pattern, phone_number))


def get_appointment_reminder_time(scheduled_at, hours_before=24):
    """
    Calcula la hora en la que se debe enviar el recordatorio.

    Args:
        scheduled_at: Fecha y hora de la cita
        hours_before: Horas antes de la cita para enviar el recordatorio

    Returns:
        datetime: Fecha y hora para enviar el recordatorio
    """
    return scheduled_at - timedelta(hours=hours_before)


def should_send_reminder(appointment, hours_before=24):
    """
    Determina si se debe enviar recordatorio para una cita.

    Args:
        appointment: Objeto Appointment
        hours_before: Horas antes de la cita

    Returns:
        bool: True si se debe enviar recordatorio
    """
    now = timezone.now()
    reminder_time = get_appointment_reminder_time(appointment.scheduled_at, hours_before)

    return (
        appointment.status in ['pending', 'confirmed']
        and not appointment.reminder_sent
        and reminder_time <= now <= appointment.scheduled_at
    )


def format_appointment_message(appointment, template=None):
    """
    Formatea un mensaje de cita.

    Args:
        appointment: Objeto Appointment
        template: Plantilla de mensaje personalizada (opcional)

    Returns:
        str: Mensaje formateado
    """
    if template:
        return template.format(
            customer_name=appointment.customer.first_name,
            service_name=appointment.service.name if appointment.service else 'tu cita',
            scheduled_at=appointment.scheduled_at.strftime('%d de %B de %Y a las %H:%M')
        )

    customer_name = appointment.customer.first_name
    service_name = appointment.service.name if appointment.service else 'tu cita'
    scheduled_time = appointment.scheduled_at.strftime('%d de %B de %Y a las %H:%M')

    return f"""Hola {customer_name}, 👋

Te recordamos que tienes una cita programada para {service_name}.

📅 Fecha y hora: {scheduled_time}
📞 Si necesitas cambiar tu cita, contáctanos.

¡Nos vemos pronto!"""


def get_time_until_appointment(appointment):
    """
    Calcula el tiempo restante hasta una cita.

    Args:
        appointment: Objeto Appointment

    Returns:
        timedelta: Tiempo restante
    """
    return appointment.scheduled_at - timezone.now()


def is_appointment_soon(appointment, hours=24):
    """
    Determina si una cita es próxima.

    Args:
        appointment: Objeto Appointment
        hours: Número de horas para considerar "próxima"

    Returns:
        bool: True si es próxima
    """
    time_until = get_time_until_appointment(appointment)
    return timedelta(0) <= time_until <= timedelta(hours=hours)


def get_business_timezone(business):
    """
    Obtiene la zona horaria de un negocio.

    Args:
        business: Objeto Business

    Returns:
        str: Zona horaria
    """
    return business.timezone or 'America/Mexico_City'


def log_reminder_event(appointment, status, message='', error=''):
    """
    Registra un evento de recordatorio.

    Args:
        appointment: Objeto Appointment
        status: Estado del recordatorio ('sent', 'failed', etc.)
        message: Mensaje enviado
        error: Mensaje de error (si aplica)
    """
    from reminders.models import ReminderLog

    ReminderLog.objects.create(
        appointment=appointment,
        status=status,
        message=message,
        error_message=error,
        sent_at=timezone.now() if status == 'sent' else None
    )

