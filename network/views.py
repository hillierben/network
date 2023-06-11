from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator

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


def update_post(request, id, content):
    if request.method == "POST":
        update = AddPost.objects.get(pk=id)
        update.add_post = content
        update.save(update_fields=['add_post'])
    data = "Hello Bob"
    return JsonResponse(data, safe=False)


@csrf_exempt
def all_posts(request, page):
    posts = AddPost.objects.all()
    posts = posts.order_by("-timestamp").all()
    current_user = request.user


    data = []
    for post in posts:
        likes = Like.objects.filter(post=post)
        try:
            tmp = Like.objects.get(user=User.objects.get(username=post.username.username), post=AddPost.objects.get(id=post.id), logged_in_user=User.objects.get(username=request.user))
            like_button = "liked"
        except:
            like_button = "unliked"

        data.append({
            "id": post.id,
            "user": post.username.username,
            "content": post.add_post,
            "timestamp": post.timestamp.strftime("%a, %d %b %Y %H:%M:%S"),
            "likes": likes.count(),
            "currentUser": str(current_user),
            "like_button": like_button
        })

    paginator = Paginator(data, 10)
    # page_number = request.GET.get("page")
    page_obj = paginator.get_page(page)

    return JsonResponse(page_obj.object_list, safe=False)


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


def user_posts(request, page):
    user = request.user.id
    posts = AddPost.objects.filter(username=user)
    posts = posts.order_by("-timestamp").all()
    current_user = request.user

    data = []
    for post in posts:
        likes = Like.objects.filter(post=post)
        data.append({
            "id": post.id,
            "user": post.username.username,
            "content": post.add_post,
            "timestamp": post.timestamp.strftime("%a, %d %b %Y %H:%M:%S"),
            "likes": likes.count(),
            "currentUser": str(current_user)
        })

    paginator = Paginator(data, 10)
    # page_number = request.GET.get("page")
    page_obj = paginator.get_page(page)

    return JsonResponse(page_obj.object_list, safe=False)


def profile(request, username, page):

    # get user id from 'user'
    user = User.objects.filter(username=username)

    posts = AddPost.objects.filter(username=user[0].id)
    posts = posts.order_by("-timestamp").all()

    followers = Follow.objects.filter(follows=user[0].id)
    follower_count = followers.count()

    following = Follow.objects.filter(user=user[0].id)
    following_count = following.count()

    name = request.user.username

    logged_in_user = request.user

    data = []
    for post in posts:
        likes = Like.objects.filter(post=post)
        data.append({
            "id": post.id,
            "user": post.username.username,
            "content": post.add_post,
            "timestamp": post.timestamp.strftime("%a, %d %b %Y %H:%M:%S"),
            "likes": likes.count(),
            "loggedInUser": str(logged_in_user)
        })

    paginator = Paginator(data, 3)
    # page_number = request.GET.get("page")
    page_obj = paginator.get_page(page)


    all_data = [
        follower_count,
        following_count,
        page_obj.object_list,
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


def follow_posts(request, page):

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
            likes = Like.objects.filter(post=pot)
            try:
                tmp = Like.objects.get(user=User.objects.get(username=pot.username.username), post=AddPost.objects.get(id=pot.id), logged_in_user=User.objects.get(username=request.user))
                like_button = "liked"
                print("liked")
            except:
                like_button = "unliked"
                print("unliked")

            data.append({
                "id": pot.id,
                "user": pot.username.username,
                "content": pot.add_post,
                "timestamp": pot.timestamp.strftime("%a, %d %b %Y %H:%M:%S"),
                "likes": likes.count(),
                "like_button": like_button
            })

    paginator = Paginator(data, 10)
    # page_number = request.GET.get("page")
    page_obj = paginator.get_page(page)

    data_sorted = sorted(page_obj.object_list, key=lambda x: x['timestamp'], reverse=True)


    return JsonResponse(data_sorted, safe=False)

@csrf_exempt
def like(request, current_user, post_id):

    user = User.objects.get(username=current_user).id
    id = AddPost.objects.get(pk=post_id).id
    logged_in_user = User.objects.get(username=request.user).id

    try:
        tmp = Like.objects.get(user=user, post=id, logged_in_user=logged_in_user)
        add_like = False
    except:
        add_like = True

    if add_like:
        new_like = Like(
            user=User.objects.get(username=current_user),
            post = AddPost.objects.get(pk=post_id),
            logged_in_user = User.objects.get(username=request.user)
        )
        new_like.save()
    else:
        delete_like = Like.objects.get(user=user, post=id, logged_in_user=logged_in_user)
        delete_like.delete()

    data = "like data"

    return JsonResponse(data, safe=False)



######### TEST VIEW FOR PAGINATOR #############

def testpaginator(request):
    return render(request, "network/testpaginator.html")


def test_paginate(request, page):
    objects = [
        {
            "name": "bob",
            "age": "1"
        },
        {
            "name": "jim",
            "age": "2"
        },
        {
            "name": "greg",
            "age": "3"
        },
        {
            "name": "adam",
            "age": "4"
        },
        {
            "name": "jim",
            "age": "5"
        },
        {
            "name": "pete",
            "age": "6"
        },
        {
            "name": "henbo",
            "age": "7"
        },
        {
            "name": "flib",
            "age": "8"
        },
        {
            "name": "jim",
            "age": "9"
        },
        {
            "name": "unboe",
            "age": "10"
        },
        {
            "name": "shiulim",
            "age": "11"
        },
        {
            "name": "refkejnrv",
            "age": "12"
        },
        {
            "name": "ddkkfl",
            "age": "13"
        },
        {
            "name": "324f9uh",
            "age": "14"
        },
        {
            "name": "digiteihb",
            "age": "15"
        },
        {
            "name": "poplie",
            "age": "16"
        },
        {
            "name": "enbog",
            "age": "17"
        },
        {
            "name": "wert",
            "age": "18"
        },
        {
            "name": "volid",
            "age": "19"
        },
    ]

    paginator = Paginator(objects, 5)
    # page_number = request.GET.get("page")
    page_obj = paginator.get_page(page)

    return JsonResponse(page_obj.object_list, safe=False)
