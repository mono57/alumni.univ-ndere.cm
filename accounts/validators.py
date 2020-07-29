from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError('This email is already taken', params={'value':value})