from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20, unique=True)
    course = models.CharField(max_length=100)
    marks = models.FloatField(default=0)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.roll_no} - {self.name}"
    class Meta:
        ordering = ['roll_no']