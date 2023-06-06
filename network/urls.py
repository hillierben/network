
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_post", views.add_post, name="add_post"),

    # API Routes
    path("posts", views.all_posts, name="all_posts"),
    path("follow_count", views.follow_count, name="follow_count"),
    path("follow_list", views.follow_list, name="follow_list"),
    path("user_posts", views.user_posts, name="user_posts"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow/<str:current_user>", views.follow, name="follow"),
    path("follow_posts", views.follow_posts, name="follow_posts"),
]
