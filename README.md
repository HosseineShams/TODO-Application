# TODO Application

This is a Django-based TODO application with a RESTful API powered by Django Rest Framework (DRF). The application supports task management features like creating, updating, deleting, and viewing tasks. It is designed using modern best practices and incorporates multiple design patterns for maintainability and scalability.

## **Features**
- Create, update, delete, and list tasks.
- Filtering, sorting, and pagination for task lists.
- Token-based authentication for secure access.
- Caching for frequently accessed endpoints.
- Robust error handling and logging.

## **Technologies Used**
- **Backend**: Django, Django Rest Framework
- **Caching**: Django's caching framework (LocMemCache)
- **API Testing**: Postman (https://documenter.getpostman.com/view/25778869/2sAYQgfnXQ)

## **Design Patterns Used**
1. **Repository Pattern**: Abstracts database interactions for task operations.
2. **Service Layer Pattern**: Encapsulates business logic for task management.
3. **Decorator Pattern**: Used for logging and error handling at the method level.
4. **Singleton Pattern**: Manages application-wide configuration settings.
