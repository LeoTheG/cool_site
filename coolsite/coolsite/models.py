from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
class Entry(models.Model):
    title = models.CharField(max_length=32)
    body = models.CharField(max_length=1024)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

