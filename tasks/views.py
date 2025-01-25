from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from tasks.services import TaskService
from django.core.exceptions import ValidationError


class TaskListView(APIView):
    """Handle listing all tasks and creating a new task."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List all tasks."""
        tasks = TaskService.get_all_tasks()
        serialized_tasks = [
            {"id": t.id, "title": t.title, "description": t.description, "completed": t.completed, "due_date": t.due_date, "priority": t.priority} 
            for t in tasks
        ]
        return Response(serialized_tasks, status=status.HTTP_200_OK)

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
