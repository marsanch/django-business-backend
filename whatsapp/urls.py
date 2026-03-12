"""
URLs de la aplicación WhatsApp.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WhatsAppTemplateViewSet, WhatsAppMessageViewSet

router = DefaultRouter()
router.register(r'templates', WhatsAppTemplateViewSet, basename='whatsapp-template')
router.register(r'messages', WhatsAppMessageViewSet, basename='whatsapp-message')

urlpatterns = [
    path('', include(router.urls)),
]

