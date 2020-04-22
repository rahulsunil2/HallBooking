from django import forms

class searchbar(forms.Form):
    searchbar = forms.CharField(label='Search', max_length=100)
class DateForm(forms.Form):
    date = forms.DateField(input_formats=['%d/%m/%Y'])
