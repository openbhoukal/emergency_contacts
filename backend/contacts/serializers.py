"""
Serializers for the emergency contacts REST API.

Serializers translate model instances into JSON representations and
validate incoming request data before saving it to the database.

This module provides comprehensive input validation for all fields,
ensuring data integrity and proper error messages.
"""
import re
from rest_framework import serializers  # type: ignore
from .models import Contact


class EventNotificationGroupsField(serializers.Field):
    """
    Custom field that accepts both string and array formats for event_notification_groups.
    
    Converts arrays to comma-separated strings for storage in the TextField.
    """
    
    def to_internal_value(self, data):
        """
        Convert input data to internal value.
        
        Accepts:
        - String: Returns as-is (after stripping)
        - Array: Converts to comma-separated string
        - None/empty: Returns empty string
        """
        if data is None:
            return ''
        
        if isinstance(data, list):
            if not data:
                return ''
            # Validate all items are strings
            validated_items = []
            for item in data:
                if not isinstance(item, str):
                    raise serializers.ValidationError(
                        'All group items must be strings.'
                    )
                item = item.strip()
                if not item:
                    raise serializers.ValidationError(
                        'Group items cannot be empty strings.'
                    )
                validated_items.append(item)
            # Return comma-separated string
            return ', '.join(validated_items)
        
        if isinstance(data, str):
            return data.strip() if data.strip() else ''
        
        raise serializers.ValidationError(
            'Event notification groups must be a string or an array of strings.'
        )
    
    def to_representation(self, value):
        """
        Convert internal value to representation.
        
        Returns the string value as-is for API responses.
        """
        return value if value else ''


