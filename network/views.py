from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json

# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate

from .models import User, AddPost, Like, Follow


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def add_post(request):
    if request.method == "POST":
        add_post = request.POST["text_post"]
        user = request.user
        post = AddPost(add_post=add_post, username=user)
        post.save()
    return HttpResponseRedirect(reverse("index"))


@csrf_exempt
def all_posts(request):
    posts = AddPost.objects.all()
    posts = posts.order_by("-timestamp").all()

    data = []
    for post in posts:
        likes = Like.objects.filter(post=post)
        data.append({
            "id": post.id,
            "user": post.username.username,
            "content": post.add_post,
            "timestamp": post.timestamp.strftime("%a, %d %b %Y %H:%M:%S"),
            "likes": likes.count()
        })

    return JsonResponse(data, safe=False)


def follow_count(request):
    followers = Follow.objects.filter(follows=request.user.id)
    follower_count = followers.count()

    following = Follow.objects.filter(user=request.user.id)
    following_count = following.count()

    follow = {
        "follower_count": follower_count,
        "following_count": following_count,
    }

    return JsonResponse(follow, safe=False)


def follow_list(request):
    follows = Follow.objects.all()

    follow_list = []
    for follow in follows:
        person = str(follow.list()["user"])
        follower = str(follow.list()["follower"])

        follow_list.append({
            "user": person,
            "follower": follower
        })

    return JsonResponse(follow_list, safe=False)


def user_posts(request):
    user = request.user.id
    posts = AddPost.objects.filter(username=user)
    posts = posts.order_by("-timestamp").all()

    data = []
    for post in posts:
        likes = Like.objects.filter(post=post)
        data.append({
            "id": post.id,
            "user": post.username.username,
            "content": post.add_post,
            "timestamp": post.timestamp.strftime("%a, %d %b %Y %H:%M:%S"),
            "likes": likes.count()
        })

    return JsonResponse(data, safe=False)


def profile(request, username):

    # get user id from 'user'
    user = User.objects.filter(username=username)

    posts = AddPost.objects.filter(username=user[0].id)
    posts = posts.order_by("-timestamp").all()

    followers = Follow.objects.filter(follows=user[0].id)
    follower_count = followers.count()

    following = Follow.objects.filter(user=user[0].id)
    following_count = following.count()

    name = request.user.username

    data = []
    for post in posts:
        likes = Like.objects.filter(post=post)
        data.append({
            "id": post.id,
            "user": post.username.username,
            "content": post.add_post,
            "timestamp": post.timestamp.strftime("%a, %d %b %Y %H:%M:%S"),
            "likes": likes.count()
        })

    all_data = [
        follower_count,
        following_count,
        data,
        username,
        name
    ]

    return JsonResponse(all_data, safe=False)

@csrf_exempt
def follow(request, current_user):
    # check status of following user and set Follow button
    data = json.loads(request.body)
    user_current = request.user
    follow_user = current_user
    user_id = User.objects.get(username=user_current).id
    follower_id = User.objects.get(username=follow_user).id
    pushed_button = (data["pushed_button"])

    try: 
        tmp = Follow.objects.get(user=user_id, follows=follower_id)
        status = "Unfollow"
    except:
        status = "Follow"


    # check if button has been push - follow or unfollow
    if pushed_button:
        if status == "Follow":
            add_following = Follow (
                user=User.objects.get(username=user_current),
                follows=User.objects.get(username=follow_user)
            )
            add_following.save()
        elif status == "Unfollow":
            delete_following = Follow.objects.filter(
                user=User.objects.get(username=user_current),
                follows=User.objects.get(username=follow_user)
                )
            delete_following.delete()

    return JsonResponse(status, safe=False)


def follow_posts(request):

    # get all Following with current user.id
    user_current = request.user
    user_id = User.objects.get(username=user_current).id
    all_following = Follow.objects.filter(user=user_id)
    user_follow_list = []
    for following in all_following:
        user_follow_list.append(following.list())

    # get all posts for each followed user
    followed_user_posts = []
    for user in user_follow_list:
        followed_user_posts.append(User.objects.get(username=user["follower"]).id)
    
    each_user_posts = []
    for postie in followed_user_posts:
        each_user_posts.append(AddPost.objects.filter(username=postie))

    posts = []
    for each_post in each_user_posts:
        posts.append(each_post.order_by("-timestamp").all())


    data = []
    for post in posts:
        for pot in post:
            likes = Like.objects.filter(post=post[0])
            data.append({
                "id": post[0].id,
                "user": post[0].username.username,
                "content": post[0].add_post,
                "timestamp": post[0].timestamp.strftime("%a, %d %b %Y %H:%M:%S"),
                "likes": likes.count()
            })
    
    
    data_sorted = sorted(data, key=lambda x: x['timestamp'], reverse=True)


    return JsonResponse(data_sorted, safe=False)



######### TEST VIEW FOR PAGINATOR #############

def testpaginator(request):
    return render(request, "network/testpaginator.html")


def test_paginate(request):
    ...
