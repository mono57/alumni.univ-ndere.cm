from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from forum.models import Groupe, Appartenir

User = get_user_model()

