from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    host = models.CharField(max_length=20)
    text = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

