from django.urls import path
from django.contrib.auth.views import PasswordResetConfirmView,  PasswordResetDoneView
from accounts.views import ProfileAccountView ,validate_email, RegistrationSend, RegistrationConditions

app_name = 'accounts'

urlpatterns = [
    path('<int:pk>/', ProfileAccountView.as_view(), name = 'profile'),
    path('validation/', validate_email, name='validate_email'),
    path('registration/send/', RegistrationSend.as_view(), name='registration_send'),
    path('registration/conditions/', RegistrationConditions.as_view(), name='registration_conditions'),
]
