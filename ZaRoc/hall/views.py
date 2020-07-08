from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
import datetime
from .forms import *
from .models import Hall,Booking,Staff
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Q

# csv 
import csv

# mail
from django.contrib.sites.models import Site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from .tokens import *

def signin(request):
    return render(request,'signin.html') 

# home
def home(request):
    # email check
    try:
        x = Staff.objects.get(email = request.user.email)
    except:
        #flush session & redirect
        request.session.flush()
        logout(request)
        messages.info(request, "Use Correct Email-id")
        return redirect('account_logout')
    
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
            request.session['sdate'] = str(dateForm.cleaned_data['date'])[:11]+str(dateForm.cleaned_data['stime'])[11:-9]
            request.session['edate'] = str(dateForm.cleaned_data['date'])[:11]+str(dateForm.cleaned_data['etime'])[11:-9]
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

def csvdown(request):
    usrid = request.user.id
    hallBookings = Booking.objects.filter(fId_id = usrid)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Bookings.csv"'

    writer = csv.writer(response)
    writer.writerow(['Hall No', 'Booking Id', 'Event name', 'Event Details','From','To'])
    for hall in hallBookings:
        writer.writerow([hall.hallNo, hall.bId, hall.eventName, hall.eventDetails, hall.sTime, hall.eTime, ])
    return response

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

def hall(request):
    timing_exist = True
    hall = Hall.objects.get(no = int(request.session['hall_no']))
    bookings = Booking.objects.filter(Q(hallNo = hall) & Q(eTime__gte=datetime.datetime.now()))

    # when time based search is done
    if 'hall_time_search' in request.POST:
        dateForm = detail(request.POST)
        if dateForm.is_valid():
            request.session['sdate'] = str(dateForm.cleaned_data['date'])[:11]+str(dateForm.cleaned_data['stime'])[11:-9]
            request.session['edate'] = str(dateForm.cleaned_data['date'])[:11]+str(dateForm.cleaned_data['etime'])[11:-9]
            
            sdate = datetime.datetime.strptime(request.session['sdate'], '%Y-%m-%d %H:%M')
            edate = datetime.datetime.strptime(request.session['edate'], '%Y-%m-%d %H:%M')

            if Booking.objects.filter(Q(hallNo = hall) & ((Q(sTime__lte=sdate) & Q(eTime__gte=sdate)) | (Q(sTime__lte=edate) & Q(eTime__gte=edate)) | (Q(sTime__gte=sdate) & Q(sTime__lte=edate)) | (Q(eTime__gte=sdate) & Q(eTime__lte=edate)))).exists():
                timing_exist = False               
            else:
                return HttpResponseRedirect('/book/')

    return render(request,'hall.html',{'date_form':detail(),'hall':hall,'bookings':bookings, 't_exist':timing_exist})

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

            # for sending mail
            user = request.user
            current_site = Site.objects.get_current()
            body = render_to_string('ver_email.html', {
            'user':user, 'domain':current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': verification_token.make_token(user),
            'bid':urlsafe_base64_encode(force_bytes(book.bId)),
            })
            print(body) 
            subject = "Verify Hall booking"
            to_mail = "bookings.mbcet@gmail.com"
            mail = EmailMessage(subject,body,to=[to_mail])
            mail.send()

            return HttpResponseRedirect('/home/')
    return render(request, 'book.html',{'desc_form':desc(),"hall":hall,"sdate":sdate,"edate":edate})
    
def confirm(request,uid,token,bid):
    try:
        booking_info = Booking.objects.get(bId = force_text(urlsafe_base64_decode(bid)))
    except:
        print("---- An exception occurred ------------------")
        return HttpResponse("Already Rejected")
    if(booking_info.status == 'confirmed' ):
        return HttpResponse("Already Confirmed")
    hall = Hall.objects.get(name = booking_info.hallNo)
    return render(request,'confirm_booking.html',{'uid':uid,'token':token,'bid':bid,'stat':'rejected','booking':booking_info, 'hall':hall})


def verified(request,uid,token,bid,stat):
    try:
        user_id = force_text(urlsafe_base64_decode(uid))
        user = User.objects.get(id = user_id)
        book_id = force_text(urlsafe_base64_decode(bid))
        print(book_id)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and verification_token.check_token(user,token):
        user.is_active = False
        if Booking.objects.filter(Q(bId = book_id) & Q(fId = user)).exists():
            x = Booking.objects.get(bId = book_id)
            x.status = stat
            x.save()
            if stat == 'confirmed':
                email = user.email
                sub = "Booking Confirmed"
                msg = "Confirmed " + x.eventName
                mail = EmailMessage(sub,msg,to=[email])
                mail.send()
                return HttpResponse("booking confirmed")
            else:
                x.delete()
                email = user.email
                sub = "Booking Rejected"
                msg = "Rejected " + x.eventName
                mail = EmailMessage(sub,msg,to=[email])
                mail.send()
                return HttpResponse("booking rejected")
    else:
        return HttpResponse("bookings not confirmed ")