"""blog1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
from post import views as post_views
from user import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path

    path('post/home/',post_views.home),
	path('post/article/',post_views.article),
	path('post/editor/',post_views.editor),
    path('post/create/', post_views.create),
	path('post/search/',post_views.search),
	path('post/comment/',post_views.comment),
    path('post/delete/',post_views.delete),
    path('post/tag/',post_views.tag),
    # user
    path('user/login/',user_views.login),
    path('user/logout/',user_views.logout),
    path('user/register/',user_views.register),
    path('user/info/',user_views.info),

    # path('post/loghandler/',views.loginhandler),
    # path('post/logout/',views.logout),

    path('post/upfile/',post_views.upfile),
    path('post/savefile/',post_views.savefile),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

