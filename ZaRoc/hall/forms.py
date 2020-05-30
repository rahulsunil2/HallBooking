from django import forms


class searchbar(forms.Form):
    searchbar = forms.CharField(label='Search', max_length=100)

class detail(forms.Form):
    sdate = forms.DateTimeField(label='start date ',input_formats= ['%d/%m/%y %H:%M'] ,widget=forms.widgets.DateTimeInput(attrs={'type':'date'}))
    stime = forms.DateTimeField(label='start time',input_formats= ['%d/%m/%y %H:%M'] ,widget=forms.widgets.DateTimeInput(attrs={'type':'time'}))
    edate = forms.DateTimeField(label='end date and time',input_formats= ['%d/%m/%y %H:%M'] ,widget=forms.widgets.DateTimeInput(attrs={'type':'date'}))
    etime = forms.DateTimeField(label='end time',input_formats= ['%d/%m/%y %H:%M'] ,widget=forms.widgets.DateTimeInput(attrs={'type':'time'}))
    # stime = forms.TimeField()
    # etime = forms.TimeField()
    
class desc(forms.Form):
    eventName = forms.CharField()
    eventDetails = forms.CharField(widget=forms.Textarea())
 