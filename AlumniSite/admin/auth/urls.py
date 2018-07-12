from django.urls import path
from admin.auth.views import LoginAdmin

app_name = 'admin_login'

urlpatterns = [
    path('login/',LoginAdmin.as_view(), name = 'login'),
]