from django.urls import path
from admin.auth.views import login

app_name = 'admin_login'

urlpatterns = [
    path('login/',login, name = 'login'),
]