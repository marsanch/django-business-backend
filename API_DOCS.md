# API REST - Documentación

## Autenticación

Por defecto, el proyecto usa autenticación de sesión de Django. Para producción, se recomienda JWT.

### Obtener token (si se implementa JWT)
```bash
POST /api/token/
{
    "username": "user",
    "password": "password"
}
```

## Negocios (Businesses)

### Listar negocios
```
GET /api/appointments/businesses/
```

**Parámetros de query:**
- `search`: Buscar por nombre, email o teléfono
- `page`: Número de página (default: 1)
- `page_size`: Resultados por página (default: 10)

**Respuesta:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Mi Salón",
            "phone": "+34666777888",
            "whatsapp_number": "+34666777888",
            "email": "salon@example.com",
            "address": "Calle Principal 123",
            "timezone": "America/Mexico_City",
            "created_at": "2024-01-15T10:00:00Z",
            "updated_at": "2024-01-15T10:00:00Z"
        }
    ]
}
```

### Crear negocio
```
POST /api/appointments/businesses/
Content-Type: application/json

{
    "name": "Mi Salón",
    "phone": "+34666777888",
    "whatsapp_number": "+34666777888",
    "email": "salon@example.com",
    "address": "Calle Principal 123",
    "timezone": "America/Mexico_City"
}
```

### Obtener detalle de negocio
```
GET /api/appointments/businesses/{id}/
```

### Actualizar negocio
```
PATCH /api/appointments/businesses/{id}/
Content-Type: application/json

{
    "name": "Nuevo nombre",
    "phone": "+34666777888"
}
```

### Eliminar negocio
```
DELETE /api/appointments/businesses/{id}/
```

## Clientes (Customers)

### Listar clientes
```
GET /api/appointments/customers/
```

**Parámetros:**
- `business_id`: Filtrar por negocio
- `search`: Buscar por nombre, teléfono o email
- `page`: Número de página

**Respuesta:**
```json
{
    "count": 1,
    "results": [
        {
            "id": 1,
            "business": 1,
            "first_name": "Juan",
            "last_name": "García",
            "full_name": "Juan García",
            "phone": "+34666555444",
            "whatsapp_number": "+34666555444",
            "email": "juan@example.com",
            "notes": "Cliente VIP",
            "created_at": "2024-01-15T10:00:00Z",
            "updated_at": "2024-01-15T10:00:00Z"
        }
    ]
}
```

### Crear cliente
```
POST /api/appointments/customers/
Content-Type: application/json

{
    "business": 1,
    "first_name": "Juan",
    "last_name": "García",
    "phone": "+34666555444",
    "whatsapp_number": "+34666555444",
    "email": "juan@example.com",
    "notes": "Cliente VIP"
}
```

## Servicios (Services)

### Listar servicios
```
GET /api/appointments/services/
```

**Parámetros:**
- `business_id`: Filtrar por negocio
- `search`: Buscar en nombre o descripción

**Respuesta:**
```json
{
    "count": 1,
    "results": [
        {
            "id": 1,
            "business": 1,
            "name": "Corte de cabello",
            "description": "Corte estándar",
            "duration_minutes": 30,
            "price": "25.00",
            "active": true,
            "created_at": "2024-01-15T10:00:00Z",
            "updated_at": "2024-01-15T10:00:00Z"
        }
    ]
}
```

### Crear servicio
```
POST /api/appointments/services/
Content-Type: application/json

{
    "business": 1,
    "name": "Corte de cabello",
    "description": "Corte estándar",
    "duration_minutes": 30,
    "price": "25.00",
    "active": true
}
```

## Citas (Appointments)

### Listar citas
```
GET /api/appointments/appointments/
```

**Parámetros:**
- `business_id`: Filtrar por negocio
- `status`: Filtrar por estado (pending, confirmed, completed, cancelled, no_show)
- `search`: Buscar por nombre de cliente o servicio

**Respuesta:**
```json
{
    "count": 1,
    "results": [
        {
            "id": 1,
            "business": 1,
            "customer": 1,
            "customer_name": "Juan García",
            "service": 1,
            "service_name": "Corte de cabello",
            "scheduled_at": "2024-01-20T15:00:00Z",
            "status": "pending",
            "notes": "",
            "reminder_sent": false,
            "reminder_sent_at": null,
            "is_upcoming": true,
            "created_at": "2024-01-15T10:00:00Z",
            "updated_at": "2024-01-15T10:00:00Z"
        }
    ]
}
```

### Crear cita
```
POST /api/appointments/appointments/
Content-Type: application/json

