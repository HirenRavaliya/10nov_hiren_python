from django.db import models

class Registration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} <{self.email}>"
