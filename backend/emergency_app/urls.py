"""
URL configuration for the emergency_app project.

The `urlpatterns` list routes URLs to views. This is the root URL configuration
that includes all app-level URL patterns.

For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import include, path

# Root URL patterns - routes requests to appropriate apps
urlpatterns = [
    # Django admin interface
    path('admin/', admin.site.urls),
    
    # API endpoints - all routes under /api/ are handled by the contacts app
    # This includes:
    # - /api/items/ - List and create contacts
    # - /api/items/{id}/ - Retrieve, update, or delete a contact
    path('api/', include('contacts.urls')),
]
