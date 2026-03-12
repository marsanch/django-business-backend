# 🚀 Guía de Inicio Rápido

## Instalación Local

### Requisitos
- Python 3.11+
- Redis (opcional, para desarrollo puede usarse SQLite)

### Pasos

1. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   ```
   Edita `.env` con tus valores.

4. **Ejecutar migraciones**
   ```bash
   python manage.py migrate
   ```

5. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

6. **Iniciar servidor**
   ```bash
   python manage.py runserver
   ```
   
   Accede a: http://localhost:8000/admin/

## Desarrollo con Docker

```bash
docker-compose up -d
```

Se levantarán automáticamente:
- PostgreSQL en puerto 5432
- Redis en puerto 6379
- Django en http://localhost:8000
- Celery Worker (procesamiento de tareas)
- Celery Beat (tareas programadas)

## Comandos Útiles

### Crear datos de ejemplo
```bash
python manage.py shell
```

```python
from appointments.models import Business, Service, Customer, Appointment
from django.utils import timezone
from datetime import timedelta

# Crear negocio
business = Business.objects.create(
    name="Salón de Belleza",
    phone="+34666777888",
    email="salon@example.com"
)

# Crear servicio
service = Service.objects.create(
    business=business,
    name="Corte de cabello",
    duration_minutes=30,
    price=25.00
)

# Crear cliente
customer = Customer.objects.create(
    business=business,
    first_name="María",
    last_name="García",
    phone="+34666555444",
    whatsapp_number="+34666555444"
)

# Crear cita
appointment = Appointment.objects.create(
    business=business,
    customer=customer,
    service=service,
    scheduled_at=timezone.now() + timedelta(days=1)
)
```

### Enviar recordatorio manual
```bash
python manage.py shell
```

```python
from reminders.services import WhatsAppService
from appointments.models import Appointment

appointment = Appointment.objects.first()
service = WhatsAppService()
service.send_reminder(appointment)
```

### Ver logs de Celery
```bash
celery -A config worker -l debug
```

### Ejecutar tarea de Celery manualmente
```bash
python manage.py shell
```

```python
from reminders.tasks import send_appointment_reminders
result = send_appointment_reminders.delay()
```

## API Endpoints de Prueba

### Listar citas
```bash
curl http://localhost:8000/api/appointments/appointments/
```

### Crear cita
```bash
curl -X POST http://localhost:8000/api/appointments/appointments/ \
  -H "Content-Type: application/json" \
  -d '{
    "business": 1,
    "customer": 1,
    "service": 1,
    "scheduled_at": "2024-03-20T15:00:00Z"
  }'
```

### Enviar recordatorio inmediato
```bash
curl -X POST http://localhost:8000/api/reminders/send_now/ \
  -H "Content-Type: application/json" \
  -d '{
    "appointment_id": 1
  }'
```

## Solución de Problemas

### "No se puede conectar a Redis"
- Asegúrate de que Redis está ejecutándose: `redis-cli ping`
- O usa Docker: `docker-compose up redis`

### "Tabla no existe"
```bash
python manage.py migrate
```

### "Errores de permisos en archivos estáticos"
```bash
python manage.py collectstatic --noinput
```

### "Celery no ejecuta tareas"
1. Inicia el worker: `celery -A config worker -l info`
2. Inicia beat: `celery -A config beat -l info`
3. O usa Docker: `docker-compose up celery celery-beat`

## Variables de Entorno Importantes

```env
# Desarrollo
DEBUG=True
SECRET_KEY=tu-clave-secreta

# WhatsApp (Twilio)
WHATSAPP_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxx
WHATSAPP_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxx
WHATSAPP_FROM_NUMBER=+1234567890

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=appointment_reminder
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost

# Redis/Celery
CELERY_BROKER_URL=redis://localhost:6379/0

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

## Estructura de Carpetas

```
django-business-backend/
├── config/               # Configuración
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── wsgi.py
├── appointments/        # Gestión de citas
├── reminders/           # Recordatorios
├── whatsapp/            # Integración WhatsApp
├── manage.py
├── requirements.txt
└── docker-compose.yml
```

## Documentación Completa

Ver `README.md` para documentación detallada.

## Soporte

Para reportar bugs o sugerencias, abre un issue en el repositorio.

