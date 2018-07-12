from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Evenement(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    lieu = models.CharField(max_length=100)
    image_illustration = models.ImageField(upload_to='event_images')
    date_evenement = models.DateTimeField(auto_now=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    createur = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return "Evenement : {} Date : {} Createur : {}".format(self.titre,self.date_evenement, self.createur)

class Actualite(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=40)
    text_description = models.TextField(blank=True)
    image_description = models.ImageField(upload_to='actuality_images')
    date_add = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "Titre : {}".format(self.title)