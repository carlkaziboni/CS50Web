from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category

class Listings(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=100, blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=50, blank=True)
    active = models.BooleanField(default=True)
    categories = models.ManyToManyField(Categories)
    userListed = models.ForeignKey(User, on_delete=models.CASCADE)

class Bids(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    userBidding = models.ForeignKey(User, on_delete=models.CASCADE)

class Comments(models.Model):
    comment = models.CharField(max_length=50)
    userCommenting = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)

class Watchlist(models.Model):
    userWatching = models.ForeignKey(User, on_delete=models.CASCADE)
    listingWatched = models.ForeignKey(Listings, on_delete=models.CASCADE)