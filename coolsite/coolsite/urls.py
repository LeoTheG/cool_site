"""coolsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^$', views.index, name='index'),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    url(r'^(?P<usernameslug>[-\w]+)/profile/$', views.user_profile, name='user_profile'),
    url(r'^(?P<usernameslug>[-\w]+)/profile/new_post/$', views.new_post, name='new_post'),
    url(r'^(?P<usernameslug>[-\w]+)/profile/manage_posts/$', views.manage_posts, name='manage_posts'),
]
