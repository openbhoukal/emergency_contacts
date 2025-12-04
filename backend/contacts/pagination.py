"""
Custom pagination classes for the contacts API.

Provides pagination configuration to ensure consistent paginated responses
across all list endpoints.
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from typing import Any, Dict


class ContactPageNumberPagination(PageNumberPagination):
    """
    Custom pagination class for contact list endpoints.
    
    Provides paginated responses with metadata including:
    - Total count of items
    - Current page number
    - Total number of pages
    - Links to next and previous pages
    
    Example response:
    {
        "count": 100,
        "next": "http://example.com/api/items/?page=3",
        "previous": "http://example.com/api/items/?page=1",
        "results": [...]
    }
    """
    # Number of items per page (can be overridden by ?page_size query parameter)
    page_size = 10
    
    # Maximum page size that can be requested via ?page_size
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    # Query parameter name for page number
    page_query_param = 'page'

    def get_paginated_response(self, data: list) -> Response:
        """
        Return a paginated Response object.
        
        Args:
            data: The serialized data for the current page
            
        Returns:
            Response object with pagination metadata and results
        """
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
            'page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'page_size': self.page_size,
        })

    def get_paginated_response_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Return schema for paginated response.
        
        Used for API documentation generation.
        
        Args:
            schema: The schema for a single item
            
        Returns:
            Schema for paginated response
        """
        return {
            'type': 'object',
            'properties': {
                'count': {
                    'type': 'integer',
                    'description': 'Total number of items'
                },
                'next': {
                    'type': 'string',
                    'nullable': True,
                    'description': 'URL to next page'
                },
                'previous': {
                    'type': 'string',
                    'nullable': True,
                    'description': 'URL to previous page'
                },
                'results': {
                    'type': 'array',
                    'items': schema
                },
                'page': {
                    'type': 'integer',
                    'description': 'Current page number'
                },
                'total_pages': {
                    'type': 'integer',
                    'description': 'Total number of pages'
                },
                'page_size': {
                    'type': 'integer',
                    'description': 'Number of items per page'
                },
            }
        }

