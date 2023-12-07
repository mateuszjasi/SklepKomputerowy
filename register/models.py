from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    phone = models.CharField(max_length=9, blank=True)
    street = models.CharField(max_length=150, blank=True)
    zip_code = models.CharField(max_length=5, blank=True)
    city = models.CharField(max_length=150, blank=True)
