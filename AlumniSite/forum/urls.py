from django.urls import path
from forum import views

app_name = 'forum'
urlpatterns = [
    path('community/',views.IndexCommunity.as_view(), name='community'),
    path('community/groups/',views.ListViewGroup.as_view(), name='groupe'),
]