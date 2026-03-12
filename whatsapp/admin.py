"""
Admin de la aplicación WhatsApp.
"""
from django.contrib import admin
from .models import WhatsAppTemplate, WhatsAppMessage


@admin.register(WhatsAppTemplate)
class WhatsAppTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'is_active', 'created_at')
    list_filter = ('is_active', 'business', 'created_at')
    search_fields = ('name', 'title', 'message_template')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Información General', {
            'fields': ('business', 'name', 'title', 'is_active')
        }),
        ('Plantilla', {
            'fields': ('message_template', 'variables')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(WhatsAppMessage)
class WhatsAppMessageAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'status', 'business', 'sent_at', 'created_at')
    list_filter = ('status', 'business', 'sent_at', 'created_at')
    search_fields = ('phone_number', 'message_body')
    readonly_fields = ('twilio_sid', 'created_at', 'updated_at', 'message_body')
    fieldsets = (
        ('Información General', {
            'fields': ('business', 'phone_number', 'status')
        }),
        ('Mensaje', {
            'fields': ('message_body',),
            'classes': ('collapse',)
        }),
        ('Twilio', {
            'fields': ('twilio_sid', 'error_message'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('sent_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return False

