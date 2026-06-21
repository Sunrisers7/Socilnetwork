from django import forms

class FriendSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False)