@echo off
REM Script para inicializar el proyecto Django en Windows

echo 🚀 Iniciando configuracion del proyecto...

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo 📥 Instalando dependencias...
pip install -r requirements.txt

REM Crear archivo .env si no existe
if not exist ".env" (
    echo 📝 Creando archivo .env...
    copy .env.example .env
    echo ⚠️  Por favor, actualiza el archivo .env con tus valores
)

REM Ejecutar migraciones
echo 🗄️  Ejecutando migraciones...
python manage.py migrate

REM Crear superusuario
echo 👤 Creando superusuario...
python manage.py createsuperuser

REM Crear datos iniciales
echo 📊 Creando datos de ejemplo...
python manage.py shell

echo.
echo ✅ ¡Proyecto inicializado correctamente!
echo.
echo 📋 Próximos pasos:
echo 1. Actualiza el archivo .env con tus configuraciones
echo 2. Inicia el servidor: python manage.py runserver
echo 3. Accede a http://localhost:8000/admin/
echo.
echo 🐳 Para usar Docker:
echo    docker-compose up -d
echo.

