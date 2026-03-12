"""
Servicios de WhatsApp para la aplicación de recordatorios.
"""
from django.conf import settings
from .models import ReminderLog
from django.utils import timezone
from datetime import datetime
import requests
import json

class WhatsAppService:
    """Servicio para enviar mensajes de WhatsApp usando Twilio."""
    
    def __init__(self):
        self.account_sid = settings.WHATSAPP_ACCOUNT_SID
        self.auth_token = settings.WHATSAPP_AUTH_TOKEN
        self.from_number = settings.WHATSAPP_FROM_NUMBER
        self.base_url = f'https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}'

    def send_reminder(self, appointment):
        """
        Envía un recordatorio de cita por WhatsApp.
        
        Args:
            appointment: Objeto Appointment a recordar
            
        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        try:
            if not self._is_configured():
                print('WhatsApp no está configurado correctamente')
                return False
            
            phone_number = appointment.customer.whatsapp_number or appointment.customer.phone
            if not phone_number:
                return False
            
            # Formatea el número de teléfono
            phone_number = self._format_phone_number(phone_number)
            
            # Crea el mensaje
            message = self._build_reminder_message(appointment)
            
            # Envía el mensaje
            if self._send_whatsapp_message(phone_number, message):
                # Registra el envío exitoso
                ReminderLog.objects.create(
                    appointment=appointment,
                    status='sent',
                    message=message,
                    sent_at=timezone.now(),
                    attempt_count=1
                )
                return True
            else:
                return False
                
        except Exception as e:
            ReminderLog.objects.create(
                appointment=appointment,
                status='failed',
                error_message=str(e),
                attempt_count=1
            )
            return False

    def _is_configured(self):
        """Verifica si WhatsApp está configurado correctamente."""
        return bool(self.account_sid and self.auth_token and self.from_number)

    def _format_phone_number(self, phone_number):
        """Formatea el número de teléfono para Twilio."""
        # Asume números en formato internacional
        phone_number = phone_number.replace('-', '').replace(' ', '')
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number
        return f'whatsapp:{phone_number}'

    def _build_reminder_message(self, appointment):
        """Construye el mensaje de recordatorio."""
        customer_name = appointment.customer.first_name
        service_name = appointment.service.name if appointment.service else 'tu cita'
        scheduled_time = appointment.scheduled_at.strftime('%d de %B de %Y a las %H:%M')
        
        message = f"""Hola {customer_name}, 👋

Te recordamos que tienes una cita programada para {service_name}.

📅 Fecha y hora: {scheduled_time}
📞 Si necesitas cambiar tu cita, contáctanos.

¡Nos vemos pronto!"""
        
        return message

    def _send_whatsapp_message(self, to_number, message):
        """
        Envía un mensaje de WhatsApp usando Twilio.
        
        Args:
            to_number: Número de destino en formato whatsapp:+1234567890
            message: Texto del mensaje
            
        Returns:
            bool: True si se envió correctamente
        """
        try:
            url = f'{self.base_url}/Messages.json'
            
            data = {
                'From': f'whatsapp:{self.from_number}',
                'To': to_number,
                'Body': message
            }
            
            response = requests.post(
                url,
                data=data,
                auth=(self.account_sid, self.auth_token)
            )
            
            return response.status_code in [200, 201]
        except Exception as e:
            print(f'Error enviando mensaje por WhatsApp: {str(e)}')
            return False


class MockWhatsAppService(WhatsAppService):
    """Servicio simulado de WhatsApp para desarrollo y pruebas."""
    
    def _send_whatsapp_message(self, to_number, message):
        """Simula el envío de un mensaje."""
        print(f'[MOCK] Enviando WhatsApp a {to_number}: {message}')
        return True


def get_whatsapp_service():
    """Factory para obtener el servicio de WhatsApp apropiado."""
    if settings.DEBUG:
        return MockWhatsAppService()
    return WhatsAppService()

