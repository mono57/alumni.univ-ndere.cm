from django.contrib import admin as admin2
from django.urls import path
from django.conf.urls import include
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from AlumniSite import settings
from main import views
from accounts.views import *


urlpatterns = [
    path('',views.HomePageView.as_view(), name='home' ),
    path('alumni/',views.IndexView.as_view(), name='index' ),
    path('comment/add/',views.AddComment.as_view(), name='addComment' ),
    path('login/', login_page, name='login'),
    path('register/', CreateEtudiant.as_view(), name='register'),
    path('account/', include('accounts.passwords.urls')),
    path('accounts/', include('accounts.urls')),
    path('forum/', include('forum.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('contact-us/', views.ContactView.as_view(), name='contact'),
    path('news/list/', views.ListActualite.as_view(), name='news'),
    path('news/<int:pk>/details/', views.DetailNews.as_view(), name='details'),
    path('alumni/event/<int:pk>/details/', views.DetailEvent.as_view(), name='details_events'),
    path('alumni/events/list/', views.ListEvenement.as_view(), name='event'),
    path('alumni/events/create/', views.create_event, name='create_event'),
    path('alumni/projects/', views.ProjectsView.as_view(), name='projects'),
    path('admin/', include('admin.urls')),
    #path('admin/', admin2.site.urls),
    path('admin/auth/', include('admin.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
