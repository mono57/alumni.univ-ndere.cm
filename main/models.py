from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from main.managers import CommentManager, NewsManager, EventsManager, ContributionManager
import datetime

User = get_user_model()

class Evenement(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    lieu = models.CharField(max_length=100)
    image_illustration = models.ImageField(upload_to='event_images', blank=False)
    date_evenement = models.DateField(blank=False)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    date_creation = models.DateTimeField(auto_now=True)
    createur = models.ForeignKey(User,on_delete=models.CASCADE)
    activated = models.BooleanField(default=False)
    
    objects = EventsManager()
    
    class Meta:
        ordering = ('date_evenement',)
    def __str__(self):
        return "{}".format(self.titre)

    def get_related_events(self):

        query = [q for q in self.titre.split() if len(q) >= 4 ]

        return self.annotate(
            search=SearchVector('titre', 'description'),
        ).filter(search=query[0])

    def get_next_events_time(self):
        return self.date_evenement - datetime.date.today()


    def registration(self):
        inscriptions = Inscription.objects.filter(event=self)
        if inscriptions.exists():
            return [inscription.alumni for inscription in inscriptions]
        return []

    def update_event(self,data):
        self.titre = data['titre']
        self.description = data['description']
        self.image_illustration = data['image_illustration']
        self.lieu = data['lieu']
        self.date_evenement = data['date_evenement']
        self.heure_debut = data['heure_debut']
        self.heure_fin = data['heure_fin']

        self.save()
        print(self)
        return self

class Actualite(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=40)
    text_description = models.TextField(blank=True)
    image_description = models.ImageField(upload_to='actuality_images')
    date_add = models.DateTimeField(auto_now=True)

    nb_vues = models.IntegerField(blank=True)
    
    objects = NewsManager()

    class Meta:
        ordering = ['-date_add']

    def __str__(self):
        return "Titre : {}".format(self.title)
    
    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs 

class Inscription(models.Model):
    date = models.DateTimeField(auto_now=True)
    alumni = models.ForeignKey(User, on_delete=models.CASCADE, default=5)
    event = models.ForeignKey(Evenement, on_delete=models.CASCADE)


class Comment(models.Model):
    author = models.CharField(max_length=50)
    email = models.EmailField()
    website = models.URLField(blank=True)
    text = models.TextField()
    add_at = models.DateTimeField(auto_now=True)
    new = models.ForeignKey(Actualite, on_delete=models.CASCADE)

    objects = CommentManager()


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField(null=True,blank=True)
    time = models.IntegerField(null=True,blank=True)
    execute = models.CharField(max_length=30, blank=True)
    montant = models.IntegerField(null=True,blank=True)
    date_add = models.DateTimeField(auto_now=True)
    activated = models.BooleanField(default=False)
    add_by = models.ForeignKey(User, on_delete=models.CASCADE, default=6)

    def __str__(self):
        return self.name

    def contributions(self):
        instance = self
        return Contribution.objects.get_contribution_by_project(instance)

class Contribution(models.Model):
    alumni = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    montant = models.IntegerField()
    mode_payement = models.CharField(max_length=50, blank=True)
    confirmed = models.BooleanField(default=False)
    donate_date = models.DateTimeField(auto_now=True, blank=True)

    objects = ContributionManager()