"""
Paginadores personalizados para la API REST.
"""
from rest_framework.pagination import PageNumberPagination


class AppointmentPagination(PageNumberPagination):
    """Paginador para citas."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CustomerPagination(PageNumberPagination):
    """Paginador para clientes."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ReminderLogPagination(PageNumberPagination):
    """Paginador para logs de recordatorios."""
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 100


class WhatsAppMessagePagination(PageNumberPagination):
    """Paginador para mensajes de WhatsApp."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

