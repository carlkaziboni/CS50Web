from django import forms

class NewPost(forms.Form):
    post_content = forms.CharField(widget=forms.Textarea, label="")