from django.contrib.auth.models import AbstractUser
from django.db import models

class Customer(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, default="Maharashtra")
    pincode = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.username
