from django.db import models
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    hospital = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=100, blank=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        app_label = 'q6'
    def __str__(self):
        return f"Dr. {self.name}"
