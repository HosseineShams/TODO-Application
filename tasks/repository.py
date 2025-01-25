from .models import Task
from django.db.models import QuerySet
from typing import Optional


class TaskRepository:
    """Repository for interacting with the Task model."""

    @staticmethod
    def create_task(**kwargs) -> Task:
        """Create a new Task instance."""
        return Task.objects.create(**kwargs)

    @staticmethod
    def get_all_tasks() -> QuerySet:
        """Retrieve all tasks."""
        return Task.objects.all()

    @staticmethod
    def get_task_by_id(task_id: int) -> Optional[Task]:
        """Retrieve a task by its ID."""
        try:
            return Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return None

    @staticmethod
    def get_filtered_tasks(**filters) -> QuerySet:
        """Retrieve tasks based on filters."""
        return Task.objects.filter(**filters)

    @staticmethod
    def update_task(task: Task, **kwargs) -> Task:
        """Update an existing task."""
        for field, value in kwargs.items():
            setattr(task, field, value)
        task.save()
        return task

    @staticmethod
    def delete_task(task: Task) -> None:
        """Delete an existing task."""
        task.delete()
