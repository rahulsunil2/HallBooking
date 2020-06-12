from django import forms


class searchbar(forms.Form):
    searchbar = forms.CharField(label='Search', max_length=100)

class detail(forms.Form):
    sdate = forms.DateTimeField(label='start date :',input_formats=['%d/%m/%Y %H:%M'])
    edate = forms.DateTimeField(label='end date   :',input_formats=['%d/%m/%Y %H:%M'])

class hidden(forms.Form):
    hidden_field = forms.CharField(widget=forms.HiddenInput()) 
      
class desc(forms.Form):
    eventName = forms.CharField(label='name', max_length=100)
    eventDetails = forms.CharField(label='details',widget=forms.Textarea)
 