from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("self", symmetrical=False)

class Posts(models.Model):
    post_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posting", null=True)
    post_content = models.TextField()
    post_time = models.DateTimeField(auto_now=True)
    post_likes = models.ManyToManyField(User)
