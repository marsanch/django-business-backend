"""
Modelos de la aplicación de recordatorios.
"""
from django.db import models
from appointments.models import Appointment

class ReminderLog(models.Model):
    """Modelo para registrar el historial de recordatorios enviados."""
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('sent', 'Enviado'),
        ('failed', 'Fallido'),
    ]

    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='reminder_logs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(verbose_name='Mensaje enviado', blank=True)
    error_message = models.TextField(verbose_name='Mensaje de error', blank=True)
    attempt_count = models.IntegerField(default=0, verbose_name='Número de intentos')
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de envío')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Registro de Recordatorio'
        verbose_name_plural = 'Registros de Recordatorios'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.appointment} - {self.status}'

