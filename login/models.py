from django.db import models

class Login(models.Model):
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)  # Allow null values
    password = models.CharField(max_length=255, null=True, blank=True)  # Allow blank passwords initially

    def __str__(self):
        return self.email 
