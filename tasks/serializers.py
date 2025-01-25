from rest_framework import serializers
from tasks.models import Task
from django.utils.timezone import now


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'completed', 'priority', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_due_date(self, value):
        """Field-level validation for due_date."""
        if value < now():
            raise serializers.ValidationError("The due date cannot be in the past.")
        return value

    def validate_title(self, value):
        """Field-level validation for title."""
        if not value.strip():
            raise serializers.ValidationError("The title cannot be blank.")
        return value

    def validate(self, data):
        """Object-level validation."""
        # Example: Add more complex cross-field validation if needed
        if data.get('priority') == 'high' and not data.get('description'):
            raise serializers.ValidationError("High priority tasks must have a description.")
        return data
