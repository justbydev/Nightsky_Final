"""NightSky URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
import main.views
from accounts import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main.views.home, name="home"),
    path('main/', main.views.main, name="main"),
    path('accounts/', user_views.register, name="register"),
    path('accounts/login/', user_views.login, name="login"),
    path('accoutns/logout/', user_views.logout, name="logout"),
    path('mysky/', main.views.mysky, name="mysky"), 
    path('realmain/', main.views.realmain, name="realmain"),
    path('mysky/user_update/', main.views.user_update, name="user_update"),
    path('mysky/user_update/changeid/', main.views.change_ID, name="change_ID"),
    path('mysky/user_update/changeemail/', main.views.change_Email, name="change_Email"),
    path('mysky/user_update/changepw/', main.views.change_pw, name="change_pw"),
    path('mysearch/', main.views.mysearch, name="mysearch"),
    path('mysearch/postdetail/', main.views.postdetail, name="postdetail"),
    path('mysearch/post_total/', main.views.post_total, name="post_total"),
    path('mysky/postdetail/', main.views.postdetail, name="postdetail"), 
    path('mysky/post_edit/', main.views.post_edit, name="post_edit"),
    path('mysky/post_delete/', main.views.post_delete, name="post_delete"),
    path('realmain/post_total/', main.views.post_total, name="post_total"),
    path('realmain/postdetail/', main.views.postdetail, name="postdetail"),
    path('othersky/<int:index>/', main.views.othersky, name="othersky"),
    path('otherdetail/', main.views.otherdetail, name="otherdetail"),
    path('postdetail/', main.views.postdetail, name="postdetail"),
    path('commentothersky/<str:index>/', main.views.commentothersky, name="commentothersky"),
    path('mysky/user_update/postdetail/', main.views.postdetail, name="postdetail"), 
    path('mysky/user_update/post_edit/', main.views.post_edit, name="post_edit"),
    path('mysky/user_update/post_delete/', main.views.post_delete, name="post_delete"),
    path('mysky/comment_update/', main.views.comment_update, name="comment_update"),
    path('mysky/comment_delete/', main.views.comment_delete, name="comment_delete"),
]