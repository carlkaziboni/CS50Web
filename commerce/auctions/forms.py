from django import forms

from .models import Categories

class CreateListingForm(forms.Form):
    name = forms.CharField(max_length=50)
    price = forms.DecimalField(decimal_places=2)
    image = forms.CharField(max_length=50)
    description = forms.CharField(max_length=50, required=False)
    categories = forms.ModelMultipleChoiceField(queryset=Categories.objects.all(), widget=forms.CheckboxSelectMultiple())

class BiddingForm(forms.Form):
    bid = forms.DecimalField(decimal_places=2)
    listing = forms.IntegerField(widget=forms.HiddenInput())

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=100)
    listing = forms.IntegerField(widget=forms.HiddenInput())

class WatchlistForm(forms.Form):
    listing = forms.IntegerField(widget=forms.HiddenInput())

class RemoveWatchlist(forms.Form):
    listingg = forms.IntegerField(widget=forms.HiddenInput())