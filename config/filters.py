"""
Filtros personalizados para la API REST.
"""
from rest_framework import filters
from django_filters import rest_framework as django_filters
from appointments.models import Appointment
from django.utils import timezone


class AppointmentFilter(django_filters.FilterSet):
    """Filtro personalizado para citas."""
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')
    scheduled_at_from = django_filters.DateTimeFilter(field_name='scheduled_at', lookup_expr='gte')
    scheduled_at_to = django_filters.DateTimeFilter(field_name='scheduled_at', lookup_expr='lte')
    business = django_filters.NumberFilter(field_name='business__id')
    customer = django_filters.NumberFilter(field_name='customer__id')
    service = django_filters.NumberFilter(field_name='service__id')

    class Meta:
        model = Appointment
        fields = ['status', 'business', 'customer', 'service', 'scheduled_at_from', 'scheduled_at_to']


class UpcomingAppointmentFilter(django_filters.FilterSet):
    """Filtro para citas próximas."""
    business = django_filters.NumberFilter(field_name='business__id')

    class Meta:
        model = Appointment
        fields = ['business']

    @property
    def qs(self):
        qs = super().qs
        return qs.filter(
            status__in=['pending', 'confirmed'],
            scheduled_at__gte=timezone.now()
        )

