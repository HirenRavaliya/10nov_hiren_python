from django.db import models
from courses.models import Course


class Student(models.Model):
    """A student who can be enrolled in multiple courses."""

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    enrollment_date = models.DateField(auto_now_add=True)
    courses = models.ManyToManyField(
        Course,
        related_name='students',
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
