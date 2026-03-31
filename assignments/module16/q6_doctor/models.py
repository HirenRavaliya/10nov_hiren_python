from django.db import models

class Doctor(models.Model):
    SPECIALTY_CHOICES = [
        ('Cardiologist', 'Cardiologist'),
        ('Dermatologist', 'Dermatologist'),
        ('Neurologist', 'Neurologist'),
        ('Orthopedist', 'Orthopedist'),
        ('Pediatrician', 'Pediatrician'),
        ('Psychiatrist', 'Psychiatrist'),
        ('General Physician', 'General Physician'),
        ('ENT Specialist', 'ENT Specialist'),
        ('Ophthalmologist', 'Ophthalmologist'),
        ('Gynecologist', 'Gynecologist'),
    ]
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=50, choices=SPECIALTY_CHOICES)
    hospital = models.CharField(max_length=150)
    city = models.CharField(max_length=80)
    experience_years = models.PositiveIntegerField(default=1)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=500.00)
    is_available = models.BooleanField(default=True)
    latitude = models.FloatField(null=True, blank=True, help_text="For Google Maps")
    longitude = models.FloatField(null=True, blank=True, help_text="For Google Maps")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.name} ({self.specialty})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'