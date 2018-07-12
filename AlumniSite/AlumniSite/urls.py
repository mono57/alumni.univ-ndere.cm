from django.contrib import admin as admin2
from django.urls import path
from django.conf.urls import include
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from AlumniSite import settings
from main.views import IndexView as home_page, ListActualite, ListEvenement, CreateEventView, ContactView,\
    create_event
from accounts.views import *


urlpatterns = [
    path('',home_page.as_view(), name='home' ),
    path('login/', login_page, name='login'),
    path('register/', CreateEtudiant.as_view(), name='register'),
    path('account/', include('accounts.passwords.urls')),
    path('accounts/', include('accounts.urls')),
    path('forum/', include('forum.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('contact-us/', ContactView.as_view(), name='contact'),
    path('list-actualites/', ListActualite.as_view(), name='news'),
    path('list-evenement/', ListEvenement.as_view(), name='event'),
    path('events/create-event/', CreateEventView.as_view(), name='create_event'),
    path('admin/', include('admin.urls')),
    #path('admin/', admin2.site.urls),
    path('admin/auth/', include('admin.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
