"""
Admin configuration for the contacts app.

This file registers the Contact model so it appears in the Django admin site.
"""
from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'status', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('status', 'event_notification_type')
