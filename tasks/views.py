from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from tasks.services import TaskService

class TaskListView(APIView):
    """View to list all tasks for an authenticated user."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = TaskService.get_all_tasks()
        serialized_tasks = [{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks]
        return Response(serialized_tasks)
