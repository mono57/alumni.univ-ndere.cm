from django.db import models
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()

class Groupe(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    category = models.CharField(max_length=30)
    status = models.CharField(max_length=10)
    avatar = models.ImageField(upload_to='avatar_groups', blank=True)
    #created_by = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    #member = models.ManyToManyField(User)

class Appartenir(models.Model):
    register_at = models.DateTimeField(auto_now=True)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    alumni = models.ForeignKey(User, on_delete=models.CASCADE)

class Subject(models.Model):
    date_add = models.DateTimeField(auto_now=True)
    alumni = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    content = models.TextField()

class Comment(models.Model):
    content = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    alumni = models.ForeignKey(User, on_delete=models.CASCADE)
    date_add = models.DateTimeField(auto_now=True)