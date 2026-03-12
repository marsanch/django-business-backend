"""
Migraciones iniciales para la aplicación appointments.
"""
from django.db import migrations, models
import django.db.models.deletion
import django.core.validators
from decimal import Decimal


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre del negocio')),
                ('phone', models.CharField(max_length=20, verbose_name='Teléfono')),
                ('whatsapp_number', models.CharField(blank=True, max_length=20, verbose_name='Número WhatsApp')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('address', models.TextField(blank=True, verbose_name='Dirección')),
                ('timezone', models.CharField(default='America/Mexico_City', max_length=50, verbose_name='Zona horaria')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Negocio',
                'verbose_name_plural': 'Negocios',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre del servicio')),
                ('description', models.TextField(blank=True, verbose_name='Descripción')),
                ('duration_minutes', models.IntegerField(validators=[django.core.validators.MinValueValidator(15)], verbose_name='Duración (minutos)')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Precio')),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='appointments.business')),
            ],
            options={
                'verbose_name': 'Servicio',
                'verbose_name_plural': 'Servicios',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('last_name', models.CharField(max_length=100, verbose_name='Apellido')),
                ('phone', models.CharField(max_length=20, verbose_name='Teléfono')),
                ('whatsapp_number', models.CharField(blank=True, max_length=20, verbose_name='Número WhatsApp')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('notes', models.TextField(blank=True, verbose_name='Notas')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customers', to='appointments.business')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['first_name', 'last_name'],
                'unique_together': {('business', 'phone')},
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduled_at', models.DateTimeField(verbose_name='Fecha y hora programada')),
                ('status', models.CharField(choices=[('pending', 'Pendiente'), ('confirmed', 'Confirmada'), ('completed', 'Completada'), ('cancelled', 'Cancelada'), ('no_show', 'No presentado')], default='pending', max_length=20, verbose_name='Estado')),
                ('notes', models.TextField(blank=True, verbose_name='Notas')),
                ('reminder_sent', models.BooleanField(default=False, verbose_name='Recordatorio enviado')),
                ('reminder_sent_at', models.DateTimeField(blank=True, null=True, verbose_name='Fecha envío recordatorio')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='appointments.business')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='appointments.customer')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appointments', to='appointments.service')),
            ],
            options={
                'verbose_name': 'Cita',
                'verbose_name_plural': 'Citas',
                'ordering': ['-scheduled_at'],
            },
        ),
        migrations.AddIndex(
            model_name='appointment',
            index=models.Index(fields=['business', 'status', 'scheduled_at'], name='appointments_business_status_scheduled_idx'),
        ),
        migrations.AddIndex(
            model_name='appointment',
            index=models.Index(fields=['customer', 'scheduled_at'], name='appointments_customer_scheduled_idx'),
        ),
    ]

