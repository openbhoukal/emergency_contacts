# Backend – Django REST Framework API

This directory contains the Python/Django implementation of the **Emergency Contacts** REST API. The backend exposes a comprehensive CRUD interface to manage contact records, stores the data in MySQL, and uses Django Rest Framework for serialization, validation, pagination, and error handling.

## Features

- ✅ **Full CRUD Operations** - Create, Read, Update, and Delete contacts
- ✅ **Input Validation** - Comprehensive field-level and cross-field validation
- ✅ **Error Handling** - Custom exception handler with consistent JSON error responses
- ✅ **Pagination** - Built-in pagination support for list endpoints
- ✅ **JSON Responses** - All endpoints return JSON format
- ✅ **RESTful Design** - Follows REST API best practices
- ✅ **Well Documented** - Comprehensive code comments and documentation

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** (Python 3.10+ recommended)
- **MySQL Server 5.7+** or **MySQL 8.0+**
- **pip** (Python package manager)
- **virtualenv** (optional but recommended)

## Installation & Setup

### 1. Clone the Repository

If you haven't already, navigate to the backend directory:

```bash
cd backend
```

### 2. Create Virtual Environment

It's recommended to use a virtual environment to isolate project dependencies:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies

Install all required Python packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

The required packages are:
- `django>=4.2` - Web framework
- `djangorestframework>=3.14` - REST API framework
- `mysqlclient>=2.2` - MySQL database adapter
- `django-cors-headers>=4.9` - CORS handling (if needed)

### 4. Configure Database

#### Option A: Using Environment Variables (Recommended)

Set the following environment variables:

```bash
export MYSQL_DATABASE=emergency_db
export MYSQL_USER=your_mysql_user
export MYSQL_PASSWORD=your_mysql_password
export MYSQL_HOST=127.0.0.1
export MYSQL_PORT=3306
export DJANGO_SECRET_KEY=your-secret-key-here
```

#### Option B: Edit settings.py Directly

Edit `emergency_app/settings.py` and update the `DATABASES` configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'emergency_db',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

#### Create MySQL Database

Create the database in MySQL:

```bash
mysql -u root -p
```

Then in MySQL console:

```sql
CREATE DATABASE emergency_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'your_mysql_user'@'localhost' IDENTIFIED BY 'your_mysql_password';
GRANT ALL PRIVILEGES ON emergency_db.* TO 'your_mysql_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 5. Run Database Migrations

Apply database migrations to create the necessary tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)

Create an admin user to access the Django admin interface:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up your admin credentials.

## Running the Application

### Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The API will be available at:
- **API Base URL**: `http://localhost:8000/api/`
- **Admin Interface**: `http://localhost:8000/admin/`

### Run on Custom Port

To run on a different port (e.g., 8001):

```bash
python manage.py runserver 8001
```

### Run on All Interfaces

To make the server accessible from other machines:

```bash
python manage.py runserver 0.0.0.0:8000
```

## API Endpoints

### Base URL
All API endpoints are prefixed with `/api/`

### Endpoints Overview

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `GET` | `/api/items/` | List all contacts (paginated) | 200 OK |
| `POST` | `/api/items/` | Create a new contact | 201 Created, 400 Bad Request |
| `GET` | `/api/items/{id}/` | Retrieve a single contact | 200 OK, 404 Not Found |
| `PUT` | `/api/items/{id}/` | Full update (all fields required) | 200 OK, 400 Bad Request, 404 Not Found |
| `PATCH` | `/api/items/{id}/` | Partial update (only provided fields) | 200 OK, 400 Bad Request, 404 Not Found |
| `DELETE` | `/api/items/{id}/` | Delete a contact | 200 OK, 404 Not Found |


## Input Validation

The API includes comprehensive input validation:

### Field Validations

- **first_name / last_name**: 
  - Required, non-empty
  - Max 50 characters
  - Only letters, spaces, hyphens, and apostrophes
  
- **email**: 
  - Required, unique
  - Valid email format
  - Automatically lowercased
  
- **mobile_number**: 
  - Optional
  - Max 20 characters
  - 10-15 digits (formatting characters allowed)
  
- **event_types**: 
  - Required, non-empty array
  - Max 20 items
  - Each item: non-empty string, max 50 characters
  - Duplicates automatically removed
  
- **status**: 
  - Required
  - Must be "ACTIVE" or "INACTIVE"
  
- **event_notification_type**: 
  - Required
  - Must be "ALL_USERS" or "GROUPS"
  
- **event_notification_groups**: 
  - Required if `event_notification_type` is "GROUPS"

### Validation Error Response

When validation fails, the API returns a structured error response:

```json
{
  "error": {
    "message": "Validation failed",
    "code": "bad_request",
    "status_code": 400,
    "details": {
      "email": ["A contact with this email address already exists."],
      "first_name": ["First name cannot be empty or whitespace only."]
    }
  },
  "detail": "Validation failed"
}
```

## Error Handling

The API uses a custom exception handler that provides consistent error responses:

### Error Response Format

```json
{
  "error": {
    "message": "Error message description",
    "code": "error_code",
    "status_code": 400
  },
  "detail": "Error message description"
}
```

### Common Error Codes

- `bad_request` (400) - Invalid request data
- `not_found` (404) - Resource not found
- `integrity_error` (400) - Database constraint violation (e.g., duplicate email)
- `validation_error` (400) - Validation failed
- `internal_server_error` (500) - Server error

### Example Error Responses

**404 Not Found:**
```json
{
  "error": {
    "message": "Contact with id 999 does not exist.",
    "code": "not_found",
    "status_code": 404
  },
  "detail": "Contact with id 999 does not exist."
}
```

**400 Bad Request (Duplicate Email):**
```json
{
  "error": {
    "message": "A contact with this email address already exists.",
    "code": "integrity_error",
    "status_code": 400
  },
  "detail": "A contact with this email address already exists."
}
```

## Pagination

List endpoints support pagination with the following query parameters:

- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10, max: 100)

**Pagination Response Structure:**
```json
{
  "count": 100,           // Total number of items
  "next": "http://...",    // URL to next page (null if last page)
  "previous": "http://...", // URL to previous page (null if first page)
  "results": [...],        // Array of contact objects
  "page": 1,              // Current page number
  "total_pages": 10,      // Total number of pages
  "page_size": 10         // Items per page
}
```

## Project Structure

```
backend/
├── contacts/                 # Main application
│   ├── __init__.py
│   ├── models.py            # Database models
│   ├── serializers.py       # API serializers with validation
│   ├── views.py             # API views with error handling
│   ├── urls.py              # URL routing
│   ├── exceptions.py        # Custom exception handler
│   ├── pagination.py        # Custom pagination class
│   ├── admin.py             # Django admin configuration
│   ├── apps.py              # App configuration
│   └── migrations/          # Database migrations
├── emergency_app/           # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Project settings
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── db_schema.sql            # Database schema (optional)
```
