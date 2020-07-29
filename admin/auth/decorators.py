from django.core.exceptions import PermissionDenied

def admin_only(func):
    def _admin_only(request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.is_admin:
                raise PermissionDenied
        return func(request, *args, **kwargs)

    return _admin_only