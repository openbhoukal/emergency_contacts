"""
Database models for the emergency contacts application.

The `Contact` model stores information about each emergency contact along with
notification preferences and event types. Use Django migrations to create
or update this table in the database.

"""
from django.db import models


class Contact(models.Model):
    """
    Represents a single emergency contact record.
    
    This model stores all information related to an emergency contact including
    personal details, notification preferences, and event types that trigger
    notifications.
    
    Attributes:
        first_name (str): First name of the contact (max 50 characters)
        last_name (str): Last name of the contact (max 50 characters)
        email (str): Email address (unique, required)
        country_code (str): Country code for mobile number (optional, max 5 characters)
        mobile_number (str): Mobile phone number (optional, max 20 characters)
        event_notification_type (str): Type of notification (ALL_USERS or GROUPS)
        event_notification_groups (str): Groups to notify if type is GROUPS
        event_types (list): List of event types that trigger notifications
        status (str): Current status of the contact (ACTIVE or INACTIVE)
        created_at (datetime): Timestamp when the record was created
        updated_at (datetime): Timestamp when the record was last updated
    """

    # Choice constants for event notification types
    EVENT_NOTIFICATION_TYPE_CHOICES = [
        ('ALL_USERS', 'All Users'),
        ('GROUPS', 'Groups'),
    ]

    # Choice constants for contact status
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]

    # Personal Information Fields
    first_name = models.CharField(
        max_length=50,
        help_text='First name of the contact (max 50 characters)'
    )
    last_name = models.CharField(
        max_length=50,
        help_text='Last name of the contact (max 50 characters)'
    )
    email = models.EmailField(
        unique=True,
        help_text='Email address of the contact (must be unique)'
    )
    country_code = models.CharField(
        max_length=5,
        blank=True,
        default='',
        help_text='Country code for mobile number (e.g., +91, +1)'
    )
    mobile_number = models.CharField(
        max_length=20,
        blank=True,
        help_text='Mobile phone number (optional, max 20 characters)'
    )

    # Notification Configuration Fields
    event_notification_type = models.CharField(
        max_length=20,
        choices=EVENT_NOTIFICATION_TYPE_CHOICES,
        default='ALL_USERS',
        help_text='Type of notification: ALL_USERS or GROUPS'
    )
    event_notification_groups = models.TextField(
        blank=True,
        null=True,
        help_text='Groups to notify (required if event_notification_type is GROUPS)'
    )

    # Event Types - stored as JSON array (e.g., ["SOS", "911"])
    event_types = models.JSONField(
        help_text='List of event types that trigger notifications for this contact'
    )

    # Status Field
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE',
        help_text='Current status of the contact: ACTIVE or INACTIVE'
    )

    # Timestamp Fields (automatically managed)
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Timestamp when the contact was created'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='Timestamp when the contact was last updated'
    )

    class Meta:
        """
        Metadata options for the Contact model.
        
        Configures verbose names for admin interface and default ordering.
        """
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ['-created_at']  # Most recent contacts first

    def __str__(self) -> str:
        """
        String representation of the Contact instance.
        
        Returns:
            str: Full name of the contact
        """
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self) -> str:
        """
        Get the full name of the contact.
        
        Returns:
            str: Full name combining first and last name
        """
        return f"{self.first_name} {self.last_name}"

    def is_active(self) -> bool:
        """
        Check if the contact is currently active.
        
        Returns:
            bool: True if status is ACTIVE, False otherwise
        """
        return self.status == 'ACTIVE'
