from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/search", views.search, name = "search"),
    path("wiki/random", views.random, name="random"),
    path("wiki/editpage", views.editpage, name = "editpage"),
    path("wiki/editpage<str:title>", views.editpage, name = "editpage"),
    path("wiki/newpage", views.newpage, name="newpage"),
    path("wiki/<str:title>", views.title, name="title")
]
