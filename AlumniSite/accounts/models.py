from django.db import models
from django.contrib.auth.models import (
    AbstractUser, BaseUserManager, Permission
)
from django.utils import timezone
import datetime
from AlumniSite import settings
from django.core.cache import cache

class Ville_residence(models.Model):
    nom = models.CharField(max_length=15)

    def __str__(self):
        return "{}".format(self.nom)


class UserManager(BaseUserManager):
    def create_user(self,email,first_name=None, last_name=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('L\' utilisateur doit avoir une adresse email')
        if not password:
            raise ValueError('L\' utilisateur doit avoir un mot de passe')
        user_object = self.model(
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email),
        )
        user_object.set_password(password)
        user_object.is_active = is_active
        user_object.admin = is_admin
        user_object.staff = is_staff
        user_object.save(using = self._db)

        return user_object
    
    def create_staffuser(self, email,first_name=None, last_name=None, password=None):
        user = self.create_user(
            first_name = first_name,
            last_name = last_name, 
            email = email,
            password = password,
            is_active = True,
            is_staff = True,
            )
        return user

    def create_superuser(self, email,first_name=None, last_name=None, password=None):
        user = self.create_user(
            first_name = first_name,
            last_name = last_name, 
            email = email,
            password = password,
            is_active = True,
            is_staff = True,
            is_admin = True
            )
        return user

class User(AbstractUser):
    username = models.CharField(max_length=30,blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30,blank=True, null=True)
    email = models.EmailField(max_length=255, unique = True)
    is_active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp   = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(default=timezone.now)
    date_joined = models.DateTimeField(default=timezone.now)

    
    is_superuser = True

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name','last_name',]

    objects = UserManager()

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_full_name(self):
        if self.first_name and self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)
        return self.email

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    def cache_online(self):
        return cache.get("online")

    def is_online(self):
        if self.cache_online():
            now = datetime.datetime.now()
            if self.cache_online:
                return True
        return False
        
    


class Faculte(models.Model):
    nom = models.CharField(max_length=30) 
    def __str__(self):
        return "{}".format(self.nom)

class Frequenter(models.Model):
    matricule = models.CharField(max_length=10)
    dernier_diplome = models.CharField(max_length=30)
    annee_entree = models.IntegerField()
    annee_sortie = models.PositiveIntegerField()
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    faculte = models.ForeignKey(Faculte, on_delete=models.CASCADE)  

    def __str__(self):
        return "Alumni : {} Matricule : {} Diplome : {} Faculte : {} ".format(self.user.get_full_name(),
                self.matricule,self.dernier_diplome,
                self.faculte.nom)  


class Entreprise(models.Model):
    nom = models.CharField(max_length=20)
    def __str__(self):
        return "Entreprise : {}".format(self.nom)

class Travailler(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    fonction = models.CharField(max_length=20)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    def __str__(self):
        return "Alumni : {2} Entreprise : {0} Fonction : {1}".format(self.entreprise.nom,self.fonction, self.user.get_full_name())

class Habiter(models.Model):
    ville = models.ForeignKey(Ville_residence, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Etudiant(models.Model):
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=20)
    email = models.EmailField()
    mot_de_passe = models.CharField(max_length=20)
    residence = models.CharField(max_length=20)
    matricule = models.CharField(max_length=10)
    annee_entree = models.IntegerField()
    annee_sortie = models.IntegerField()
    faculte = models.CharField(max_length=50)
    diplome = models.CharField(max_length=30)
    entreprise = models.CharField(max_length=20)
    fonction = models.CharField(max_length=100)

    def get_full_name(self):
        return "{} {}".format(self.nom, self.prenom)