"""
Migraciones iniciales para la aplicación whatsapp.
"""
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WhatsAppTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
                ('title', models.CharField(max_length=255, verbose_name='Título')),
                ('message_template', models.TextField(verbose_name='Plantilla de mensaje')),
                ('variables', models.JSONField(default=list, verbose_name='Variables disponibles')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='whatsapp_templates', to='appointments.business')),
            ],
            options={
                'verbose_name': 'Plantilla WhatsApp',
                'verbose_name_plural': 'Plantillas WhatsApp',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='WhatsAppMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Número telefónico')),
                ('message_body', models.TextField(verbose_name='Cuerpo del mensaje')),
                ('status', models.CharField(choices=[('pending', 'Pendiente'), ('sent', 'Enviado'), ('delivered', 'Entregado'), ('failed', 'Fallido')], default='pending', max_length=20)),
                ('twilio_sid', models.CharField(blank=True, max_length=255, verbose_name='Twilio Message SID')),
                ('error_message', models.TextField(blank=True, verbose_name='Mensaje de error')),
                ('sent_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='whatsapp_messages', to='appointments.business')),
            ],
            options={
                'verbose_name': 'Mensaje WhatsApp',
                'verbose_name_plural': 'Mensajes WhatsApp',
                'ordering': ['-created_at'],
            },
        ),
    ]

