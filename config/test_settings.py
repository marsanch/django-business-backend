"""
Configuración para correr tests.
"""
import os

# Usar SQLite para testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Deshabilitar migraciones para testing más rápido
class DisableMigrations:
    def __contains__(self, item):
        return True
    
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Configuración mínima para tests
SECRET_KEY = 'test-secret-key'
DEBUG = True
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'rest_framework',
    'corsheaders',
    'appointments',
    'reminders',
    'whatsapp',
]

MIDDLEWARE = []

# Mock Redis para Celery
CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = 'cache+memory://'

# WhatsApp deshabilitado en tests
WHATSAPP_ACCOUNT_SID = ''
WHATSAPP_AUTH_TOKEN = ''
WHATSAPP_FROM_NUMBER = ''

