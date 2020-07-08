from django import forms
from .models import Hall
# from hall.middleware import get_current_session

class searchbar(forms.Form):
    searchbar = forms.CharField(label='Search', max_length=100)

class detail(forms.Form):
    date = forms.DateTimeField(label='date       :',input_formats=['%d/%m/%Y'],)
    etime = forms.DateTimeField(label='end time   :',input_formats=['%I:%M %p'],)
    stime = forms.DateTimeField(label='end time   :',input_formats=['%I:%M %p'],)

class halldetail(forms.Form):
    hall_name = forms.ModelChoiceField(queryset=Hall.objects.all(),empty_label="Choose Halls")
    
class hidden(forms.Form):
    hidden_field = forms.CharField(widget=forms.HiddenInput())

class desc(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description',widget=forms.Textarea)