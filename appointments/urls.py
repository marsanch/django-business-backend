"""
URLs de la aplicación de citas.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessViewSet, ServiceViewSet, CustomerViewSet, AppointmentViewSet

router = DefaultRouter()
router.register(r'businesses', BusinessViewSet, basename='business')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = [
    path('', include(router.urls)),
]

