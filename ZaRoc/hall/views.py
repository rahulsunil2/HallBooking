from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import datetime
from .forms import *
from .models import Hall,Booking
from django.contrib.auth.models import User
# Create your views here.
def signin(request):
    return render(request, 'signin.html') 

def result(request):
    #form = searchbar()   
    date = datetime.datetime.strptime(request.GET.get('initDate'),"%Y-%m-%d").date()
    
    obid = Booking.objects.all() #getting objectid
    hob = Hall.objects.all() #getting hall objects
    n=0
    halldict = {}
    obj=[]
    while n < len(hob):
        x = 0
        a = []
        while x < len(obid):
            if obid[x].hallNo.name ==  hob[n].name and date == obid[x].sdate :
                a.append(obid[x].stime)
                a.append(obid[x].etime)

            x+=1

        if len(a)>0:
            a.sort()
            halldict[n] = {}
            halldict[n]['name'] = hob[n].name
            halldict[n]['0'] = ['00:00:00',a[0].strftime("%H:%M:%S")]
            halldict[n]['1'] = [a[len(a)-1].strftime("%H:%M:%S"),'00:00:00']
            m=1
            p=2
            while m < len(a)-1:
                if (datetime.datetime.combine(date, a[m+1])-datetime.datetime.combine(date, a[m])) != 0:
                    halldict[n][p] = [a[m].strftime("%H:%M:%S"),a[m+1].strftime("%H:%M:%S")]
                    p+=1
                    m+=2
                else:
                    m+=2
                    p+=1
        else:
            halldict[n] = {}
            halldict[n]['name'] = hob[n].name
            halldict[n]['0'] = ['00:00:00','00:00:00']
        n+=1
    print(halldict)
    return render(request, 'result.html',{'halls':halldict})

    # #if this is a POST request we need to process the form data
    # if request.method == 'POST':
    #     # create a form instance and populate it with data from the request:
    #     form = searchbar(request.POST)
    #     # check whether it's valid:
    #     if form.is_valid():
    #         return HttpResponseRedirect('/result/?value=%s' %(form.cleaned_data['searchbar'],))
    # # if a GET (or any other method) we'll create a blank form
    # else: 


def home(request):

    global value,sdate,edate,stime,etime,hall,available

    if 'check' in request.POST: #get time and redirect to next page
        dateForm = detail(request.POST)
        print(dateForm['sdate'].value())
        print(dateForm.errors)
        if dateForm.is_valid():
            Sdate = dateForm['sdate'].value()
            Stime = dateForm['stime'].value()
            Edate = dateForm['edate'].value()
            Etime = dateForm['etime'].value()
            c="\n{} \n{} \n{} \n{}\n"
            print(c.format(Sdate,Stime,Edate,Etime))
            print("hey")
            return HttpResponseRedirect('/result/?initDate=%s' %(dateForm.cleaned_data['sdate'],))

    return render(request,'home.html',{'form':detail()})

    # if 'check' in request.POST: #forms for time
    #     hall = Hall.objects.get(name=value)
    #     frm2 = desc()
    #     frm = detail(request.POST)
    #     if frm.is_valid():
    #         sdate = frm.cleaned_data.get('sdate')
    #         edate = frm.cleaned_data.get('edate')
    #         stime = frm.cleaned_data.get('stime')
    #         etime = frm.cleaned_data.get('etime')
    #         if Booking.objects.filter(hallNo=hall):
    #             obid = Booking.objects.filter(hallNo=hall) #getting objectid
    #             n=0
    #             while n<len(obid):
    #                 if sdate==obid[n].sdate: 
    #                     if stime == obid[n].stime: #same time
    #                         return HttpResponse("booking not possible")
    #                         break
    #                     elif etime > obid[n].stime: #end time is greater than start time of another event
    #                         return HttpResponse("booking not possible")
    #                         break
    #                     elif stime > obid[n].stime and stime < obid[n].etime: #new booking starts b/w a ongoing event
    #                         return HttpResponse("booking not possible")
    #                         break
    #                 n+=1
    #         return render(request, 'result.html',{'name':value,
    #         'inCharge':str(Hall.objects.only('inCharge').get(name=value).inCharge), 
    #         'capacity':str(Hall.objects.only('capacity').get(name=value).capacity), 
    #         'no':str(Hall.objects.only('no').get(name=value).no),'form':frm2,'ch':True}) 
             
    # elif 'book' in request.POST: #forms for event
    #     c= request.user
    #     n=c.username
    #     i=c.id 
    #     form = desc(request.POST)   
    #     if form.is_valid():
    #         ename = form.cleaned_data.get('eventName')
    #         edes = form.cleaned_data.get('eventDetails')
    #         booking = Booking.objects.create(sdate=sdate,edate=edate,stime=stime,
    #         etime=etime,hallNo=hall,fId=c,eventName=ename,eventDetails=edes)
    #         booking.save();
    #         return redirect('home')

    # value = request.GET.get('value')
    # hall = Hall.objects.get(name=value)
    # frm1 = detail()

    # if Hall.objects.filter(name=value).exists():
    #     return render(request, 'result.html',{'name':value,
    #     'inCharge':str(Hall.objects.only('inCharge').get(name=value).inCharge), 
    #     'capacity':str(Hall.objects.only('capacity').get(name=value).capacity), 
    #     'no':str(Hall.objects.only('no').get(name=value).no),'form':frm1,'ch':False} )
    # else:
    #     return HttpResponse('<p>no such hall</p>')