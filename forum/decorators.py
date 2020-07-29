from forum.models import Appartenir
from django.core.exceptions import PermissionDenied

def can_access(func):
    def _can_access(request, *args, **kwargs):
        user = request.user.id
        
        try:
            app = Appartenir.objects.get(alumni=user)
        except:
            app = None
            print(app)
        if app is None:
            raise PermissionDenied
        return func(request, *args, *kwargs)
    return _can_access