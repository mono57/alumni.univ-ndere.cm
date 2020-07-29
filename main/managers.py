from django.db import models
from django.db.models import Q
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
        ).filter(search=self.query[0])
    def get_latest_post(self):
        pass

class EventsManager(models.Manager):
    
    def get_uncoming_event(self):
        return self.filter(order='-date_evenement').first()

    def get_queryset(self):
        today = datetime.date.today()
        return super().get_queryset().filter(models.Q(date_evenement__gt=today) | models.Q(date_evenement=today))

    def get_pass_event(self):
        return self.filter(date_evenement<datetime.date.today())

    def get_activated_events(self):
        return self.filter(activated=True)
    
class ContributionManager(models.Manager):
   
    def get_no_confirm(self):
        return super().get_queryset().filter(confirmed=True)
        
    def get_contribution_by_project(self, project):
        return self.filter(Q(project=project)&Q(confirmed=True))