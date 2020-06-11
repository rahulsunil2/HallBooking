from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import datetime
from .forms import *
from .models import Hall,Booking
from django.contrib.auth.models import User
import re
from django.db.models import Q
# Create your views here.
def signin(request):
    return render(request, 'signin.html') 

def result(request):
    sdate = datetime.datetime.strptime(request.GET.get('sdate')[:-10], '%Y-%m-%d %H:%M')
    edate = datetime.datetime.strptime(request.GET.get('edate')[:-10], '%Y-%m-%d %H:%M')
    halls=list(Hall.objects.all())
    for i in halls:
        if Booking.objects.filter(Q(hallNo=i) & ((Q(sTime__lte=sdate) & Q(eTime__gte=sdate)) | (Q(sTime__lte=edate) & Q(eTime__gte=edate)) | (Q(sTime__gte=sdate) & Q(sTime__lte=edate)) | (Q(eTime__gte=sdate) & Q(eTime__lte=edate)))).exists():
            halls.remove(i)
    print(halls)
    return render(request,'home.html',{'form':detail()})


def home(request):

    global value,sdate,edate,stime,etime,hall,available

    if 'check' in request.POST: #get time and redirect to next page
        dateForm = detail(request.POST)
        if dateForm.is_valid():
            return HttpResponseRedirect('/result/?sdate=%s&edate=%s' %(dateForm.cleaned_data['sdate'],dateForm.cleaned_data['edate']))

    return render(request,'home.html',{'form':detail()})

   