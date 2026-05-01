from django.db import models

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField()
    doctor_name = models.CharField(max_length=100)
    doctor_specialty = models.CharField(max_length=100)
    appointment_date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=500.00)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    stripe_session_id = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} → Dr. {self.doctor_name} ({self.status})"
