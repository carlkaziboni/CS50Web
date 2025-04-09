
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),

    #API routes
    path("edit", views.edit, name="edit"),
    path("like", views.like, name="like"),
    path("unlike", views.unlike, name="unlike"),
    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),

    #Must go last
    path("profile/<str:user>", views.profile, name="profile")
]
