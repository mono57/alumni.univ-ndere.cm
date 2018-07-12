from django.contrib.auth import get_user_model
from django.core.cache import cache
from AlumniSite import settings
from django.utils import timezone
import datetime

User = get_user_model()

class SetLastUserLogin:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            now = timezone.now()
            request.user.last_login = now
            request.user.save(update_fields=['last_login'])
            cache.set("online", now, settings.EXPIRE_TIME)
            print(cache.get("online"))
            print(request.user.is_online)
        return response