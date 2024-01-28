# post/models.py

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    owner = models.ForeignKey(
        "auth.User", related_name="post", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=50)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(
        "auth.User", related_name="like", on_delete=models.CASCADE
    )
    liked_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.liked_by} liked '{self.post}'"
