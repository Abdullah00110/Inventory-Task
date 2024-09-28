# Inventory Management System

## Overview

The **Inventory Management System** is a RESTful web service built with Django and Django REST Framework. It provides endpoints for creating, retrieving, updating, and deleting items. The API is equipped with authentication, Redis caching for performance, and logging for better monitoring.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete items.
- **Authentication**: Secure API access using token-based authentication.
- **Caching**: Utilizes Redis for caching frequently accessed data to improve performance.
- **Logging**: Configured logging to monitor application behavior and errors.
- **Testing**: Comprehensive test coverage for all endpoints.

## Technologies Used

- Django
- Django REST Framework
- Redis
- Python
- PostgreSQL (or any database of your choice)
- Docker (optional, for containerization)

## Getting Started

### Prerequisites

- Python 3.x
- Django
- Django REST Framework
- Redis server
- PostgreSQL (or another database)

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/item-management-api.git
   cd item-management-api

2. **Create a virtual environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
4. **Set up environment variables:
   Create a .env file in the root directory and add your configuration:**
   ```
   SECRET_KEY='your-secret-key'
   DEBUG=True
   DATABASE_URL='your-database-url'
   REDIS_URL='redis://localhost:6379/0'
   ```
5. **Run migrations:**
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
6. **Run the server:**
   ```
   python manage.py runserver
   ```
7. **API Endpoints
   Here are the available API endpoints for the Item Management API:**
   ```
   | Method | Endpoint              | Description                      |
   |--------|-----------------------|----------------------------------|
   | POST   | `/api/items/`         | Create a new item                |
   | GET    | `/api/items/`         | List all items                   |
   | GET    | `/api/items/{id}/`    | Retrieve a specific item         |
   | PUT    | `/api/items/{id}/`    | Update a specific item           |
   | DELETE | `/api/items/{id}/`    | Delete a specific item           |
   ```
8. **Authentication**
   ```Register a new user via the registration endpoint.
      Use token authentication to access protected endpoints.```
9. **Running Tests
   To run the tests for the API, use the following command:**
   ```python manage.py test items```
   
11. **Logging**
    Logging is configured to log messages to both console and a file (debug.log). Modify the logging configuration in settings.py as needed.

12. **Caching**
    The API uses Redis for caching item data. Ensure that the Redis server is running to take advantage of this feature.

13. **Contributing**
    ```Fork the repository.
       1. Create a new branch (git checkout -b feature-branch).
       2. Make your changes and commit them (git commit -m 'Add new feature').
       3. Push to the branch (git push origin feature-branch).
       4. Create a new Pull Request.```
    
14. **License**
    This project is licensed under the MIT License - see the LICENSE file for details.






