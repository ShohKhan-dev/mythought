"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views

from mythought.forms import UserLoginForm

from mythought.views import frontpage, signup, feed, search, userprofile, follow_user, unfollow_user, followers, follows, edit_profile, conversations, conversation, notifications
from mythought.api import api_add_post, api_add_like, api_add_message

from django.views.static import serve
from django.conf.urls import url

urlpatterns = [

    path('', frontpage, name='frontpage'),
    path('signup/', signup, name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('login/', views.LoginView.as_view(template_name='login.html'), name='login'),

    path('login/', views.LoginView.as_view( template_name="login.html", authentication_form=UserLoginForm), name='login'),


    path('feed/', feed, name='feed'),
    path('search/', search, name='search'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('notifications/', notifications, name='notifications'),
    path('conversations/', conversations, name='conversations'),
    path('conversations/<int:user_id>/', conversation, name='conversation'),

    path('u/<str:username>/', userprofile, name='userprofile'),

    path('u/<str:username>/follow/', follow_user, name='follow_user'),

    path('u/<str:username>/unfollow/', unfollow_user, name='unfollow_user'),

    path('u/<str:username>/followers/', followers, name='followers'),
    path('u/<str:username>/follows/', follows, name='follows'),

    path('api/add_post/', api_add_post, name='api_add_post'),

    path('api/add_like/', api_add_like, name='api_add_like'),

    path('api/add_message/', api_add_message, name='api_add_message'),

    # ADMIN
    path('admin/', admin.site.urls),

    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

