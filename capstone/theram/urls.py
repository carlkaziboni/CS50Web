from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("password", views.change_password, name="changepwd"),
    path("newuser", views.new_user, name="newuser"),
    path("accounts", views.accounts, name="accounts"),
    path("api/accounts", views.AccountsView.as_view()),
    path("api/accounts/<str:username>", views.AccountsView.as_view()),
    path("upload", views.upload, name="upload"),
    path("collection", views.collection, name="collection"),
    path("latest", views.latest, name="latest"),
    path("delete", views.delete, name="delete")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)