from django import forms


class searchbar(forms.Form):
    searchbar = forms.CharField(label='Search', max_length=100)

class detail(forms.Form):
    sdate = forms.DateTimeField(label='start date :',input_formats=['%d/%m/%Y %H:%M'])
    # stime = forms.TimeField(label='start time',input_formats= ['%H:%M'] ,widget=forms.widgets.TimeInput(attrs={'type':'time'}))
    edate = forms.DateTimeField(label='end date   :',input_formats=['%d/%m/%Y %H:%M'])
    # etime = forms.TimeField(label='end time',input_formats= ['%H:%M'] ,widget=forms.widgets.TimeInput(attrs={'type':'time'}))
    # stime = forms.TimeField()
    # etime = forms.TimeField()
    
class desc(forms.Form):
    eventName = forms.CharField(label='name', max_length=100)
    eventDetails = forms.CharField(label='details',widget=forms.Textarea)
 