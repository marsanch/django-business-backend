"""
Tests para la aplicación reminders.
"""
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from appointments.models import Business, Service, Customer, Appointment
from reminders.models import ReminderLog
from reminders.services import WhatsAppService


class ReminderLogModelTest(TestCase):
    """Tests para el modelo ReminderLog."""
    
    def setUp(self):
        self.business = Business.objects.create(
            name="Test Business",
            phone="+1234567890",
            email="test@example.com"
        )
        self.service = Service.objects.create(
            business=self.business,
            name="Test Service",
            duration_minutes=30,
            price=50.00
        )
        self.customer = Customer.objects.create(
            business=self.business,
            first_name="Juan",
            last_name="Pérez",
            phone="+34666777888"
        )
        self.appointment = Appointment.objects.create(
            business=self.business,
            customer=self.customer,
            service=self.service,
            scheduled_at=timezone.now() + timedelta(days=1)
        )
        self.reminder_log = ReminderLog.objects.create(
            appointment=self.appointment,
            status='pending'
        )
    
    def test_reminder_log_creation(self):
        """Verifica que un registro de recordatorio se crea correctamente."""
        self.assertEqual(self.reminder_log.status, 'pending')
        self.assertEqual(self.reminder_log.appointment, self.appointment)
    
    def test_reminder_log_str(self):
        """Verifica la representación en string del recordatorio."""
        self.assertIn('pending', str(self.reminder_log))


class WhatsAppServiceTest(TestCase):
    """Tests para el servicio WhatsApp."""
    
    def setUp(self):
        self.business = Business.objects.create(
            name="Test Business",
            phone="+1234567890",
            email="test@example.com"
        )
        self.service = Service.objects.create(
            business=self.business,
            name="Test Service",
            duration_minutes=30,
            price=50.00
        )
        self.customer = Customer.objects.create(
            business=self.business,
            first_name="Juan",
            last_name="Pérez",
            phone="+34666777888",
            whatsapp_number="+34666777888"
        )
        self.appointment = Appointment.objects.create(
            business=self.business,
            customer=self.customer,
            service=self.service,
            scheduled_at=timezone.now() + timedelta(days=1)
        )
        self.service_instance = WhatsAppService()
    
    def test_format_phone_number(self):
        """Verifica que el número de teléfono se formatea correctamente."""
        formatted = self.service_instance._format_phone_number("34666777888")
        self.assertTrue(formatted.startswith("whatsapp:"))
    
    def test_build_reminder_message(self):
        """Verifica que se construye el mensaje correctamente."""
        message = self.service_instance._build_reminder_message(self.appointment)
        self.assertIn("Juan", message)
        self.assertIn("Test Service", message)
    
    def test_reminder_message_contains_customer_name(self):
        """Verifica que el mensaje incluye el nombre del cliente."""
        message = self.service_instance._build_reminder_message(self.appointment)
        self.assertIn(self.customer.first_name, message)

