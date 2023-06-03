
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_post", views.add_post, name="add_post"),
    path("profile", views.profile, name="profile"),
    path("following", views.following, name="following"),

    # API Routes
    path("posts", views.all_posts, name="all_posts"),
]
