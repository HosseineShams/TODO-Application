import django_filters
from tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    """FilterSet for filtering tasks."""
    title = django_filters.CharFilter(lookup_expr='icontains')  # Search by title (case-insensitive)
    description = django_filters.CharFilter(lookup_expr='icontains')  # Search by description
    due_date = django_filters.DateFromToRangeFilter()  # Filter by due_date range
    completed = django_filters.BooleanFilter()  # Filter by completed status
    priority = django_filters.ChoiceFilter(choices=Task.PRIORITY_CHOICES)  # Filter by priority

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'completed', 'priority']
