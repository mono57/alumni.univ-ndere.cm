from django.db import models

class CommentManager(models.Manager):
    def filter_by_instance(self,instance):
        return self.filter(new=instance)
        