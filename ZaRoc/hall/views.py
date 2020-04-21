from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import searchbar
from .models import *
# Create your views here.
def signin(request):
    return render(request, 'signin.html')
def home(request):
    #if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = searchbar(request.POST)
        # check whether it's valid:
        if form.is_valid():
            return HttpResponseRedirect('/result/?value=%s' %(form.cleaned_data['searchbar'],))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = searchbar()   
        return render(request, 'home.html',{'form': form})
def result(request):
    value = request.GET.get('value')
    if Hall.objects.filter(name=value).exists():
        return render(request, 'result.html',{'name':value,
        'inCharge':str(Hall.objects.only('inCharge').get(name=value).inCharge), 
        'capacity':str(Hall.objects.only('capacity').get(name=value).capacity), 
        'no':str(Hall.objects.only('no').get(name=value).no)}          
        )
    else:
        return HttpResponse('<p>no such hall</p>')
