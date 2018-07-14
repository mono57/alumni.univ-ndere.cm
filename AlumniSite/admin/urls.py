from django.urls import path
from admin import views

app_name = 'admin'

urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),
    path('add/user/',views.AjaxRequestProcessUser.as_view(), name='processUser'),
    path('list/user/',views.ListViewUser.as_view(), name='list_user'),
    path('news/create/',views.CreateNews.as_view(), name='create_news'),
]