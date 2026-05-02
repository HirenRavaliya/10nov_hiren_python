from django.db import models


class Course(models.Model):
    """A course that students can enrol in."""

    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    credits = models.PositiveSmallIntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.code} – {self.name}"
