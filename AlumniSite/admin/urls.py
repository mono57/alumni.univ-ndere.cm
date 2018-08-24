from django.urls import path
from admin import views

app_name = 'admin'

urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),
    path('add/user/',views.AjaxRequestAddUser.as_view(), name='processUser'),
    path('delete/user/',views.ajaxDeleteRequest, name='processDeleteUser'),
    path('suspend/user/',views.ajaxSuspendRequest, name='processSuspendUser'),
    path('active/user/',views.ajaxActiveRequest, name='processActiveUser'),
    path('users/list/',views.ListViewUser.as_view(), name='list_user'),
    path('project/list/',views.ListProject.as_view(), name='list_project'),
    path('group/list/',views.ListGroup.as_view(), name='list_group'),
    path('news/create/',views.CreateNews.as_view(), name='create_news'),
    path('project/create/',views.AddProject.as_view(), name='create_project'),
    path('group/create/',views.AddGroup.as_view(), name='create_group'),
    path('news/update/<int:pk>/',views.UpdateNewsView.as_view(), name='update_news'),
    path('project/<int:pk>/details/',views.DetailsProject.as_view(), name='details_project'),
    path('news/delete/<int:pk>/',views.DeleteNewsView.as_view(), name='delete_news'),
    path('events/delete/<int:pk>/',views.DeleteEventsView.as_view(), name='delete_event'),
    path('events/activation/',views.eventActivation, name='event_activation'),
    path('projects/activation/',views.projectActivation, name='project_activation'),
    path('statistiques/',views.StatsView.as_view(), name='statistiques'),
    path('donate/',views.DonateList.as_view(), name='donate_list'),
    path('donate/confirm/',views.confirmDonate, name='confirm_donate'),
    path('events/list/',views.ListEventsView.as_view(), name='manage_events'),
    path('news/list/',views.ListNews.as_view(), name='list_news'),
]