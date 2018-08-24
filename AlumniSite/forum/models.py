from django.db import models
from django.contrib.auth import get_user_model
from forum.managers import *
import datetime

User = get_user_model()

class Groupe(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    category = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=10)
    avatar = models.ImageField(upload_to='avatar_groups', blank=True)
    #created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    activated = models.BooleanField(default=False)
    #member = models.ManyToManyField(User)
    

    def __str__(self):
        return self.name

    @property
    def subjects(self):
        return Subject.objects.get_subjects_by_group(self)[:10]

    """def get_admin(self):
        instance = self
        member = Appartenir.objects.get_app_by_group(instance)
        admin = member.get(is_admin=True)
        return admin.alumni"""
    def get_members(self):
        appartenir = Appartenir.objects.get_app_by_group(self)
        return [app.alumni for app in appartenir]
    
    def get_admins(self):
        instance = self
        appartenir = Appartenir.objects.get_app_by_group(instance)
        admins = [app.alumni.get_full_name() for app in appartenir if app.admin]
        if admins:
            return admins
        return []

    def get_admin(self):
        return self.get_admins()[0]

    def get_request(self):
        instance = self
        request_ = Request.objects.get_request_by_group(instance)
        return [req.alumni for req in request_]

class Appartenir(models.Model):
    register_at = models.DateTimeField(auto_now=True)
    admin = models.BooleanField(default=False)
    group = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    alumni = models.ForeignKey(User, on_delete=models.CASCADE)
    
    objects = AppartenirManager()

class Subject(models.Model):
    date_add = models.DateTimeField(auto_now=True)
    alumni = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    content = models.TextField()
   

    objects = SubjectManager()
    class Meta:
        ordering = ['-date_add']
    @property
    def get_comments(self):
        return Comment.objects.get_comments_by_subject(self)
        
    def update(self, data):
        self.content = data['content']
        self.save()
        return self

class Comment(models.Model):
    content = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    alumni = models.ForeignKey(User, on_delete=models.CASCADE)
    date_add = models.DateTimeField(auto_now=True)

    objects = CommentManager()

class Request(models.Model):
    group = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    alumni = models.ForeignKey(User, on_delete=models.CASCADE)
    date_request = models.DateTimeField(auto_now=True)

    objects = RequestManager()
