from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Groupe(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=100)
    category = models.CharField(max_length=30)
    openned = models.BooleanField(default=True)
    #created_by = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    member = models.ManyToManyField(User)


