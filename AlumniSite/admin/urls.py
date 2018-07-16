from django.urls import path
from admin import views

app_name = 'admin'

urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),
    path('add/user/',views.AjaxRequestProcessUser.as_view(), name='processUser'),
    path('delete/user/',views.ajaxDeleteRequest, name='processDeleteUser'),
    path('suspend/user/',views.ChangeStateUser.as_view(), name='processSuspendUser'),
    path('list/user/',views.ListViewUser.as_view(), name='list_user'),
    path('news/create/',views.CreateNews.as_view(), name='create_news'),
]