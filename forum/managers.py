from django.db import models

class AppartenirManager(models.Manager):
    def get_app_by_group(self, group):
        return self.filter(group=group)

    def get_app_by_user(self, user):
        return self.filter(alumni=user)

class SubjectManager(models.Manager):
    def get_subjects_by_group(self, group):
        return self.filter(group=group)

class CommentManager(models.Manager):
    def get_comments_by_subject(self, subject):
        return self.filter(subject = subject)

class RequestManager(models.Manager):
    def get_request_by_group(self, group):
        return  self.filter(group = group)

class GroupeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(activated=True)