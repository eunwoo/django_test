from django.db import models

from user.models import CustomUser


# 공지사항
class AnnouncePost(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField()
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    preSave = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title


# 공지사항 첨부파일
class AnnouncePostFile(models.Model):
    file = models.FileField(upload_to="announcement/files/")
    announce_post = models.ForeignKey(
        AnnouncePost, on_delete=models.CASCADE, related_name="files"
    )
