# 📑 ÍNDICE DEL PROYECTO

## 🚀 Comienza Aquí

1. **Nuevo en el proyecto?** → Lee [README.md](README.md) primero
2. **Quieres comenzar rápido?** → Sigue [QUICKSTART.md](QUICKSTART.md) (5 min)
3. **Necesitas instrucciones detalladas?** → Ve a [GETTING_STARTED.md](GETTING_STARTED.md)

---

## 📚 Documentación General

| Archivo | Descripción |
|---------|------------|
| [README.md](README.md) | 📖 Documentación general completa del proyecto |
| [QUICKSTART.md](QUICKSTART.md) | ⚡ Guía de inicio rápido (5 minutos) |
| [GETTING_STARTED.md](GETTING_STARTED.md) | 🚀 Instrucciones detalladas de instalación |
| [API_DOCS.md](API_DOCS.md) | 🔌 Documentación de API con 30+ ejemplos |
| [DEVELOPMENT.md](DEVELOPMENT.md) | 📋 Checklist de desarrollo |
| [PROJECT_SUMMARY.txt](PROJECT_SUMMARY.txt) | 📊 Resumen visual del proyecto |
| [INDEX.md](INDEX.md) | 📑 Este archivo |

---

## 🗂️ Estructura del Código

### Configuración (`config/`)
- `settings.py` - Configuración principal de Django
- `urls.py` - URLs de proyecto
- `wsgi.py` - WSGI application
- `celery.py` - Configuración de Celery
- `constants.py` - Constantes globales
- `exceptions.py` - Excepciones personalizadas
- `filters.py` - Filtros para API
- `pagination.py` - Paginadores
- `utils.py` - Funciones de utilidad
- `logging_config.py` - Configuración de logs
- `test_settings.py` - Configuración para tests

### Apps Django

#### 📅 Appointments (Citas)
```
appointments/
├── models.py         # Business, Service, Customer, Appointment
├── views.py          # ViewSets para API
├── serializers.py    # Serializadores DRF
├── urls.py           # URLs de la app
├── admin.py          # Interfaces admin
├── apps.py           # Configuración app
├── tests.py          # Tests unitarios
└── migrations/       # Migraciones de BD
```

#### 🔔 Reminders (Recordatorios)
```
reminders/
├── models.py         # ReminderLog
├── views.py          # ViewSets para API
├── serializers.py    # Serializadores
├── urls.py           # URLs
├── services.py       # Servicio WhatsApp
├── tasks.py          # Tareas Celery
├── admin.py          # Admin Django
├── apps.py           # Configuración app
├── tests.py          # Tests
└── migrations/       # Migraciones
```

#### 💬 WhatsApp (Integración)
```
whatsapp/
├── models.py         # Template, Message
├── views.py          # ViewSets para API
├── serializers.py    # Serializadores
├── urls.py           # URLs
├── admin.py          # Admin Django
├── apps.py           # Configuración app
└── migrations/       # Migraciones
```

---

## 🔌 API Endpoints

### Negocios
```
GET/POST    /api/appointments/businesses/
GET/PATCH   /api/appointments/businesses/{id}/
DELETE      /api/appointments/businesses/{id}/
```

### Servicios
```
GET/POST    /api/appointments/services/
GET/PATCH   /api/appointments/services/{id}/
DELETE      /api/appointments/services/{id}/
```

### Clientes
```
GET/POST    /api/appointments/customers/
GET/PATCH   /api/appointments/customers/{id}/
DELETE      /api/appointments/customers/{id}/
```

### Citas
```
GET/POST    /api/appointments/appointments/
GET/PATCH   /api/appointments/appointments/{id}/
DELETE      /api/appointments/appointments/{id}/
POST        /api/appointments/appointments/{id}/cancel/
POST        /api/appointments/appointments/{id}/confirm/
POST        /api/appointments/appointments/{id}/mark_reminder_sent/
GET         /api/appointments/appointments/upcoming/
GET         /api/appointments/appointments/pending_reminders/
```

### Recordatorios
```
POST        /api/reminders/send_now/
POST        /api/reminders/send_batch/
GET         /api/reminders/logs/
```

### WhatsApp
```
GET/POST    /api/whatsapp/templates/
GET         /api/whatsapp/messages/
GET         /api/whatsapp/messages/statistics/
```

Ver [API_DOCS.md](API_DOCS.md) para ejemplos detallados.

---

## ⚙️ Configuración

### Archivos de Configuración
- `.env.example` - Template de variables de entorno
- `requirements.txt` - Dependencias Python
- `docker-compose.yml` - Orquestación Docker
- `Dockerfile` - Imagen Docker
- `Procfile` - Configuración Heroku
- `pytest.ini` - Configuración pytest
- `.editorconfig` - Configuración de editor
- `.gitignore` - Archivos a ignorar en git

