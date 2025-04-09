from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json

from .models import User, Posts
from .forms import NewPost

@login_required
def index(request):
    if request.method == 'POST':
        form = NewPost(request.POST)
        if form.is_valid():
            post_content = form.cleaned_data['post_content']
            post = Posts(post_user = request.user ,post_content = post_content)
            post.save()
    postform = NewPost(auto_id=False)
    allposts = Posts.objects.all().order_by("-post_time")
    paginator = Paginator(allposts, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {"postform": postform, "posts": page_obj})


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

@login_required    
def profile(request, user):
    userprofile = User.objects.get(username=user)
    test = userprofile.followers.all()
    postsall = userprofile.user_posting.all().order_by("-post_time")
    paginator = Paginator(postsall, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {"userprofile": userprofile, "posts": page_obj})

@login_required
@csrf_exempt
def edit(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        id = data['id']
        content = data['content']
        post = Posts.objects.filter(id=id)
        if post[0].post_user != request.user:
            return HttpResponse(status=400)
        post.update(post_content = content)
        id = post[0].id
        content = post[0].post_content
        return JsonResponse({"id": id, "content": content}, status=200)
    return HttpResponse(content="Bad request", status=400)

@login_required
@csrf_exempt
def like(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        post_id = data['id']
        post = Posts.objects.get(id = post_id)
        user = User.objects.get(id = request.user.id)
        post.post_likes.add(user)
        likes = len(post.post_likes.all())
        return JsonResponse({"likes": likes})
    return HttpResponse(status=400)

@login_required
@csrf_exempt
def unlike(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        post_id = data['id']
        post = Posts.objects.get(id = post_id)
        user = User.objects.get(id = request.user.id)
        post.post_likes.remove(user)
        likes = len(post.post_likes.all())
        return JsonResponse({"likes": likes})
    return HttpResponse(status=400)

@login_required
@csrf_exempt
def follow(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        profile_id = data['id']
        profile = User.objects.get(id = profile_id)
        user = User.objects.get(id = request.user.id)
        profile.followers.add(user)
        followers = len(profile.followers.all())
        return JsonResponse({"followers": followers})
    return HttpResponse(status=400)

@login_required
@csrf_exempt
def unfollow(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        profile_id = data['id']
        profile = User.objects.get(id = profile_id)
        user = User.objects.get(id = request.user.id)
        profile.followers.remove(user)
        followers = len(profile.followers.all())
        return JsonResponse({"followers": followers})
    return HttpResponse(status=400)

@login_required
def following(request):
    allposts = Posts.objects.all().order_by("-post_time")
    user = User.objects.get(id = request.user.id)
    followingpost = []
    for post in allposts:
        if (user in post.post_user.followers.all()) and (post.post_user != user):
            followingpost.append(post)
    
    paginator = Paginator(followingpost, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {"posts": page_obj})