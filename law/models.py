from django.db import models
from user.models import CustomUser


class LawPost(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField()
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title


class LawPostFile(models.Model):
    file = models.FileField(upload_to="law/files/")
    Law_post = models.ForeignKey(
        LawPost, on_delete=models.CASCADE, related_name="files"
    )
