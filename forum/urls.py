from django.urls import path
from forum import views

app_name = 'forum'
urlpatterns = [
    path('',views.IndexCommunity.as_view(), name='community'),
    path('group/list/',views.ListGroupCommunity.as_view(), name='list_group'),
    path('group/request/',views.ListRequest.as_view(), name='list_request'),
    path('group/<int:pk>/',views.DetailsViewGroup.as_view(), name='group_details'),
    path('group/<int:pk>/quit/',views.quitGroup, name='quit_group'),
    path('group/subject/<int:pk>/',views.DetailsViewSubject.as_view(), name='subject_details'),
    path('group/subject/add',views.addSubject, name='add_subject'),
    path('group/subject/delete',views.deleteSubject, name='delete_subject'),
    path('group/comment/add',views.appendComments, name='add_comment'),
    path('group/create/',views.CreateGroupeView.as_view(), name='create_group'),
    path('group/request',views.addRequest, name='request_group'),
    path('group/request/<int:pk>/accept/',views.acceptRequest, name='accept_request'),
    path('group/request/<int:pk>/decline/',views.declineRequest, name='decline_request'),
    path('group/manage/',views.ManageGroup.as_view(), name='manage_group'),
    path('group/manage/delete',views.deleteEvent, name='delete_event'),
    path('group/<int:pk>/delete/',views.DeleteGroup.as_view(), name='delete_group'),
    
]