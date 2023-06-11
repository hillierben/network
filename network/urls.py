
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_post", views.add_post, name="add_post"),

    # API Routes
    path("posts/<int:page>", views.all_posts, name="all_posts"),
    path("follow_count", views.follow_count, name="follow_count"),
    path("follow_list", views.follow_list, name="follow_list"),
    path("user_posts/<int:page>", views.user_posts, name="user_posts"),
    path("profile/<str:username>/<int:page>", views.profile, name="profile"),
    path("follow/<str:current_user>", views.follow, name="follow"),
    path("follow_posts/<int:page>", views.follow_posts, name="follow_posts"),
    path("update_post/<int:id>/<str:content>", views.update_post, name="update_post"),
    path("like/<str:current_user>/<int:post_id>", views.like, name="like"),

    #TEST PAGE
    path("testpaginator", views.testpaginator, name="testpaginator"),
    #TEST API
    path("test_paginate/<int:page>", views.test_paginate, name="test_paginate"),
]
