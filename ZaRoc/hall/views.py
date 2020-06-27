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

# home
def home(request):
    h_exist=True
    # when "search hall" in hall name option is pressed
    if 'Hsearch' in request.POST: #get hall id and redirect to next page
        h_form = searchbar(request.POST)
        if h_form.is_valid():
            ihall=h_form.cleaned_data['searchbar']
            if Hall.objects.filter(Q(no=ihall) | Q(name=ihall)).exists():
                request.session['obj_id']=Hall.objects.get(Q(no=ihall) | Q(name=ihall)).id
                return HttpResponseRedirect('/hall' )
            else:
                h_exist=False
    # when "search hall" in time period option is pressed
    elif 'Tsearch' in request.POST: #get time and redirect to next page
        dateForm = detail(request.POST)
        if dateForm.is_valid():
            return HttpResponseRedirect('/result/?sdate=%s&edate=%s' %(dateForm.cleaned_data['sdate'],dateForm.cleaned_data['edate']))
    usrid = request.user.id
    hallBookings = Booking.objects.filter(Q(fId_id = usrid) & Q(eTime__gte=datetime.datetime.now()))
    #hallBookings = Booking.objects.filter(Q(fId_id = usrid))
    if 'hidden_field' in request.POST: #cancel halls
        bid = hidden(request.POST)
        if bid.is_valid():
            bookId = bid.cleaned_data['hidden_field']
            obj = Booking.objects.filter(bId=bookId)
            obj.delete()
            hallBookings = Booking.objects.filter(fId_id = usrid)
            return render(request, 'home.html',{'se_form':detail(),'hidden_form':hidden(), "halls":hallBookings})
    return render(request, 'home.html',{'se_form':detail(),'h_form': searchbar() ,'hidden_form':hidden(), "halls":hallBookings, 'h_exist':h_exist})

def result(request):
    t_exist=True
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
        t_exist=False
    if 'hidden_field' in request.POST: #get time and redirect to next page
        oid = hidden(request.POST)
        if oid.is_valid():
            request.session['obj_id']=oid.cleaned_data['hidden_field']
            return HttpResponseRedirect('/book/')
    return render(request,'result.html',{'se_form':detail(), 'hidden_form':hidden(),"avail_halls":avail_halls,'t_exist':t_exist})


# book
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
            return HttpResponseRedirect('/home/')
    return render(request, 'book.html',{'desc_form':desc(),"hall":hall,"sdate":sdate,"edate":edate})

def hall(request):
    t_exist=True
    h_info=Hall.objects.get(pk=int(request.session['obj_id']))
    b_info=Booking.objects.filter(Q(hallNo=h_info) & Q(eTime__gte=datetime.datetime.now()))
    #b_info=Booking.objects.filter(Q(hallNo=h_info))
    print(b_info)
    if 'Tsearch' in request.POST: #get time and redirect to next page
        dateForm = detail(request.POST)
        if dateForm.is_valid():
            request.session['sdate']=str(dateForm.cleaned_data['sdate'])[:-10]
            request.session['edate']=str(dateForm.cleaned_data['edate'])[:-10]
            sdate = datetime.datetime.strptime(request.session['sdate'], '%Y-%m-%d %H:%M')
            edate = datetime.datetime.strptime(request.session['edate'], '%Y-%m-%d %H:%M')
            if Booking.objects.filter(Q(hallNo=h_info) & ((Q(sTime__lte=sdate) & Q(eTime__gte=sdate)) | (Q(sTime__lte=edate) & Q(eTime__gte=edate)) | (Q(sTime__gte=sdate) & Q(sTime__lte=edate)) | (Q(eTime__gte=sdate) & Q(eTime__lte=edate)))).exists():
                t_exist=False               
            else:
                return HttpResponseRedirect('/book/')
    return render(request,'hall.html',{'se_form': detail(),'hall':h_info,'b_info':b_info,'t_exist':t_exist})
