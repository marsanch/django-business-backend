"""
Migraciones iniciales para la aplicación reminders.
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
            name='ReminderLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pendiente'), ('sent', 'Enviado'), ('failed', 'Fallido')], default='pending', max_length=20)),
                ('message', models.TextField(blank=True, verbose_name='Mensaje enviado')),
                ('error_message', models.TextField(blank=True, verbose_name='Mensaje de error')),
                ('attempt_count', models.IntegerField(default=0, verbose_name='Número de intentos')),
                ('sent_at', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de envío')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reminder_logs', to='appointments.appointment')),
            ],
            options={
                'verbose_name': 'Registro de Recordatorio',
                'verbose_name_plural': 'Registros de Recordatorios',
                'ordering': ['-created_at'],
            },
        ),
    ]

