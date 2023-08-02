from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


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
