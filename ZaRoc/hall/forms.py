from django import forms
from .models import *

class searchbar(forms.Form):
    searchbar = forms.CharField( max_length=100,label='')
    class Meta:
        model = Hall
        fields =['name']
class DateForm(forms.Form):
    date = forms.DateField(input_formats=['%d/%m/%Y'])
