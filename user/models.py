from django.db import models
from django.contrib.auth.models import AbstractUser


# Create model for user registration
class CustomUser(AbstractUser):
    name = models.CharField(max_length=30)
    class1 = models.CharField(max_length=60)
    class2_choices = (
        ("일반 사용자", "일반 사용자"),
        ("현장 대리인", "현장 대리인"),
        ("일반 건설사업관리기술인", "일반 건설사업관리기술인"),
        ("총괄 건설사업관리기술인", "총괄 건설사업관리기술인"),
    )
    class2 = models.CharField(max_length=60, choices=class2_choices)
    class3 = models.CharField(max_length=60)
    company = models.CharField(max_length=60)
    phone = models.CharField(max_length=20)
    signImage = models.ImageField(upload_to="signature/", blank=True)
    is_system_manager = models.BooleanField(default=False)
    register = models.BooleanField(default=False)
    first_name = None
    last_name = None


class ChangePwd(models.Model):
    code = models.CharField(max_length=6)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    expired_time = models.DateTimeField(auto_now_add=True)
    isSuccess = models.BooleanField(default=False)
