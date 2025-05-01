from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Signup(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, unique=True) 
    password = models.CharField(max_length=128)  # Password should be hashed

    def set_password(self, raw_password):
        """Hashes the password before saving."""
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

   


    def __str__(self):
        return self.email