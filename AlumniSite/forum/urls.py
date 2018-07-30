from django.urls import path
from forum import views

app_name = 'forum'
urlpatterns = [
    path('community/',views.IndexCommunity.as_view(), name='community'),
    path('community/group/<int:pk>/',views.DetailsViewGroup.as_view(), name='group_details'),
    path('community/group/subject/add',views.addSubject, name='add_subject'),
    path('community/groups/create/',views.CreateGroupeView.as_view(), name='create_group'),
]