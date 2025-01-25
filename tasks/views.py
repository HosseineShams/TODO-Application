from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from tasks.services import TaskService
from tasks.config import AppConfig  # For default pagination size
from django.core.exceptions import ValidationError


class CustomPagination(PageNumberPagination):
    """Custom pagination class to include additional metadata."""
    page_size = AppConfig().default_pagination_size
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """Customize the paginated response structure."""
        return Response({
            'pagination': {
                'current_page': self.page.number,
                'total_pages': self.page.paginator.num_pages,
                'total_items': self.page.paginator.count,
                'page_size': self.page_size,
            },
            'results': data
        })


class TaskListView(APIView):
    """Handle listing all tasks and creating a new task."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List all tasks with pagination."""
        tasks = TaskService.get_all_tasks()
        paginator = CustomPagination()
        paginated_tasks = paginator.paginate_queryset(tasks, request)
        serialized_tasks = [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "completed": t.completed,
                "due_date": t.due_date,
                "priority": t.priority,
            }
            for t in paginated_tasks
        ]
        return paginator.get_paginated_response(serialized_tasks)

    def post(self, request):
        """Create a new task."""
        try:
            task = TaskService.create_task(request.data)
            return Response({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "due_date": task.due_date,
                "priority": task.priority,
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
    """Handle retrieving, updating, and deleting a single task."""
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        """Retrieve a task by ID."""
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "due_date": task.due_date,
            "priority": task.priority,
        }, status=status.HTTP_200_OK)

    def put(self, request, task_id):
        """Update a task by ID."""
        try:
            task = TaskService.update_task(task_id, request.data)
            if not task:
                return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "due_date": task.due_date,
                "priority": task.priority,
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id):
        """Delete a task by ID."""
        success = TaskService.delete_task(task_id)
        if not success:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
