from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager

from task_manager import settings


class Worker(AbstractUser):
    position = models.CharField(max_length=64)
    REQUIRED_FIELDS = ["position"]

    class Meta:
        ordering = ["username"]
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"

    def get_absolute_url(self):
        return reverse(
            "manager:worker-detail",
            kwargs={"pk": self.pk}
        )


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "manager:task-type-detail",
            kwargs={"pk": self.pk}
        )


class Task(models.Model):
    class StatusChoices(models.TextChoices):
        TO_DO = "TD", "To Do"
        IN_PROGRESS = "IP", "In Progress"
        DONE = "DN", "Done"
        ARCHIVED = "AR", "Archived"

    class PriorityOptions(models.TextChoices):
        URGENT = "UR", "Urgent"
        HIGH_PRIORITY = "HP", "High Priority"
        MEDIUM_PRIORITY = "MP", "Medium Priority"
        LOW_PRIORITY = "LP", "Low Priority"
        ROUTINE = "RT", "Routine"
        OPTIONAL = "OP", "Optional"

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)

    priority = models.CharField(
        max_length=2,
        choices=PriorityOptions.choices,
        default=PriorityOptions.MEDIUM_PRIORITY
    )

    status = models.CharField(
        max_length=2,
        choices=StatusChoices.choices,
        default=StatusChoices.TO_DO,
    )

    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True
    )

    task_tag = TaggableManager(blank=True)

    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="assigned_tasks"
    )

    @property
    def is_completed(self):
        return self.status == self.StatusChoices.DONE

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.priority})"

    def get_absolute_url(self):
        return reverse(
            "manager:task-detail",
            kwargs={"pk": self.pk}
        )
