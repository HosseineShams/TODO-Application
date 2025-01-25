from .repository import TaskRepository
from django.core.exceptions import ValidationError
from .models import Task
from typing import Optional
from django.utils.timezone import now


class TaskService:
    """Service layer for handling business logic related to tasks."""

    @staticmethod
    def create_task(data: dict) -> Task:
        """Create a new task with business logic validation."""
        # Validate that due_date is not in the past
        due_date = data.get('due_date')
        if due_date and due_date < now():
            raise ValidationError("The due date cannot be in the past.")

        # Delegate to repository to create the task
        return TaskRepository.create_task(**data)

    @staticmethod
    def update_task(task_id: int, data: dict) -> Optional[Task]:
        """Update an existing task with business logic validation."""
        task = TaskRepository.get_task_by_id(task_id)
        if not task:
            return None

        # Validate that due_date is not in the past if being updated
        due_date = data.get('due_date')
        if due_date and due_date < now():
            raise ValidationError("The due date cannot be in the past.")

        # Delegate to repository to update the task
        return TaskRepository.update_task(task, **data)

    @staticmethod
    def delete_task(task_id: int) -> bool:
        """Delete a task."""
        task = TaskRepository.get_task_by_id(task_id)
        if not task:
            return False

        # Delegate to repository to delete the task
        TaskRepository.delete_task(task)
        return True

    @staticmethod
    def get_task_by_id(task_id: int) -> Optional[Task]:
        """Retrieve a task by ID."""
        return TaskRepository.get_task_by_id(task_id)

    @staticmethod
    def get_all_tasks() -> list:
        """Retrieve all tasks."""
        return TaskRepository.get_all_tasks()

    @staticmethod
    def get_filtered_tasks(filters: dict) -> list:
        """Retrieve tasks based on filters."""
        return TaskRepository.get_filtered_tasks(**filters)
