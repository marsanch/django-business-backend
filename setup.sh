#!/bin/bash

# Script para inicializar el proyecto Django

set -e

echo "🚀 Iniciando configuración del proyecto..."

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "📝 Creando archivo .env..."
    cp .env.example .env
    echo "⚠️  Por favor, actualiza el archivo .env con tus valores"
fi

# Ejecutar migraciones
echo "🗄️  Ejecutando migraciones..."
python manage.py migrate

# Crear superusuario si no existe
echo "👤 Creando superusuario..."
python manage.py createsuperuser

# Crear datos iniciales
echo "📊 Creando datos de ejemplo..."
python manage.py shell << EOF
from appointments.models import Business, Service
from django.contrib.auth.models import User

# Crear un negocio de ejemplo
if not Business.objects.exists():
    business = Business.objects.create(
        name="Mi Negocio",
        phone="+1234567890",
        whatsapp_number="+1234567890",
        email="negocio@example.com",
        address="Calle Principal 123"
    )

    # Crear un servicio de ejemplo
    Service.objects.create(
        business=business,
        name="Servicio de Ejemplo",
        description="Descripción del servicio",
        duration_minutes=30,
        price=50.00
    )

    print("✅ Datos iniciales creados exitosamente")
else:
    print("ℹ️  Los datos iniciales ya existen")
EOF

echo ""
echo "✅ ¡Proyecto inicializado correctamente!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Actualiza el archivo .env con tus configuraciones"
echo "2. Inicia el servidor: python manage.py runserver"
echo "3. Accede a http://localhost:8000/admin/"
echo ""
echo "🐳 Para usar Docker:"
echo "   docker-compose up -d"
echo ""