class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contact model.
    
    Provides comprehensive validation for all fields including:
    - Email format validation
    - Mobile number format validation
    - Event types validation
    - Status and notification type validation
    """
    
    # Explicit field definitions with validation
    email = serializers.EmailField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Email field is required.',
            'invalid': 'Enter a valid email address.',
        }
    )
    
    first_name = serializers.CharField(
        max_length=50,
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'First name is required.',
            'blank': 'First name cannot be blank.',
            'max_length': 'First name cannot exceed 50 characters.',
        }
    )
    
    last_name = serializers.CharField(
        max_length=50,
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Last name is required.',
            'blank': 'Last name cannot be blank.',
            'max_length': 'Last name cannot exceed 50 characters.',
        }
    )
    
    country_code = serializers.CharField(
        max_length=5,
        required=False,
        allow_blank=True,
        error_messages={
            'max_length': 'Country code cannot exceed 5 characters.',
        },
        help_text='Country code for mobile number (e.g., +91, +1)'
    )
    
    mobile_number = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        error_messages={
            'max_length': 'Mobile number cannot exceed 20 characters.',
        }
    )
    
    # Custom field to handle event_notification_groups as both string and array
    event_notification_groups = EventNotificationGroupsField(
        required=False,
        allow_null=True,
        help_text='Groups to notify (can be a string or array of strings)'
    )

    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_first_name(self, value: str) -> str:
        """
        Validate first name format.
        
        Args:
            value: The first name to validate
            
        Returns:
            The validated first name
            
        Raises:
            serializers.ValidationError: If validation fails
        """
        if not value or not value.strip():
            raise serializers.ValidationError('First name cannot be empty or whitespace only.')
        
        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        if not re.match(r"^[a-zA-Z\s\-']+$", value.strip()):
            raise serializers.ValidationError('First name can only contain letters, spaces, hyphens, and apostrophes.')
        
        return value.strip()

    def validate_last_name(self, value: str) -> str:
        """
        Validate last name format.
        
        Args:
            value: The last name to validate
            
        Returns:
            The validated last name
            
        Raises:
            serializers.ValidationError: If validation fails
        """
        if not value or not value.strip():
            raise serializers.ValidationError('Last name cannot be empty or whitespace only.')
        
        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        if not re.match(r"^[a-zA-Z\s\-']+$", value.strip()):
            raise serializers.ValidationError('Last name can only contain letters, spaces, hyphens, and apostrophes.')
        
        return value.strip()

    def validate_email(self, value: str) -> str:
        """
        Validate email address format and uniqueness (for creation).
        
        Args:
            value: The email address to validate
            
        Returns:
            The validated email address (lowercased)
            
        Raises:
            serializers.ValidationError: If validation fails
        """
        if not value or not value.strip():
            raise serializers.ValidationError('Email cannot be empty.')
        
        email = value.strip().lower()
        
        # Additional email format check (beyond DRF's EmailField)
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise serializers.ValidationError('Enter a valid email address.')
        
        return email

    def validate_country_code(self, value: str) -> str:
        """
        Validate country code format (optional field).
        
        Args:
            value: The country code to validate (can be empty string or None)
            
        Returns:
            The validated country code or empty string
            
        Raises:
            serializers.ValidationError: If validation fails
        """
        # Handle None, empty string, or whitespace-only values
        if not value or (isinstance(value, str) and not value.strip()):
            return ''
        
        country_code = value.strip()
        
        # Country code should start with + and contain only digits after +
        if not country_code.startswith('+'):
            raise serializers.ValidationError(
                'Country code must start with a plus sign (+).'
            )
        
        # Check if the part after + contains only digits
        digits_part = country_code[1:]
        if not digits_part.isdigit():
            raise serializers.ValidationError(
                'Country code can only contain a plus sign (+) followed by digits.'
            )
        
        # Validate length (including + sign, typically 1-4 digits)
        if len(digits_part) < 1 or len(digits_part) > 4:
            raise serializers.ValidationError(
                'Country code must contain 1 to 4 digits after the plus sign.'
            )
        
        return country_code

    def validate_mobile_number(self, value: str) -> str:
        """
        Validate mobile number format (optional field).
        
        Args:
            value: The mobile number to validate (can be empty string or None)
            
        Returns:
            The validated mobile number or empty string
            
        Raises:
            serializers.ValidationError: If validation fails
        """
        # Handle None, empty string, or whitespace-only values
        if not value or (isinstance(value, str) and not value.strip()):
            return ''
        
        mobile = value.strip()
        
        # Allow digits, spaces, hyphens, parentheses, and plus sign
        # Remove common formatting characters for validation
        cleaned = re.sub(r'[\s\-\(\)\+]', '', mobile)
        
        # Check if remaining characters are all digits
        if not cleaned.isdigit():
            raise serializers.ValidationError(
                'Mobile number can only contain digits, spaces, hyphens, parentheses, and plus sign.'
            )
        
        # Check length (minimum 10 digits, maximum 15 for international)
        if len(cleaned) < 10 or len(cleaned) > 15:
            raise serializers.ValidationError(
                'Mobile number must contain between 10 and 15 digits.'
            )
        
        return mobile


    def validate_event_types(self, value):  # type: ignore[override]
        """
        Validate event_types field.
        
        Ensures that event_types is a non-empty list of non-empty strings.
        
        Args:
            value: The event types list to validate
            
        Returns:
            The validated list of event types
            
        Raises:
            serializers.ValidationError: If validation fails
        """
        if not isinstance(value, list):
            raise serializers.ValidationError('Event types must be a list.')
        
        if not value:
            raise serializers.ValidationError('At least one event type is required.')
        
        if len(value) > 20:  # Reasonable limit
            raise serializers.ValidationError('Cannot specify more than 20 event types.')
        
        validated_types = []
        for event_type in value:
            if not isinstance(event_type, str):
                raise serializers.ValidationError('Each event type must be a string.')
            
            event_type = event_type.strip()
            if not event_type:
                raise serializers.ValidationError('Event types cannot be empty strings.')
            
            if len(event_type) > 50:
                raise serializers.ValidationError('Each event type cannot exceed 50 characters.')
            
            validated_types.append(event_type)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_types = []
        for event_type in validated_types:
            if event_type not in seen:
                seen.add(event_type)
                unique_types.append(event_type)
        
        return unique_types

    def validate_status(self, value: str) -> str:
        """
        Validate status field value.
        
        Args:
            value: The status value to validate
            
        Returns:
            The validated status
            
        Raises:
            serializers.ValidationError: If validation fails
        """
        valid_statuses = [choice[0] for choice in Contact.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f'Status must be one of: {", ".join(valid_statuses)}'
            )
        return value

    def validate_event_notification_type(self, value: str) -> str:
        """
        Validate event_notification_type field value.
        
        Args:
            value: The notification type value to validate
            
        Returns:
            The validated notification type
            
        Raises:
            serializers.ValidationError: If validation fails
        """
        valid_types = [choice[0] for choice in Contact.EVENT_NOTIFICATION_TYPE_CHOICES]
        if value not in valid_types:
            raise serializers.ValidationError(
                f'Event notification type must be one of: {", ".join(valid_types)}'
            )
        return value

    def validate(self, attrs: dict) -> dict:
        """
        Perform cross-field validation.
        
        Args:
            attrs: Dictionary of validated field values
            
        Returns:
            Dictionary of validated attributes
            
        Raises:
            serializers.ValidationError: If validation fails
        """
        # If event_notification_type is GROUPS, event_notification_groups should be provided
        if attrs.get('event_notification_type') == 'GROUPS':
            groups = attrs.get('event_notification_groups', '')
            # Check if groups is empty (handles both string and None)
            if not groups or (isinstance(groups, str) and not groups.strip()):
                raise serializers.ValidationError({
                    'event_notification_groups': 'This field is required when event_notification_type is GROUPS.'
                })
        
        return attrs
