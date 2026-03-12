"""
Excepciones personalizadas para el proyecto.
"""
from rest_framework.exceptions import APIException
from rest_framework import status


class AppointmentException(APIException):
    """Excepción base para citas."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Error en la cita'


class AppointmentNotFound(APIException):
    """Excepción cuando no se encuentra una cita."""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Cita no encontrada'


class InvalidAppointmentStatus(AppointmentException):
    """Excepción cuando el estado de la cita es inválido."""
    default_detail = 'Estado de cita inválido'


class AppointmentAlreadyCancelled(AppointmentException):
    """Excepción cuando se intenta modificar una cita cancelada."""
    default_detail = 'La cita ya ha sido cancelada'


class ReminderException(APIException):
    """Excepción base para recordatorios."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Error en el recordatorio'


class ReminderAlreadySent(ReminderException):
    """Excepción cuando se intenta enviar un recordatorio duplicado."""
    default_detail = 'El recordatorio ya ha sido enviado'


class WhatsAppException(APIException):
    """Excepción base para WhatsApp."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Error en WhatsApp'


class InvalidPhoneNumber(WhatsAppException):
    """Excepción cuando el número de teléfono es inválido."""
    default_detail = 'Número de teléfono inválido'


class WhatsAppNotConfigured(WhatsAppException):
    """Excepción cuando WhatsApp no está configurado."""
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'WhatsApp no está configurado correctamente'


class MessageSendingFailed(WhatsAppException):
    """Excepción cuando falla el envío de mensaje."""
    default_detail = 'Fallo al enviar el mensaje'


class CustomerException(APIException):
    """Excepción base para clientes."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Error en el cliente'


class DuplicateCustomerPhone(CustomerException):
    """Excepción cuando se intenta crear un cliente con número duplicado."""
    default_detail = 'Ya existe un cliente con este número de teléfono'

