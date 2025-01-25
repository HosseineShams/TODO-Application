from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from tasks.services import TaskService
from tasks.filters import TaskFilter
from tasks.serializers import TaskSerializer
from tasks.config import AppConfig  # For default pagination size
from django.core.exceptions import ValidationError
from rest_framework.exceptions import NotFound


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
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TaskFilter  # Use TaskFilter for filtering
    ordering_fields = ['due_date', 'priority', 'created_at']  # Allow sorting by these fields

    def get(self, request):
        """List all tasks with filtering, sorting, and pagination."""
        tasks = TaskService.get_all_tasks()

        # Apply filtering and sorting
        filter_backend = DjangoFilterBackend()
        tasks = filter_backend.filter_queryset(request, tasks, self)
        
        ordering_backend = OrderingFilter()
        tasks = ordering_backend.filter_queryset(request, tasks, self)

        # Apply pagination
        paginator = CustomPagination()
        paginated_tasks = paginator.paginate_queryset(tasks, request)
        serialized_tasks = TaskSerializer(paginated_tasks, many=True).data
        return paginator.get_paginated_response(serialized_tasks)

    def post(self, request):
        """Create a new task."""
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = TaskService.create_task(serializer.validated_data)
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
    """Handle retrieving, updating, and deleting a single task."""
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        """Retrieve a task by ID."""
        task = TaskService.get_task_by_id(task_id)
        if not task:
            raise NotFound(detail="Task not found")
        return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)

    def put(self, request, task_id):
        """Update a task by ID."""
        task = TaskService.get_task_by_id(task_id)
        if not task:
            raise NotFound(detail="Task not found")

        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            updated_task = TaskService.update_task(task_id, serializer.validated_data)
            return Response(TaskSerializer(updated_task).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id):
        """Delete a task by ID."""
        success = TaskService.delete_task(task_id)
        if not success:
            raise NotFound(detail="Task not found")
        return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
