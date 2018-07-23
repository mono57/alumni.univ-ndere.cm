from django.urls import path
from django.contrib.auth.views import PasswordResetConfirmView,  PasswordResetDoneView
from accounts.views import ProfileAccountView ,validate_email

app_name = 'accounts'

urlpatterns = [
    path('', ProfileAccountView.as_view(), name = 'profile'),
    path('validation/', validate_email, name='validate_email'),
]
