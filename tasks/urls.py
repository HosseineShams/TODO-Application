from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from tasks.views import TaskListView, TaskDetailView

urlpatterns = [
    # JWT Authentication Endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # CRUD Endpoints for Tasks
    path('tasks/', TaskListView.as_view(), name='task_list'),  # List & Create
    path('tasks/<int:task_id>/', TaskDetailView.as_view(), name='task_detail'),  # Retrieve, Update, Delete

]
