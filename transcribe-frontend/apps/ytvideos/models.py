# backend/server/apps/notes/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Ytvideo(models.Model):
    url = models.TextField(blank=True)
    title = models.TextField(blank=True)
    length = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)
