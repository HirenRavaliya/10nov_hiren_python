import random
from django.db import models

class OTPRecord(models.Model):
    phone = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone} — {'Verified' if self.verified else 'Pending'}"
