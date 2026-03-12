# Appointment Reminder System - WhatsApp Backend

Sistema backend completo para gestionar recordatorios automáticos de citas por WhatsApp.

## 🎯 Características

- **Gestión de Citas**: Crear, actualizar y gestionar citas
- **Recordatorios Automáticos**: Envío automático de recordatorios por WhatsApp 24 horas antes
- **Plantillas Personalizables**: Crear plantillas de mensajes WhatsApp por negocio
- **Registro de Mensajes**: Histórico completo de mensajes enviados
- **API REST**: API completa para integración con frontend
- **Sistema de Tareas**: Celery para procesamiento asincrónico
- **Admin Django**: Interfaz de administración completa

## 🛠️ Tecnologías

- **Python 3.11+**
- **Django 4.2**
- **Django REST Framework**
- **PostgreSQL** (producción) / SQLite (desarrollo)
- **Celery** - Task queue
- **Redis** - Message broker
- **Twilio** - Integración WhatsApp
- **Docker** - Containerización

## 📋 Requisitos Previos

- Python 3.11 o superior
- PostgreSQL 12+ (opcional, se puede usar SQLite en desarrollo)
- Redis 6+ (para Celery)
- Docker y Docker Compose (opcional)

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd django-business-backend
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env` con tus valores:

```env
SECRET_KEY=tu-clave-secreta
DEBUG=True
WHATSAPP_ACCOUNT_SID=tu_sid_twilio
WHATSAPP_AUTH_TOKEN=tu_token_twilio
WHATSAPP_FROM_NUMBER=+1234567890
```

### 5. Ejecutar migraciones

```bash
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Iniciar servidor de desarrollo

```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

## 🐳 Usando Docker

### Iniciar con Docker Compose

```bash
docker-compose up -d
```

Esto levanta:
- PostgreSQL
- Redis
- Django Web Server
- Celery Worker
- Celery Beat

Acceder a:
- Admin: `http://localhost:8000/admin/`
- API: `http://localhost:8000/api/`

### Detener los servicios

```bash
docker-compose down
```

## 📚 Estructura del Proyecto

```
django-business-backend/
├── config/                 # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── celery.py
├── appointments/          # App de gestión de citas
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── admin.py
├── reminders/             # App de recordatorios
│   ├── models.py
│   ├── views.py
│   ├── tasks.py
│   └── services.py
├── whatsapp/              # App de integración WhatsApp
│   ├── models.py
│   ├── views.py
│   └── admin.py
├── manage.py
├── requirements.txt
├── docker-compose.yml
└── Dockerfile
```

## 🔌 API Endpoints

### Citas
- `GET /api/appointments/appointments/` - Listar citas
- `POST /api/appointments/appointments/` - Crear cita
- `GET /api/appointments/appointments/{id}/` - Detalle de cita
- `PATCH /api/appointments/appointments/{id}/` - Actualizar cita
- `POST /api/appointments/appointments/{id}/cancel/` - Cancelar cita
- `POST /api/appointments/appointments/{id}/confirm/` - Confirmar cita
- `GET /api/appointments/appointments/upcoming/` - Citas próximas
- `GET /api/appointments/appointments/pending_reminders/` - Citas sin recordatorio

### Recordatorios
- `GET /api/reminders/logs/` - Historial de recordatorios
- `POST /api/reminders/send_now/` - Enviar recordatorio inmediato
- `POST /api/reminders/send_batch/` - Enviar múltiples recordatorios

### WhatsApp
- `GET /api/whatsapp/templates/` - Listar plantillas
- `POST /api/whatsapp/templates/` - Crear plantilla
- `GET /api/whatsapp/messages/` - Historial de mensajes
- `GET /api/whatsapp/messages/statistics/` - Estadísticas

### Negocios
- `GET /api/appointments/businesses/` - Listar negocios
- `POST /api/appointments/businesses/` - Crear negocio

### Clientes
- `GET /api/appointments/customers/` - Listar clientes
- `POST /api/appointments/customers/` - Crear cliente

### Servicios
- `GET /api/appointments/services/` - Listar servicios
- `POST /api/appointments/services/` - Crear servicio

## ⚙️ Tareas de Celery

Las tareas automáticas se ejecutan con Celery Beat:

- **send_appointment_reminders**: Cada 15 minutos, envía recordatorios de citas próximas
- **cleanup_old_appointments**: Cada día, limpia citas antiguas

## 🔐 Seguridad

- Usa variables de entorno para todos los datos sensibles
- No commits de archivos `.env` (está en `.gitignore`)
- Secretas de seguridad en producción
- CORS configurado para dominios específicos

## 📝 Autenticación

Actualmente usa autenticación de sesión de Django. Para producción, considera:
- JWT Tokens
- OAuth2
- Django REST Framework Token Authentication

## 🧪 Testing

Para correr tests (cuando los crees):

```bash
python manage.py test
```

## 🚢 Deployment

### Heroku

1. Crear archivo `runtime.txt`:
```
python-3.11.0
```

2. Configurar variables de entorno en Heroku
3. Push a Heroku

### Otras plataformas

Consulta `Procfile` para configuración de procesos.

## 📊 Admin Django

Acceder a `http://localhost:8000/admin/` con superusuario.

Funcionalidades:
- Gestión completa de negocios, servicios, clientes y citas
- Historial de recordatorios enviados
- Plantillas de WhatsApp
- Acciones en lote (cancelar, confirmar citas)

## 🔧 Troubleshooting

### Redis no conecta
```bash
# Asegurar que Redis está corriendo
redis-cli ping
```

### Celery no procesa tareas
```bash
# Revisar logs de Celery
celery -A config worker -l debug
```

### Error en migraciones
```bash
# Resetear migraciones (solo desarrollo)
python manage.py migrate appointments zero
python manage.py migrate
```

## 📦 Dependencias Principales

Ver `requirements.txt` para lista completa.

Principales:
- Django 4.2.0
- djangorestframework 3.14.0
- celery 5.3.0
- twilio 8.10.0
- psycopg2-binary 2.9.6

## 📄 Licencia

MIT License

## 👤 Autor

Maria Sánchez - Python Backend Developer

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📞 Soporte

Para reportar bugs o sugerencias, abre un issue en el repositorio.