{
    "business": 1,
    "customer": 1,
    "service": 1,
    "scheduled_at": "2024-01-20T15:00:00Z",
    "status": "pending",
    "notes": "Nota adicional"
}
```

### Citas próximas
```
GET /api/appointments/appointments/upcoming/
```

Retorna solo citas futuras con estado pending o confirmed.

### Citas sin recordatorio
```
GET /api/appointments/appointments/pending_reminders/
```

Retorna citas que no han tenido recordatorio enviado.

### Cancelar cita
```
POST /api/appointments/appointments/{id}/cancel/
```

### Confirmar cita
```
POST /api/appointments/appointments/{id}/confirm/
```

### Marcar recordatorio como enviado
```
POST /api/appointments/appointments/{id}/mark_reminder_sent/
```

## Recordatorios (Reminders)

### Enviar recordatorio inmediato
```
POST /api/reminders/send_now/
Content-Type: application/json

{
    "appointment_id": 1
}
```

**Respuesta:**
```json
{
    "status": "success",
    "message": "Recordatorio enviado correctamente"
}
```

### Enviar múltiples recordatorios
```
POST /api/reminders/send_batch/
Content-Type: application/json

{
    "appointment_ids": [1, 2, 3]
}
```

**Respuesta:**
```json
{
    "status": "success",
    "sent_count": 3,
    "total": 3
}
```

### Historial de recordatorios
```
GET /api/reminders/logs/
```

**Parámetros:**
- `appointment_id`: Filtrar por cita
- `business_id`: Filtrar por negocio

**Respuesta:**
```json
{
    "count": 1,
    "results": [
        {
            "id": 1,
            "appointment": 1,
            "appointment_customer": "Juan García",
            "appointment_scheduled_at": "2024-01-20T15:00:00Z",
            "status": "sent",
            "message": "Hola Juan...",
            "error_message": "",
            "attempt_count": 1,
            "sent_at": "2024-01-20T14:00:00Z",
            "created_at": "2024-01-20T14:00:00Z",
            "updated_at": "2024-01-20T14:00:00Z"
        }
    ]
}
```

## WhatsApp

### Plantillas
```
GET /api/whatsapp/templates/
POST /api/whatsapp/templates/
```

### Mensajes enviados
```
GET /api/whatsapp/messages/
```

### Estadísticas
```
GET /api/whatsapp/messages/statistics/
```

**Respuesta:**
```json
{
    "total_messages": 100,
    "sent": 95,
    "delivered": 90,
    "failed": 5,
    "delivery_rate": 95.0
}
```

## Códigos de respuesta HTTP

- **200 OK**: Solicitud exitosa
- **201 Created**: Recurso creado
- **204 No Content**: Solicitud exitosa sin contenido
- **400 Bad Request**: Solicitud inválida
- **401 Unauthorized**: No autenticado
- **403 Forbidden**: No autorizado
- **404 Not Found**: Recurso no encontrado
- **500 Internal Server Error**: Error del servidor

## Manejo de errores

Todos los errores retornan un JSON con formato:
```json
{
    "detail": "Descripción del error",
    "code": "error_code"
}
```

## Rate Limiting

El API no tiene rate limiting implementado por defecto. Para producción, se recomienda agregarlo.

## CORS

CORS está habilitado para los dominios configurados en `CORS_ALLOWED_ORIGINS`.

## Ejemplos con cURL

### Listar citas
```bash
curl -X GET http://localhost:8000/api/appointments/appointments/
```

### Crear cita
```bash
curl -X POST http://localhost:8000/api/appointments/appointments/ \
  -H "Content-Type: application/json" \
  -d '{
    "business": 1,
    "customer": 1,
    "service": 1,
    "scheduled_at": "2024-01-20T15:00:00Z"
  }'
```

### Enviar recordatorio
```bash
curl -X POST http://localhost:8000/api/reminders/send_now/ \
  -H "Content-Type: application/json" \
  -d '{"appointment_id": 1}'
```

## WebSocket (Futuro)

Se puede implementar WebSocket para notificaciones en tiempo real usando Django Channels.

