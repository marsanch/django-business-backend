"""
Tests para la aplicación appointments.
"""
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from appointments.models import Business, Service, Customer, Appointment


class BusinessModelTest(TestCase):
    """Tests para el modelo Business."""
    
    def setUp(self):
        self.business = Business.objects.create(
            name="Test Business",
            phone="+1234567890",
            email="test@example.com"
        )
    
    def test_business_creation(self):
        """Verifica que un negocio se crea correctamente."""
        self.assertEqual(self.business.name, "Test Business")
        self.assertEqual(self.business.phone, "+1234567890")
    
    def test_business_str(self):
        """Verifica la representación en string del negocio."""
        self.assertEqual(str(self.business), "Test Business")


class ServiceModelTest(TestCase):
    """Tests para el modelo Service."""
    
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
    
    def test_service_creation(self):
        """Verifica que un servicio se crea correctamente."""
        self.assertEqual(self.service.name, "Test Service")
        self.assertEqual(self.service.duration_minutes, 30)
    
    def test_service_active_by_default(self):
        """Verifica que los servicios están activos por defecto."""
        self.assertTrue(self.service.active)


class CustomerModelTest(TestCase):
    """Tests para el modelo Customer."""
    
    def setUp(self):
        self.business = Business.objects.create(
            name="Test Business",
            phone="+1234567890",
            email="test@example.com"
        )
        self.customer = Customer.objects.create(
            business=self.business,
            first_name="Juan",
            last_name="Pérez",
            phone="+34666777888"
        )
    
    def test_customer_creation(self):
        """Verifica que un cliente se crea correctamente."""
        self.assertEqual(self.customer.first_name, "Juan")
        self.assertEqual(self.customer.full_name, "Juan Pérez")
    
    def test_customer_unique_phone_per_business(self):
        """Verifica que no se pueden crear dos clientes con el mismo número en el mismo negocio."""
        with self.assertRaises(Exception):
            Customer.objects.create(
                business=self.business,
                first_name="Pedro",
                last_name="López",
                phone="+34666777888"
            )


class AppointmentModelTest(TestCase):
    """Tests para el modelo Appointment."""
    
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
    
    def test_appointment_creation(self):
        """Verifica que una cita se crea correctamente."""
        self.assertEqual(self.appointment.status, "pending")
        self.assertFalse(self.appointment.reminder_sent)
    
    def test_appointment_is_upcoming(self):
        """Verifica que una cita futura se detecta correctamente."""
        self.assertTrue(self.appointment.is_upcoming)
    
    def test_past_appointment_not_upcoming(self):
        """Verifica que una cita pasada no se considera próxima."""
        past_appointment = Appointment.objects.create(
            business=self.business,
            customer=self.customer,
            service=self.service,
            scheduled_at=timezone.now() - timedelta(days=1)
        )
        self.assertFalse(past_appointment.is_upcoming)
    
    def test_appointment_time_until(self):
        """Verifica el cálculo del tiempo hasta la cita."""
        time_until = self.appointment.time_until_appointment
        self.assertTrue(time_until.total_seconds() > 0)


class AppointmentViewSetTest(TestCase):
    """Tests para el AppointmentViewSet."""
    
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
    
    def test_get_upcoming_appointments(self):
        """Verifica que se pueden obtener citas próximas."""
        upcoming = Appointment.objects.filter(
            status__in=['pending', 'confirmed'],
            scheduled_at__gte=timezone.now()
        )
        self.assertEqual(upcoming.count(), 1)
    
    def test_get_pending_reminders(self):
        """Verifica que se pueden obtener citas sin recordatorio."""
        pending = Appointment.objects.filter(
            reminder_sent=False,
            scheduled_at__gte=timezone.now()
        )
        self.assertEqual(pending.count(), 1)

