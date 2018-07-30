from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from main.managers import CommentManager, NewsManager, EventsManager

User = get_user_model()

class Evenement(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    lieu = models.CharField(max_length=100)
    image_illustration = models.ImageField(upload_to='event_images', blank=False)
    date_evenement = models.DateField(auto_now=True)
    heure_debut = models.TimeField(auto_now=True)
    heure_fin = models.TimeField(auto_now=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    createur = models.ForeignKey(User,on_delete=models.CASCADE)
    activated = models.BooleanField(default=False)
    
    objects = EventsManager()

    def __str__(self):
        return "{}".format(self.titre)
   

class Actualite(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=40)
    text_description = models.TextField(blank=True)
    image_description = models.ImageField(upload_to='actuality_images')
    date_add = models.DateTimeField(auto_now=True)

    nb_vues = models.IntegerField()
    
    objects = NewsManager()

    def __str__(self):
        return "Titre : {}".format(self.title)
    
    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs
    
    

class Comment(models.Model):
    author = models.CharField(max_length=50)
    email = models.EmailField()
    website = models.URLField(blank=True)
    text = models.TextField()
    add_at = models.DateTimeField(auto_now=True)
    new = models.ForeignKey(Actualite, on_delete=models.CASCADE)

    objects = CommentManager()