from django import forms


class searchbar(forms.Form):
    searchbar = forms.CharField(label='Search', max_length=100)

class detail(forms.Form):
    sdate = forms.DateField(widget=forms.SelectDateWidget)
    edate = forms.DateField(widget=forms.SelectDateWidget)
    stime = forms.TimeField()
    etime = forms.TimeField()
    
class desc(forms.Form):
    eventName = forms.CharField()
    eventDetails = forms.CharField(widget=forms.Textarea())
