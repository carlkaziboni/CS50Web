from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import loginForm, newPaper, passwordForm, newUserForm
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import User, Papers
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, PapersSerializer
from rest_framework.decorators import api_view
import os
# Create your views here.


def index(request):
    return render(request, "theram/index.html")

def login(request):
    if request.user.is_authenticated:
        return redirect(reverse("index"))
    if request.method == 'GET':
        login_form = loginForm()
        return render(request, "theram/login.html", {"login_form": login_form})
    elif request.method == 'POST':
        incoming_login_form = loginForm(request.POST)
        if incoming_login_form.is_valid():
            login_form_data = incoming_login_form.cleaned_data
            username = login_form_data['username']
            password = login_form_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                user_login(request, user)
                return redirect(reverse("index"))
            else:
                return redirect(reverse("login"))
    else:
        return HttpResponseBadRequest()

@login_required
def logout(request):
    user_logout(request)
    return redirect(reverse("index"))

@login_required
def change_password(request):
    if request.method == 'GET':
        password_form = passwordForm()
        return render(request, "theram/password.html", {"password_form": password_form})
    elif request.method == 'POST':
        incoming_password = passwordForm(request.POST)
        if incoming_password.is_valid():
            user = request.user
            user = User.objects.get(id=user.id)
            incoming_password_clean = incoming_password.cleaned_data
            if incoming_password_clean['password'] == incoming_password_clean['confirm_password']:
                user.set_password(incoming_password_clean['password'])
                user.save()
                user = authenticate(request, username=user.username, password=incoming_password_clean["password"])
                user_login(request, user)
                return redirect(reverse("index"))
            else:
                return redirect(reverse("changepwd"))
        else:
            return redirect(reverse("changepwd"))
    else:
        return HttpResponseBadRequest()
    
@login_required
@staff_member_required
def new_user(request):
    if request.method == "GET":
        user_form = newUserForm()
        return render(request, "theram/newuser.html", {"user_form": user_form})
    elif request.method == "POST":
        user_form = newUserForm(request.POST)
        if user_form.is_valid():
            user_form_cleaned = user_form.cleaned_data
            if user_form_cleaned['admin']:
                try:
                    User.objects.create_superuser(user_form_cleaned['username'], None, user_form_cleaned['username'])
                except:
                    return redirect(reverse("newuser"))
            else:
                try:
                    User.objects.create_user(user_form_cleaned['username'], None, user_form_cleaned['username'])
                except:
                    return redirect(reverse("newuser"))
            return redirect(reverse("accounts"))
        else:
            return redirect(reverse("newuser"))
    else:
        return HttpResponseBadRequest()

@login_required
@staff_member_required
def accounts(request):
    if request.method == "GET":
        return render(request, "theram/accounts.html")
    else:
        return HttpResponseBadRequest()
    
class AccountsView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        try:
            user = User.objects.get(username = request.data['username'])
            user.set_password(user.username)
            user.save()
            return Response({"message": "successfully reset password"})
        except:
            return Response({"message": "failed to reset"})

    def get(self, request):
        serializer = UserSerializer(User.objects.all(), many=True)
        return Response(serializer.data)
    
    def delete(self,request, username):
        try:
            user = User.objects.get(username = username)
            user.delete()
            return Response({"message": "successfully deleted"})
        except:
            return Response({"message": "deletion failed"})

@login_required        
def upload(request):
    if request.method == "GET":
        uplaod_form = newPaper
        return render(request, "theram/upload.html", {"upload_form": uplaod_form})
    elif request.method == "POST":
        form = newPaper(request.POST, request.FILES)
        if form.is_valid():
            instance = Papers(paper=request.FILES['paper'], main=True)
            instance.save()
            papers = Papers.objects.exclude(pk=instance.pk)
            for paper in papers:
                paper.main=False
                paper.save()
            return redirect("index")
        return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()
    
def collection(request):
    if request.method == "GET":
        papers = Papers.objects.all()
        return render(request, 'theram/collection.html',{"papers": papers})
    elif request.method == 'POST':
        if request.user.is_authenticated:
            papers = Papers.objects.exclude(pk=request.POST['main'])
            for paper in papers:
                paper.main = False
                paper.save()
            paper = Papers.objects.get(pk=request.POST['main'])
            paper.main = True
            paper.save()
            return redirect(reverse("collection"))
        else:
            return redirect(reverse("index"))
    else:
        return HttpResponseBadRequest()
    
@api_view(['GET'])
def latest(request):
    if request.method == "GET":
        paper = Papers.objects.get(main=True)
        papers_serialized = PapersSerializer(paper)
        return Response(papers_serialized.data)
    return HttpResponseBadRequest()

@login_required
def delete(request):
    if request.method == "GET":
        papers = Papers.objects.all()
        return render(request, "theram/delete.html", {"papers": papers})
    if request.method == 'POST':
        paper = Papers.objects.get(pk=request.POST['main'])
        os.remove(str(paper.paper))
        paper.delete()
        return redirect(reverse("delete"))