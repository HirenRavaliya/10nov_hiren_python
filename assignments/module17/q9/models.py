from django.db import models

class Doctor(models.Model):
    """Doctor model for the doctor_finder app."""
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    hospital = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=100, blank=True)
    available = models.BooleanField(default=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'q9'
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

    def __str__(self):
        return f"Dr. {self.name} ({self.specialty})"
