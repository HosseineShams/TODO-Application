from .repository import TaskRepository
from .decorators import log_method_call, handle_exceptions
from django.core.exceptions import ValidationError
from .models import Task
from typing import Optional
from django.utils.timezone import now
from tasks.config import AppConfig


class TaskService:
    """Service layer for handling business logic related to tasks."""

    @staticmethod
    @log_method_call
    @handle_exceptions
    def create_task(data: dict) -> Task:
        """Create a new task with business logic validation."""
        due_date = data.get('due_date')
        if due_date and due_date < now():
            raise ValidationError("The due date cannot be in the past.")
        return TaskRepository.create_task(**data)

    @staticmethod
    @log_method_call
    @handle_exceptions
    def update_task(task_id: int, data: dict) -> Optional[Task]:
        """Update an existing task with business logic validation."""
        task = TaskRepository.get_task_by_id(task_id)
        if not task:
            return None

        due_date = data.get('due_date')
        if due_date and due_date < now():
            raise ValidationError("The due date cannot be in the past.")

        return TaskRepository.update_task(task, **data)

    @staticmethod
    @log_method_call
    @handle_exceptions
    def delete_task(task_id: int) -> bool:
        """Delete a task."""
        task = TaskRepository.get_task_by_id(task_id)
        if not task:
            return False

        TaskRepository.delete_task(task)
        return True

    @staticmethod
    @log_method_call
    @handle_exceptions
    def get_task_by_id(task_id: int) -> Optional[Task]:
        """Retrieve a task by ID."""
        return TaskRepository.get_task_by_id(task_id)

    @staticmethod
    @log_method_call
    @handle_exceptions
    def get_all_tasks() -> list:
        """Retrieve all tasks."""
        return TaskRepository.get_all_tasks()

    @staticmethod
    @log_method_call
    @handle_exceptions
    def get_filtered_tasks(filters: dict) -> list:
        """Retrieve tasks based on filters."""
        return TaskRepository.get_filtered_tasks(**filters)

    @staticmethod
    def get_paginated_tasks(page: int):
        """Retrieve paginated tasks."""
        config = AppConfig()
        page_size = config.default_pagination_size

        # Simulated pagination logic (for demonstration purposes)
        tasks = TaskRepository.get_all_tasks()
        start = (page - 1) * page_size
        end = start + page_size
        return tasks[start:end]