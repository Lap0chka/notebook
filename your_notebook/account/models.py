from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(upload_to='images/users/%Y-%M', blank=True)
    is_verified = models.BooleanField(default=False)
    biography = models.CharField(blank=True, max_length=255)
    about_me = models.TextField(blank=True)
