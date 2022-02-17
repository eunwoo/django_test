from django.db import models
from django.contrib.auth.models import AbstractUser


# Create model for user registration
class CustomUser(AbstractUser):
    name = models.CharField(max_length=30)
    class1 = models.CharField(max_length=60)
    class2 = models.CharField(max_length=60)
    class3 = models.CharField(max_length=60)
    company = models.CharField(max_length=60)
    phone = models.CharField(max_length=20)
    signImage = models.ImageField(upload_to="signature/", blank=True)
    is_system_manager = models.BooleanField(default=False)
    register = models.BooleanField(default=False)
    first_name = None
    last_name = None
