from django import forms


class searchbar(forms.Form):
    searchbar = forms.CharField(label='Search', max_length=100)

class detail(forms.Form):
    sdate = forms.DateField(label='start date ',input_formats= ['%Y-%m-%d'] ,widget=forms.widgets.DateInput(attrs={'type':'date'}))
    stime = forms.TimeField(label='start time',input_formats= ['%H:%M'] ,widget=forms.widgets.TimeInput(attrs={'type':'time'}))
    edate = forms.DateField(label='end date',input_formats= ['%Y-%m-%d'] ,widget=forms.widgets.DateInput(attrs={'type':'date'}))
    etime = forms.TimeField(label='end time',input_formats= ['%H:%M'] ,widget=forms.widgets.TimeInput(attrs={'type':'time'}))
    # stime = forms.TimeField()
    # etime = forms.TimeField()
    
class desc(forms.Form):
    eventName = forms.CharField()
    eventDetails = forms.CharField(widget=forms.Textarea())
 