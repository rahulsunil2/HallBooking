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
    # when "hall based search" is pressed
    if 'hall_search' in request.POST:
        hallForm = halldetail(request.POST)
        if hallForm.is_valid():
            
            hall_name = hallForm.cleaned_data['hall_name']
            hall = Hall.objects.get(name = hall_name)
            request.session['hall_id'] = hall.id
            request.session['hall_no'] = hall.no
            return HttpResponseRedirect('/hall')
            
    # when "time based search" is pressed redirect to result page
    elif 'time_search' in request.POST:
        dateForm = detail(request.POST)
        if dateForm.is_valid():
            request.session['sdate'] = str(dateForm.cleaned_data['sdate'])[:-9]
            request.session['edate'] = str(dateForm.cleaned_data['edate'])[:-9]
            return HttpResponseRedirect('/result')

    usrid = request.user.id
    hallBookings = Booking.objects.filter(fId_id = usrid)
    #booking cancellation
    if 'hidden_field' in request.POST:
        bid = hidden(request.POST)
        print(bid)
        if bid.is_valid(): # if the booking_id is valid, delete it
            bookId = bid.cleaned_data['hidden_field']
            print("git bid")
            obj = Booking.objects.filter(bId=bookId)
            obj.delete()
            hallBookings = Booking.objects.filter(fId_id = usrid)

    return render(request, 'home.html', {'date_form':detail(),'hall_form':halldetail(), 'hidden_form':hidden(), "halls":hallBookings})

# request
def result(request):
    sdate = datetime.datetime.strptime(request.session['sdate'], '%Y-%m-%d %H:%M')
    edate = datetime.datetime.strptime(request.session['edate'], '%Y-%m-%d %H:%M')

    # when "search hall" is pressed go to home() -- if(time_search)

    # find & append avail halls
    halls = list(Hall.objects.all())
    avail_halls = []
    for i in halls:
        if Booking.objects.filter(Q(hallNo=i) & ((Q(sTime__lte=sdate) & Q(eTime__gte=sdate)) | (Q(sTime__lte=edate) & Q(eTime__gte=edate)) | (Q(sTime__gte=sdate) & Q(sTime__lte=edate)) | (Q(eTime__gte=sdate) & Q(eTime__lte=edate)))).exists():
            pass
        else:
            avail_halls.append(i)
    #if halls available display
    if len(avail_halls)==0:
        return render(request,'result.html',{'date_form':detail(),'avail':True,'hidden_form':hidden(),"avail_halls":avail_halls})

    #if book is pressed  go to /book 
    if 'hidden_field' in request.POST: #get time n redirect
        oid = hidden(request.POST)
        if oid.is_valid():
            request.session['hall_id'] = oid.cleaned_data['hidden_field']
            return HttpResponseRedirect('/book/')

    return render(request,'result.html',{'date_form':detail(), 'hidden_form':hidden(),"avail_halls":avail_halls,"sdate":sdate,"edate":edate})

# book
def book(request):
    hall = Hall.objects.get(pk=int(request.session['hall_id']))
    sdate = datetime.datetime.strptime(request.session['sdate'], '%Y-%m-%d %H:%M')
    edate = datetime.datetime.strptime(request.session['edate'], '%Y-%m-%d %H:%M')
    userr = User.objects.get(username=request.user) 
    if 'book' in request.POST: #get time and redirect to next page
        eve_desc = desc(request.POST)
        if eve_desc.is_valid():
            book = Booking.objects.create(sTime=sdate,eTime=edate,fId=userr,hallNo=hall,eventName=eve_desc.cleaned_data['title'],eventDetails=eve_desc.cleaned_data['description'],)
            book.save()
            return HttpResponseRedirect('/home/')
    return render(request, 'book.html',{'desc_form':desc(),"hall":hall,"sdate":sdate,"edate":edate})

def hall(request):
    timing_exist = True
    hall = Hall.objects.get(no = int(request.session['hall_no']))
    bookings = Booking.objects.filter(Q(hallNo = hall) & Q(eTime__gte=datetime.datetime.now()))

    # when time based search is done
    if 'hall_time_search' in request.POST:
        dateForm = detail(request.POST)
        if dateForm.is_valid():
            request.session['sdate'] = str(dateForm.cleaned_data['sdate'])[:-9]
            request.session['edate'] = str(dateForm.cleaned_data['edate'])[:-9]
            
            sdate = datetime.datetime.strptime(request.session['sdate'], '%Y-%m-%d %H:%M')
            edate = datetime.datetime.strptime(request.session['edate'], '%Y-%m-%d %H:%M')

            if Booking.objects.filter(Q(hallNo = hall) & ((Q(sTime__lte=sdate) & Q(eTime__gte=sdate)) | (Q(sTime__lte=edate) & Q(eTime__gte=edate)) | (Q(sTime__gte=sdate) & Q(sTime__lte=edate)) | (Q(eTime__gte=sdate) & Q(eTime__lte=edate)))).exists():
                timing_exist = False               
            else:
                return HttpResponseRedirect('/book/')

    return render(request,'hall.html',{'date_form':detail(),'hall':hall,'bookings':bookings, 't_exist':timing_exist})
    