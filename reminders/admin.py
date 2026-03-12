"""
Admin de la aplicación de recordatorios.
"""
from django.contrib import admin
from .models import ReminderLog

@admin.register(ReminderLog)
class ReminderLogAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'status', 'sent_at', 'attempt_count', 'created_at')
    list_filter = ('status', 'sent_at', 'created_at')
    search_fields = ('appointment__customer__first_name', 'appointment__customer__last_name')
    readonly_fields = ('created_at', 'updated_at', 'message', 'error_message')
    fieldsets = (
        ('Cita', {
            'fields': ('appointment',)
        }),
        ('Información de Envío', {
            'fields': ('status', 'sent_at', 'attempt_count')
        }),
        ('Mensaje', {
            'fields': ('message', 'error_message'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

