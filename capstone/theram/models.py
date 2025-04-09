from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class Papers(models.Model):
    paper = models.FileField(upload_to="papers")
    main = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)