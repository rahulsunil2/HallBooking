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
    halls=list(Hall.objects.all())
    avail_halls=[]
    for i in halls:
        if Booking.objects.filter(Q(hallNo=i) & ((Q(sTime__lte=sdate) & Q(eTime__gte=sdate)) | (Q(sTime__lte=edate) & Q(eTime__gte=edate)) | (Q(sTime__gte=sdate) & Q(sTime__lte=edate)) | (Q(eTime__gte=sdate) & Q(eTime__lte=edate)))).exists():
            pass
        else:
            avail_halls.append(i)
    if len(avail_halls)==0:
        return render(request,'home.html',{'form':detail(),'avail':True})
    if 'hidden_field' in request.POST: #get time and redirect to next page
        oid = hidden(request.POST)
        if oid.is_valid():
            request.session['obj_id']=oid.cleaned_data['hidden_field']
            return render(request, 'book.html',{'form':desc()})
    return render(request,'result.html',{'form':hidden(),"avail_halls":avail_halls})

def book(request):
    hall= Hall.objects.get(pk=int(request.session['obj_id']))
    sdate = datetime.datetime.strptime(request.session['sdate'], '%Y-%m-%d %H:%M')
    edate = datetime.datetime.strptime(request.session['edate'], '%Y-%m-%d %H:%M')
    userr = User.objects.get(username=request.user) 
    if 'book' in request.POST: #get time and redirect to next page
        eve_desc = desc(request.POST)
        if eve_desc.is_valid():

            book = Booking.objects.create(sTime=sdate,eTime=edate,fId=userr,hallNo=hall,eventName=eve_desc.cleaned_data['eventName'],eventDetails=eve_desc.cleaned_data['eventDetails'],)
            book.save()
            return render(request,'home.html',{'form':detail(),'avail':False,'book':True})

    return render(request, 'book.html',{'form':desc()})