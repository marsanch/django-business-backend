"""
Constantes para el proyecto.
"""

# Estados de cita
APPOINTMENT_STATUS_PENDING = 'pending'
APPOINTMENT_STATUS_CONFIRMED = 'confirmed'
APPOINTMENT_STATUS_COMPLETED = 'completed'
APPOINTMENT_STATUS_CANCELLED = 'cancelled'
APPOINTMENT_STATUS_NO_SHOW = 'no_show'

APPOINTMENT_STATUSES = [
    (APPOINTMENT_STATUS_PENDING, 'Pendiente'),
    (APPOINTMENT_STATUS_CONFIRMED, 'Confirmada'),
    (APPOINTMENT_STATUS_COMPLETED, 'Completada'),
    (APPOINTMENT_STATUS_CANCELLED, 'Cancelada'),
    (APPOINTMENT_STATUS_NO_SHOW, 'No presentado'),
]

# Estados de recordatorio
REMINDER_STATUS_PENDING = 'pending'
REMINDER_STATUS_SENT = 'sent'
REMINDER_STATUS_FAILED = 'failed'

REMINDER_STATUSES = [
    (REMINDER_STATUS_PENDING, 'Pendiente'),
    (REMINDER_STATUS_SENT, 'Enviado'),
    (REMINDER_STATUS_FAILED, 'Fallido'),
]

# Estados de mensaje WhatsApp
MESSAGE_STATUS_PENDING = 'pending'
MESSAGE_STATUS_SENT = 'sent'
MESSAGE_STATUS_DELIVERED = 'delivered'
MESSAGE_STATUS_FAILED = 'failed'

MESSAGE_STATUSES = [
    (MESSAGE_STATUS_PENDING, 'Pendiente'),
    (MESSAGE_STATUS_SENT, 'Enviado'),
    (MESSAGE_STATUS_DELIVERED, 'Entregado'),
    (MESSAGE_STATUS_FAILED, 'Fallido'),
]

# Duración mínima de servicio (en minutos)
MIN_SERVICE_DURATION = 15

# Precio mínimo
MIN_PRICE = 0.01

# Horas por defecto antes del recordatorio
DEFAULT_REMINDER_HOURS_BEFORE = 24

# Tiempo de espera para reintentar (en minutos)
REMINDER_RETRY_INTERVAL = 30

# Máximo de reintentos
MAX_REMINDER_RETRIES = 3

# Tiempo de conservación de citas completadas (en días)
APPOINTMENT_RETENTION_DAYS = 90

