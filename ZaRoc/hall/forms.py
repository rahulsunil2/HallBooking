from django import forms


class searchbar(forms.Form):
    searchbar = forms.CharField(label='Search', max_length=100)

class detail(forms.Form):
    sdate = forms.DateField(input_formats=['%d/%m/%Y'])
    edate = forms.DateField(input_formats=['%d/%m/%Y'])
    stime = forms.TimeField()
    etime = forms.TimeField()
    
class desc(forms.Form):
    eventName = forms.CharField()
    eventDetails = forms.CharField(widget=forms.Textarea())
