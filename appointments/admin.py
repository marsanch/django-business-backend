"""
Admin de la aplicación de citas.
"""
from django.contrib import admin
from .models import Business, Service, Customer, Appointment


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Información General', {
            'fields': ('name', 'phone', 'email', 'address')
        }),
        ('WhatsApp', {
            'fields': ('whatsapp_number',)
        }),
        ('Configuración', {
            'fields': ('timezone',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'duration_minutes', 'price', 'active')
    list_filter = ('active', 'business', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Información General', {
            'fields': ('business', 'name', 'description')
        }),
        ('Detalles', {
            'fields': ('duration_minutes', 'price', 'active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'business', 'created_at')
    list_filter = ('business', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone', 'email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Información General', {
            'fields': ('business', 'first_name', 'last_name')
        }),
        ('Contacto', {
            'fields': ('phone', 'whatsapp_number', 'email')
        }),
        ('Notas', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'service', 'scheduled_at', 'status', 'reminder_sent')
    list_filter = ('status', 'reminder_sent', 'business', 'scheduled_at')
    search_fields = ('customer__first_name', 'customer__last_name', 'service__name')
    readonly_fields = ('reminder_sent', 'reminder_sent_at', 'created_at', 'updated_at', 'is_upcoming')
    fieldsets = (
        ('Información General', {
            'fields': ('business', 'customer', 'service', 'scheduled_at')
        }),
        ('Estado', {
            'fields': ('status', 'notes')
        }),
        ('Recordatorio', {
            'fields': ('reminder_sent', 'reminder_sent_at'),
            'classes': ('collapse',)
        }),
        ('Detalles', {
            'fields': ('is_upcoming',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_reminder_sent', 'cancel_appointments', 'confirm_appointments']

    def mark_reminder_sent(self, request, queryset):
        from django.utils import timezone
        count = queryset.update(reminder_sent=True, reminder_sent_at=timezone.now())
        self.message_user(request, f'{count} citas marcadas con recordatorio enviado.')

    mark_reminder_sent.short_description = 'Marcar como recordatorio enviado'

    def cancel_appointments(self, request, queryset):
        count = queryset.update(status='cancelled')
        self.message_user(request, f'{count} citas canceladas.')

    cancel_appointments.short_description = 'Cancelar citas seleccionadas'

    def confirm_appointments(self, request, queryset):
        count = queryset.update(status='confirmed')
        self.message_user(request, f'{count} citas confirmadas.')

    confirm_appointments.short_description = 'Confirmar citas seleccionadas'

