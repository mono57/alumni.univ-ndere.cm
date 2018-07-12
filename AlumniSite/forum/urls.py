from django.urls import path
from forum.views import IndexCommunity

app_name = 'forum'
urlpatterns = [
    path('community',IndexCommunity.as_view(), name='community'),
]