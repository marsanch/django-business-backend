"""
Modelos de la aplicación WhatsApp.
"""
from django.db import models
from appointments.models import Business

class WhatsAppTemplate(models.Model):
    """Modelo para plantillas de mensajes WhatsApp."""
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='whatsapp_templates')
    name = models.CharField(max_length=255, verbose_name='Nombre')
    title = models.CharField(max_length=255, verbose_name='Título')
    message_template = models.TextField(verbose_name='Plantilla de mensaje')
    variables = models.JSONField(default=list, verbose_name='Variables disponibles')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Plantilla WhatsApp'
        verbose_name_plural = 'Plantillas WhatsApp'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.business.name})'


class WhatsAppMessage(models.Model):
    """Modelo para registrar mensajes WhatsApp enviados."""
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('sent', 'Enviado'),
        ('delivered', 'Entregado'),
        ('failed', 'Fallido'),
    ]

    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='whatsapp_messages')
    phone_number = models.CharField(max_length=20, verbose_name='Número telefónico')
    message_body = models.TextField(verbose_name='Cuerpo del mensaje')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    twilio_sid = models.CharField(max_length=255, blank=True, verbose_name='Twilio Message SID')
    error_message = models.TextField(blank=True, verbose_name='Mensaje de error')
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Mensaje WhatsApp'
        verbose_name_plural = 'Mensajes WhatsApp'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.phone_number} - {self.status}'

