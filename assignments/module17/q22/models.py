from django.db import models

class DoctorLocation(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    hospital = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    contact_phone = models.CharField(max_length=20, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.name} — {self.hospital}, {self.city}"

    class Meta:
        app_label = 'q22'
