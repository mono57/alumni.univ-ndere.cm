from django.urls import path
from admin import views

app_name = 'admin'

urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),
    path('add/user/',views.AjaxRequestAddUser.as_view(), name='processUser'),
    path('delete/user/',views.ajaxDeleteRequest, name='processDeleteUser'),
    path('suspend/user/',views.ajaxSuspendRequest, name='processSuspendUser'),
    path('active/user/',views.ajaxActiveRequest, name='processActiveUser'),
    path('list/user/',views.ListViewUser.as_view(), name='list_user'),
    path('news/create/',views.CreateNews.as_view(), name='create_news'),
    path('statistiques/',views.StatsView.as_view(), name='statistiques'),
    path('events/list/',views.ListEventsView.as_view(), name='manage_events'),
]