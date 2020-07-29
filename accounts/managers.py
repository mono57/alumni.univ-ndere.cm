from django.db import models

class HabiterManager(models.Manager):
    def get_habiter_by_user(self, user):
        return self.filter(user=user)
class UserProfileManager(models.Manager):
    def get_profile_by_user(self, user):
        return self.get(user=user)