### Variables de Entorno (.env)
```env
# Django
SECRET_KEY=tu-clave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# WhatsApp (Twilio)
WHATSAPP_ACCOUNT_SID=ACxxxxxxx
WHATSAPP_AUTH_TOKEN=xxxxxx
WHATSAPP_FROM_NUMBER=+1234567890

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

---

## 🧪 Testing

### Ejecutar Tests
```bash
# Todos los tests
python manage.py test

# Tests específicos
python manage.py test appointments

# Con pytest
pytest -v

# Con cobertura
coverage run --source='.' manage.py test
coverage report
```

### Archivos de Tests
- `appointments/tests.py` - Tests de modelos y API de citas
- `reminders/tests.py` - Tests de recordatorios y servicios
- `config/test_settings.py` - Configuración para tests

---

## 🚀 Inicio Rápido

### Opción 1: Sin Docker
```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar .env
cp .env.example .env

# 4. Ejecutar migraciones
python manage.py migrate

# 5. Crear superusuario
python manage.py createsuperuser

# 6. Iniciar servidor
python manage.py runserver
```

### Opción 2: Con Docker
```bash
docker-compose up -d
docker-compose exec web python manage.py createsuperuser
```

Acceder a: http://localhost:8000/admin/

---

## 📊 Estadísticas

```
Total de archivos:      54
Archivos Python:        45+
Líneas de código:       3,500+
Aplicaciones:           3
Modelos:                7
Endpoints:              20+
Tests:                  50+
Documentación:          6 archivos
```

---

## 🎯 Modelos de Datos

1. **Business** - Negocios/Empresas
2. **Service** - Servicios ofrecidos
3. **Customer** - Clientes
4. **Appointment** - Citas (con índices optimizados)
5. **ReminderLog** - Historial de recordatorios
6. **WhatsAppTemplate** - Plantillas de mensajes
7. **WhatsAppMessage** - Mensajes enviados

---

## 📋 Tareas Celery

### send_appointment_reminders
- **Frecuencia**: Cada 15 minutos
- **Función**: Envía recordatorios a citas próximas
- **Archivo**: `reminders/tasks.py`

### cleanup_old_appointments
- **Frecuencia**: Diariamente a las 2:00 AM
- **Función**: Limpia citas antiguas (>90 días)
- **Archivo**: `reminders/tasks.py`

---

## 🔐 Seguridad

- ✅ Variables de entorno en .env (no tracked)
- ✅ CORS configurado
- ✅ CSRF protection
- ✅ SQL injection prevention
- ✅ Autenticación de sesión
- ✅ Admin Django protegido

---

## 🛠️ Tecnologías

| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| Backend | Django | 4.2.0 |
| API | Django REST Framework | 3.14.0 |
| Task Queue | Celery | 5.3.0 |
| Message Broker | Redis | 5.0.0 |
| Base de Datos | PostgreSQL/SQLite | 15/3 |
| WhatsApp | Twilio | 8.10.0 |
| Containerización | Docker | Latest |
| Python | Python | 3.11+ |

---

## 📞 Comandos Útiles

```bash
# Migraciones
python manage.py makemigrations
python manage.py migrate
python manage.py migrate --fake-initial

# Servidor
python manage.py runserver

# Superusuario
python manage.py createsuperuser

# Shell interactivo
python manage.py shell

# Tests
python manage.py test
pytest -v

# Celery (en terminal separada)
celery -A config worker -l info
celery -A config beat -l info

# Docker
docker-compose up -d
docker-compose down
docker-compose logs -f web
```

---

## 📖 Para Aprender Más

- [Django Official Docs](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [Twilio WhatsApp API](https://www.twilio.com/docs/whatsapp)
- [Docker Docs](https://docs.docker.com/)

---

## 📞 Próximos Pasos

1. **Lee** [README.md](README.md) para entender el proyecto
2. **Sigue** [QUICKSTART.md](QUICKSTART.md) para empezar rápido
3. **Consulta** [API_DOCS.md](API_DOCS.md) para ejemplos de API
4. **Revisa** [DEVELOPMENT.md](DEVELOPMENT.md) para checklist

---

## 🎉 Estado del Proyecto

**Versión**: 1.0.0  
**Estado**: ✅ MVP Completado  
**Fecha**: 2024-03-12  
**Completitud**: 100%  

El proyecto está **listo para desarrollo, testing y deployment**.

---

**Última actualización**: 2024-03-12  
**Autor**: Sistema de Recordatorios de Citas por WhatsApp

