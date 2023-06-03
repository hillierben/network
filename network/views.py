from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

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
        print("ADDED POST")
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


def profile(request):
    return render(request, "network/profile.html")


def following(request):
    return render(request, "network/following.html")




