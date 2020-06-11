from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import datetime
from .forms import *
from .models import Hall,Booking
from django.contrib.auth.models import User
from django.db.models import Q
# Create your views here.
def signin(request):
    return render(request, 'signin.html') 

def home(request):
    if 'check' in request.POST: #get time and redirect to next page
        dateForm = detail(request.POST)
        if dateForm.is_valid():
            return HttpResponseRedirect('/result/?sdate=%s&edate=%s' %(dateForm.cleaned_data['sdate'],dateForm.cleaned_data['edate']))

    return render(request,'home.html',{'form':detail(),'avail':False,'book':False})

def result(request):
    request.session['sdate']=request.GET.get('sdate')[:-10]
    request.session['edate']=request.GET.get('edate')[:-10]
    sdate = datetime.datetime.strptime(request.GET.get('sdate')[:-10], '%Y-%m-%d %H:%M')
    edate = datetime.datetime.strptime(request.GET.get('edate')[:-10], '%Y-%m-%d %H:%M')
    avail_halls=list(Hall.objects.all())
    for i in avail_halls:
        if Booking.objects.filter(Q(hallNo=i) & ((Q(sTime__lte=sdate) & Q(eTime__gte=sdate)) | (Q(sTime__lte=edate) & Q(eTime__gte=edate)) | (Q(sTime__gte=sdate) & Q(sTime__lte=edate)) | (Q(eTime__gte=sdate) & Q(eTime__lte=edate)))).exists():
            avail_halls.remove(i)
    if len(avail_halls)==0:
        return render(request,'home.html',{'form':detail(),'avail':True})
    # request.session['avail_halls']=avail_halls
    return render(request,'result.html',{"avail_halls":avail_halls})

def book(request):
    return render(request,'home.html',{'form':detail(),'avail':False,'book':True})
