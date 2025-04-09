from django.contrib import admin

# Register your models here.
from .models import Listings, Comments, Bids, Categories

admin.site.register([Listings, Comments, Bids, Categories])