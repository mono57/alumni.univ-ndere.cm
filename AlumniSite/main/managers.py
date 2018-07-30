from django.db import models
from django.contrib.postgres.search import SearchVector
import datetime

class CommentManager(models.Manager):
    def filter_by_instance(self,instance):
        return self.filter(new=instance)
        

class NewsManager(models.Manager):
    query = None
    def get_related_posts(self):

        self.query = [q for q in self.title.split() if len(q) >= 4 ]

        return self.annotate(
            search=SearchVector('title', 'text_description'),
        ).filter(search=self.query)

class EventsManager(models.Manager):
    def get_uncoming_event(self):
        return self.first()
    
