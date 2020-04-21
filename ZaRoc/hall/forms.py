from django import forms

class searchbar(forms.Form):
    searchbar = forms.CharField(label='Search', max_length=100)
