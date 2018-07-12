from django.urls import path
from django.contrib.auth.views import PasswordResetConfirmView,  PasswordResetDoneView
from accounts.views import ProfileAccountView

app_name = 'accounts'

urlpatterns = [
    path('', ProfileAccountView.as_view(), name = 'profile'),
]
