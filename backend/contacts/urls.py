"""
URL patterns for the contacts app.

Routes are prefixed with `/api/` in the project URL configuration.
This means the full URL paths will be:
- /api/items/ - List and create contacts
- /api/items/{id}/ - Retrieve, update, or delete a specific contact

All endpoints return JSON responses and support proper HTTP status codes.
"""
from django.urls import path
from .views import ContactListCreateView, ContactRetrieveUpdateDestroyView

# URL patterns for the contacts API
# These routes map to the view classes that handle HTTP methods
urlpatterns = [
    # List all contacts (GET) or create a new contact (POST)
    # Supports pagination via query parameters: ?page=1&page_size=10
    path('items/', ContactListCreateView.as_view(), name='contact-list'),
    
    # Retrieve (GET), update (PUT/PATCH), or delete (DELETE) a specific contact by ID
    # PUT: Full update (all fields required)
    # PATCH: Partial update (only provided fields)
    path('items/<int:pk>/', ContactRetrieveUpdateDestroyView.as_view(), name='contact-detail'),
]
