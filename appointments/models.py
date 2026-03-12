"""
Modelos de la aplicación de citas.
"""
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal

class Business(models.Model):
    """Modelo para representar un negocio."""
    name = models.CharField(max_length=255, verbose_name='Nombre del negocio')
    phone = models.CharField(max_length=20, verbose_name='Teléfono')
    whatsapp_number = models.CharField(max_length=20, verbose_name='Número WhatsApp', blank=True)
    email = models.EmailField(verbose_name='Email')
    address = models.TextField(verbose_name='Dirección', blank=True)
    timezone = models.CharField(max_length=50, default='America/Mexico_City', verbose_name='Zona horaria')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Negocio'
        verbose_name_plural = 'Negocios'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Service(models.Model):
    """Modelo para representar un servicio."""
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=255, verbose_name='Nombre del servicio')
    description = models.TextField(verbose_name='Descripción', blank=True)
    duration_minutes = models.IntegerField(validators=[MinValueValidator(15)], verbose_name='Duración (minutos)')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name='Precio')
    active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.business.name})'


class Customer(models.Model):
    """Modelo para representar un cliente."""
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='customers')
    first_name = models.CharField(max_length=100, verbose_name='Nombre')
    last_name = models.CharField(max_length=100, verbose_name='Apellido')
    phone = models.CharField(max_length=20, verbose_name='Teléfono')
    whatsapp_number = models.CharField(max_length=20, verbose_name='Número WhatsApp', blank=True)
    email = models.EmailField(verbose_name='Email', blank=True)
    notes = models.TextField(verbose_name='Notas', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['first_name', 'last_name']
        unique_together = ['business', 'phone']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Appointment(models.Model):
    """Modelo para representar una cita."""
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmada'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
        ('no_show', 'No presentado'),
    ]

    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='appointments')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, related_name='appointments')
    scheduled_at = models.DateTimeField(verbose_name='Fecha y hora programada')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Estado')
    notes = models.TextField(verbose_name='Notas', blank=True)
    reminder_sent = models.BooleanField(default=False, verbose_name='Recordatorio enviado')
    reminder_sent_at = models.DateTimeField(verbose_name='Fecha envío recordatorio', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['-scheduled_at']
        indexes = [
            models.Index(fields=['business', 'status', 'scheduled_at']),
            models.Index(fields=['customer', 'scheduled_at']),
        ]

    def __str__(self):
        return f'{self.customer.full_name} - {self.scheduled_at}'

    @property
    def is_upcoming(self):
        """Verifica si la cita está próxima."""
        return self.scheduled_at > timezone.now() and self.status in ['pending', 'confirmed']

    @property
    def time_until_appointment(self):
        """Calcula el tiempo restante hasta la cita."""
        return self.scheduled_at - timezone.now()

