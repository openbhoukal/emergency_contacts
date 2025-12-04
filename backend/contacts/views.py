"""
REST views for the emergency contacts application.

These generic class‑based views provide CRUD operations for the Contact
model with proper error handling, pagination, and input validation.

Endpoints provided:
- GET /api/items/ - List all contacts (paginated)
- POST /api/items/ - Create a new contact
- GET /api/items/{id}/ - Retrieve a single contact
- PUT /api/items/{id}/ - Update an existing contact
- DELETE /api/items/{id}/ - Delete a contact
"""
from rest_framework import generics, status, filters  # type: ignore
from rest_framework.response import Response
from django.http import Http404
from django.db import IntegrityError
from .models import Contact
from .serializers import ContactSerializer
from .pagination import ContactPageNumberPagination


class ContactListCreateView(generics.ListCreateAPIView):
    """
    List all contacts or create a new contact.
    
    GET:
    - Returns a paginated list of all contacts
    - Supports query parameters:
      * page: Page number (default: 1)
      * page_size: Items per page (default: 10, max: 100)
      * search: Search across first_name, last_name, email, and mobile_number (case-insensitive)
      * status: Filter by status (ACTIVE or INACTIVE)
      * event_notification_type: Filter by notification type (ALL_USERS or GROUPS)
      * ordering: Sort by field (e.g., first_name, last_name, email, created_at, updated_at)
                 Use - prefix for descending order (e.g., -created_at)
    - Returns 200 OK with paginated data
    
    POST:
    - Creates a new contact
    - Validates all required fields
    - Returns 201 Created with the created contact data
    - Returns 400 Bad Request with validation errors if data is invalid
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    pagination_class = ContactPageNumberPagination
    
    # Enable search, filter, and ordering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
    # Search fields - searches across first_name, last_name, email, and mobile_number
    search_fields = ['first_name', 'last_name', 'email', 'mobile_number']
    
    # Ordering fields - allows sorting by these fields
    ordering_fields = ['first_name', 'last_name', 'email', 'status', 'created_at', 'updated_at']
    ordering = ['-created_at']  # Default ordering (most recent first)
    
    def get_queryset(self):
        """
        Override get_queryset to add custom filtering.
        
        Supports filtering by:
        - status: Filter by ACTIVE or INACTIVE
        - event_notification_type: Filter by ALL_USERS or GROUPS
        
        Returns:
            QuerySet: Filtered and ordered queryset
        """
        queryset = super().get_queryset()
        
        # Filter by status if provided
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param.upper())
        
        # Filter by event_notification_type if provided
        notification_type = self.request.query_params.get('event_notification_type', None)
        if notification_type:
            queryset = queryset.filter(event_notification_type=notification_type.upper())
        
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Create a new contact instance.
        
        Overrides the default create method to provide better error handling
        and consistent JSON responses.
        
        Args:
            request: HTTP request object containing the data to create
            
        Returns:
            Response: JSON response with created contact or error details
        """
        serializer = self.get_serializer(data=request.data)
        
        try:
            # Validate the data
            serializer.is_valid(raise_exception=True)
            
            # Save the new contact
            self.perform_create(serializer)
            
            # Return success response with created data
            headers = self.get_success_headers(serializer.data)
            return Response(
                {
                    'message': 'Contact created successfully.',
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except IntegrityError as e:
            # Handle database integrity errors (e.g., duplicate email)
            error_message = 'A contact with this email address already exists.'
            if 'email' not in str(e).lower():
                error_message = 'An error occurred while creating the contact. Please check your data.'
            
            return Response(
                {
                    'error': {
                        'message': error_message,
                        'code': 'integrity_error',
                        'status_code': status.HTTP_400_BAD_REQUEST,
                    },
                    'detail': error_message
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class ContactRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a single contact by primary key.
    
    GET /api/items/{id}/:
    - Returns a single contact by ID
    - Returns 200 OK with contact data
    - Returns 404 Not Found if contact doesn't exist
    
    PUT /api/items/{id}/:
    - Updates an existing contact (full update - all fields required)
    - Validates all fields
    - Returns 200 OK with updated contact data
    - Returns 400 Bad Request with validation errors if data is invalid
    - Returns 404 Not Found if contact doesn't exist
    
    PATCH /api/items/{id}/:
    - Partially updates an existing contact (only provided fields)
    - Validates only provided fields
    - Returns 200 OK with updated contact data
    - Returns 400 Bad Request with validation errors if data is invalid
    - Returns 404 Not Found if contact doesn't exist
    
    DELETE /api/items/{id}/:
    - Deletes an existing contact
    - Returns 200 OK with success message
    - Returns 404 Not Found if contact doesn't exist
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get_object(self):
        """
        Retrieve a single contact instance by primary key.
        
        Overrides default method to provide better error messages.
        
        Returns:
            Contact: The contact instance
            
        Raises:
            Http404: If contact doesn't exist
        """
        try:
            return super().get_object()
        except Http404:
            # Provide a more descriptive error message
            pk = self.kwargs.get('pk')
            raise Http404(f'Contact with id {pk} does not exist.')

    def update(self, request, *args, **kwargs):
        """
        Update an existing contact instance (full update).
        
        Overrides the default update method to provide better error handling
        and consistent JSON responses.
        
        Args:
            request: HTTP request object containing the updated data
            
        Returns:
            Response: JSON response with updated contact or error details
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        try:
            # Validate the data
            serializer.is_valid(raise_exception=True)
            
            # Save the updated contact
            self.perform_update(serializer)
            
            # Return success response with updated data
            return Response(
                {
                    'message': 'Contact updated successfully.',
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        except IntegrityError as e:
            # Handle database integrity errors (e.g., duplicate email)
            error_message = 'A contact with this email address already exists.'
            if 'email' not in str(e).lower():
                error_message = 'An error occurred while updating the contact. Please check your data.'
            
            return Response(
                {
                    'error': {
                        'message': error_message,
                        'code': 'integrity_error',
                        'status_code': status.HTTP_400_BAD_REQUEST,
                    },
                    'detail': error_message
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        """
        Delete an existing contact instance.
        
        Overrides the default destroy method to provide better error handling
        and consistent JSON responses.
        
        Args:
            request: HTTP request object
            
        Returns:
            Response: JSON response indicating success or error
        """
        instance = self.get_object()
        
        try:
            # Delete the contact
            self.perform_destroy(instance)
            
            # Return success response
            return Response(
                {
                    'message': 'Contact deleted successfully.'
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            # Handle any unexpected errors during deletion
            return Response(
                {
                    'error': {
                        'message': 'An error occurred while deleting the contact.',
                        'code': 'deletion_error',
                        'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    },
                    'detail': str(e) if request.user.is_staff else 'Contact could not be deleted.'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
