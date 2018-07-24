"""from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

User = get_user_model()
ADD = 1
CHANGE = 2
DELETE = 3
ACTIVE = 4
SUSPEND = 5
REJET = 6

choices = (
    (ADD, "Ajouter"),
    (CHANGE, "Changer"),
    (DELETE, "Supprimer"),
    (ACTIVE, "Activer"),
    (SUSPEND, "Suspendre"),
    (REJET, "Rejeter"),
    )
class LogEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=10,choices=choices)
    content_type = models.ForeignKey(ContentType, models.SET_NULL, blank=True, null=True)
    object_id = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
# Create your models here.
"""