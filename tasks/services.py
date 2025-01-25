from .repository import TaskRepository
from .decorators import log_method_call, handle_exceptions
from django.core.exceptions import ValidationError
from .models import Task
from typing import Optional
from django.utils.timezone import now
from tasks.config import AppConfig
from django.utils.dateparse import parse_datetime
import logging

logger = logging.getLogger('tasks')

class TaskService:
    """Service layer for handling business logic related to tasks."""

    @staticmethod
    @log_method_call
    @handle_exceptions
    def create_task(data: dict) -> Task:
        """Create a new task with business logic validation."""
        logger.info(f"Creating task with data: {data}")
        due_date = data.get('due_date')

        # Check if due_date is already a datetime object
        if isinstance(due_date, str):
            due_date = parse_datetime(due_date)
            if not due_date:
                logger.error("Invalid due_date format. Must be ISO-8601 compliant.")
                raise ValidationError("Invalid due_date format. Must be ISO-8601 compliant.")

        # Validate that due_date is not in the past
        if due_date < now():
            logger.error("The due date cannot be in the past.")
            raise ValidationError("The due date cannot be in the past.")

        data['due_date'] = due_date  # Ensure the data contains a valid datetime object
        task = TaskRepository.create_task(**data)
        logger.info(f"Task created successfully: {task.title}")
        return task

    @staticmethod
    @log_method_call
    @handle_exceptions
    def update_task(task_id: int, data: dict) -> Optional[Task]:
        """Update an existing task with business logic validation."""
        logger.info(f"Updating task {task_id} with data: {data}")
        task = TaskRepository.get_task_by_id(task_id)
        if not task:
            logger.warning(f"Task {task_id} not found for update.")
            return None

        # Parse and validate due_date
        due_date = data.get('due_date')

        # Check if due_date is already a datetime object
        if isinstance(due_date, str):
            due_date = parse_datetime(due_date)
            if not due_date:
                logger.error("Invalid due_date format. Must be ISO-8601 compliant.")
                raise ValidationError("Invalid due_date format. Must be ISO-8601 compliant.")

        # Validate that due_date is not in the past
        if due_date < now():
            logger.error("The due date cannot be in the past.")
            raise ValidationError("The due date cannot be in the past.")

        # Update the parsed datetime in the data dictionary
        data['due_date'] = due_date

        # Delegate to the repository to update the task
        updated_task = TaskRepository.update_task(task, **data)
        logger.info(f"Task {task_id} updated successfully.")
        return updated_task

    @staticmethod
    @log_method_call
    @handle_exceptions
    def delete_task(task_id: int) -> bool:
        """Delete a task."""
        logger.info(f"Deleting task with ID {task_id}")
        task = TaskRepository.get_task_by_id(task_id)
        if not task:
            logger.warning(f"Task {task_id} not found for deletion.")
            return False

        TaskRepository.delete_task(task)
        logger.info(f"Task {task_id} deleted successfully.")
        return True

    @staticmethod
    @log_method_call
    @handle_exceptions
    def get_task_by_id(task_id: int) -> Optional[Task]:
        """Retrieve a task by ID."""
        logger.info(f"Fetching task with ID {task_id}")
        task = TaskRepository.get_task_by_id(task_id)
        if not task:
            logger.warning(f"Task {task_id} not found.")
        return task

    @staticmethod
    @log_method_call
    @handle_exceptions
    def get_all_tasks() -> list:
        """Retrieve all tasks."""
        logger.info("Fetching all tasks")
        tasks = TaskRepository.get_all_tasks()
        logger.debug(f"Total tasks retrieved: {len(tasks)}")
        return tasks

    @staticmethod
    @log_method_call
    @handle_exceptions
    def get_filtered_tasks(filters: dict) -> list:
        """Retrieve tasks based on filters."""
        logger.info(f"Fetching tasks with filters: {filters}")
        tasks = TaskRepository.get_filtered_tasks(**filters)
        logger.debug(f"Total tasks retrieved after filtering: {len(tasks)}")
        return tasks

    @staticmethod
    def get_paginated_tasks(page: int):
        """Retrieve paginated tasks."""
        logger.info(f"Fetching paginated tasks for page {page}")
        config = AppConfig()
        page_size = config.default_pagination_size

        # Simulated pagination logic (for demonstration purposes)
        tasks = TaskRepository.get_all_tasks()
        start = (page - 1) * page_size
        end = start + page_size
        paginated_tasks = tasks[start:end]
        logger.debug(f"Paginated tasks retrieved: {len(paginated_tasks)}")
        return paginated_tasks
