from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """Model-level validation for Task."""
        # Ensure the due_date is not in the past
        if self.due_date < now():
            raise ValidationError("The due date cannot be in the past.")

        # Ensure the title is not blank
        if not self.title.strip():
            raise ValidationError("The title cannot be blank.")

    def save(self, *args, **kwargs):
        """Override save to include validation."""
        self.full_clean()  # Call clean() before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
