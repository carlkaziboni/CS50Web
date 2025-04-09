from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listings, Categories, Bids, Comments, Watchlist
from .forms import CreateListingForm, BiddingForm, CommentForm, WatchlistForm, RemoveWatchlist


def index(request):
    listings = Listings.objects.filter(active=True)
    return render(request, "auctions/index.html", {"listings": listings})

@login_required
def watchlist(request):
    if request.method =='POST':
        listing = Listings.objects.get(pk=request.POST['listing'])
        user = request.user
        watchlist = Watchlist.objects.get(userWatching=user, listingWatched=listing)
        watchlist.delete()
    user = request.user
    watchlists = Watchlist.objects.filter(userWatching=user)
    return render(request, "auctions/watchlist.html",{"watchlists": watchlists})


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = CreateListingForm(request.POST)
        test = form.is_valid()
        if form.is_valid():
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            image = form.cleaned_data['image']
            description = form.cleaned_data['description']
            categories = form.cleaned_data['categories']
            listing = Listings(name=name, price=price, image=image, description=description, userListed=request.user)
            listing.save()
            listing.categories.set(categories)
            return redirect(reverse("viewlisting", kwargs={"id": listing.pk}))
    form = CreateListingForm()
    return render(request, "auctions/createlisting.html", {"form": form})

def view_listing(request, id):
    if request.method == 'POST':
        comment = CommentForm(request.POST)
        watchlist = WatchlistForm(request.POST)
        removewatchlist = RemoveWatchlist(request.POST)
        if comment.is_valid():
            commentt = comment.cleaned_data['comment']
            listing = comment.cleaned_data['listing']
            user = request.POST['user']
            userCommenting = User.objects.get(pk=user)
            listingComment = Listings.objects.get(pk=listing)
            comments = Comments(comment=commentt, listing=listingComment, userCommenting=userCommenting)
            comments.save()
        form = BiddingForm(request.POST)
        if form.is_valid():
            bid = form.cleaned_data['bid']
            if bid <= Listings.objects.get(pk=id).price:
                return render(request, "auctions/error.html")
            listing = form.cleaned_data['listing']
            bids = Bids(bid=bid, listing=Listings.objects.get(pk=listing), userBidding=request.user)
            bids.save()
            Listings.objects.filter(pk=id).update(price=bid)
        elif watchlist.is_valid():
            listing = Listings.objects.get(pk=watchlist.cleaned_data['listing'])
            user=request.user
            watchlistt = Watchlist(userWatching=user ,listingWatched=listing)
            watchlistt.save()
        elif removewatchlist.is_valid():
            listing = Listings.objects.get(pk=removewatchlist.cleaned_data['listingg'])
            user = request.user
            watchlist = Watchlist.objects.get(userWatching=user, listingWatched=listing)
            watchlist.delete()
        else:
            listing = request.POST['listinggg']
            Listings.objects.filter(pk=listing).update(active=False)
        return redirect(reverse("viewlisting", kwargs={"id": id}))
    listing = Listings.objects.get(pk=id)
    user = request.user
    form = BiddingForm(initial={"listing": user.id})
    watchlist = WatchlistForm(initial={"listing": listing.id})
    removewatchList = RemoveWatchlist(initial={"listingg": listing.id})
    watchlistresult = None
    if user.is_authenticated:
        watchlistresult = len(Watchlist.objects.filter(userWatching = user, listingWatched=listing))
    commentform = CommentForm(initial={"listing": listing.id})
    comments = Comments.objects.filter(listing = listing)
    highest = len(Bids.objects.filter(listing=listing))
    if highest != 0:
        highest = Bids.objects.filter(listing=listing).order_by("bid")[::-1][0]
    return render(request, "auctions/listing.html", {"listing": listing, "user": user, "form": form, "commentform": commentform, "comments": comments, "highest": highest,
                  "watchlist": watchlist, "watchlistresult": watchlistresult, "removewatchlist": removewatchList})

def categories(request):
    categoryAll = Categories.objects.all()
    return render(request, "auctions/categorylist.html", {"categoryAll": categoryAll})

def category(request, cat):
    categoryy = Categories.objects.filter(category=cat)
    if len(categoryy) == 0:
        return render(request, "auctions/error.html")
    categoryy = categoryy[0]
    listings = categoryy.listings_set.all()
    return render(request, "auctions/category.html", {"listings": listings, "heading": cat})