"""
Custom exception handlers for the contacts API.

This module provides a custom exception handler that ensures consistent
JSON error responses across all API endpoints.
"""
from typing import Any, Optional
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from django.core.exceptions import ValidationError as DjangoValidationError


def custom_exception_handler(exc: Exception, context: dict[str, Any]) -> Optional[Response]:
    """
    Custom exception handler for DRF views.
    
    Provides consistent JSON error responses with proper status codes
    and error messages. Handles:
    - DRF API exceptions
    - Database integrity errors
    - Django validation errors
    - Generic exceptions (500 errors)
    
    Args:
        exc: The exception that was raised
        context: Dictionary containing request, view, and other context
        
    Returns:
        Response object with error details, or None if exception should be re-raised
    """
    # Call DRF's default exception handler first
    response = drf_exception_handler(exc, context)
    
    # Handle Django database integrity errors (e.g., unique constraint violations)
    if isinstance(exc, IntegrityError):
        error_message = str(exc)
        
        # Check for common integrity error
        if 'email' in error_message.lower() and 'unique' in error_message.lower():
            error_message = 'A contact with this email address already exists.'
        elif 'unique' in error_message.lower():
            error_message = 'A record with these values already exists.'
        
        custom_response_data = {
            'error': {
                'message': error_message,
                'code': 'integrity_error',
                'status_code': status.HTTP_400_BAD_REQUEST,
            },
            'detail': error_message
        }
        
        response = Response(
            custom_response_data,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Handle Django validation errors
    elif isinstance(exc, DjangoValidationError):
        error_messages = exc.messages if hasattr(exc, 'messages') else [str(exc)]
        custom_response_data = {
            'error': {
                'message': 'Validation failed',
                'code': 'validation_error',
                'status_code': status.HTTP_400_BAD_REQUEST,
                'details': error_messages
            },
            'detail': error_messages
        }
        
        response = Response(
            custom_response_data,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Format DRF exceptions for consistent response structure
    if response is not None:
        custom_response_data = {
            'error': {
                'message': 'An error occurred',
                'code': 'api_error',
                'status_code': response.status_code,
            }
        }
        
        # Extract detail from DRF response
        if hasattr(response, 'data'):
            if isinstance(response.data, dict):
                if 'detail' in response.data:
                    custom_response_data['error']['message'] = response.data['detail']
                elif 'non_field_errors' in response.data:
                    custom_response_data['error']['message'] = response.data['non_field_errors']
                    custom_response_data['error']['details'] = response.data
                else:
                    # Field-specific errors
                    custom_response_data['error']['message'] = 'Validation failed'
                    custom_response_data['error']['details'] = response.data
            elif isinstance(response.data, list):
                custom_response_data['error']['message'] = response.data[0] if response.data else 'An error occurred'
                custom_response_data['error']['details'] = response.data
            else:
                custom_response_data['error']['message'] = str(response.data)
        
        # Map status codes to error codes
        status_code_map = {
            status.HTTP_400_BAD_REQUEST: 'bad_request',
            status.HTTP_401_UNAUTHORIZED: 'unauthorized',
            status.HTTP_403_FORBIDDEN: 'forbidden',
            status.HTTP_404_NOT_FOUND: 'not_found',
            status.HTTP_405_METHOD_NOT_ALLOWED: 'method_not_allowed',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'internal_server_error',
        }
        
        custom_response_data['error']['code'] = status_code_map.get(
            response.status_code,
            'api_error'
        )
        
        # Add detail field for backward compatibility
        custom_response_data['detail'] = custom_response_data['error']['message']
        
        response.data = custom_response_data
        response.content_type = 'application/json'
    
    return response

