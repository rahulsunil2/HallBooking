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

# def result(request):
#     #form = searchbar()   
#     date = datetime.datetime.strptime(request.GET.get('initDate'),"%Y-%m-%d").date()
    
#     obid = Booking.objects.all() #getting objectid
#     hob = Hall.objects.all() #getting hall objects
#     n=0
#     halldict = {}
#     obj=[]
#     while n < len(hob):
#         x = 0
#         a = []
#         while x < len(obid):
#             if obid[x].hallNo.name ==  hob[n].name and date == obid[x].sdate :
#                 a.append(obid[x].stime)
#                 a.append(obid[x].etime)

#             x+=1

#         if len(a)>0:
#             a.sort()
#             halldict[n] = {}
#             halldict[n]['name'] = hob[n].name
#             halldict[n]['0'] = ['00:00:00',a[0].strftime("%H:%M:%S")]
#             halldict[n]['1'] = [a[len(a)-1].strftime("%H:%M:%S"),'00:00:00']
#             m=1
#             p=2
#             while m < len(a)-1:
#                 if (datetime.datetime.combine(date, a[m+1])-datetime.datetime.combine(date, a[m])) != 0:
#                     halldict[n][p] = [a[m].strftime("%H:%M:%S"),a[m+1].strftime("%H:%M:%S")]
#                     p+=1
#                     m+=2
#                 else:
#                     m+=2
#                     p+=1
#         else:
#             halldict[n] = {}
#             halldict[n]['name'] = hob[n].name
#             halldict[n]['0'] = ['00:00:00','00:00:00']
#         n+=1
#     print(halldict)
#     return render(request, 'result.html',{'halls':halldict})



# def home(request):

#     #global value,sdate,edate,stime,etime,haxxxxxxll,available

#     if 'check' in request.POST: #get time and redirect to next page
#         dateForm = detail(request.POST)
#         if dateForm.is_valid():
#             Sdate = dateForm.cleaned_data.get('sdate')
#             Edate = dateForm.cleaned_data.get('edate')
#             c="\n{} \n{}\n"
#             print(c.format(Sdate,Edate))
#             obid = Booking.objects.all() #getting objectid
#             hob = Hall.objects.all() #getting hall objects
#             a = []
            
#             for i in hob:
#                 print(i )
#                 for j in obid:
#                     n = 0
#                     print(j)
#                     if j.hallNo.no == i.no and j.sTime.date() == Sdate.date(): 
#                         n = 1
#                         chkResult = sartTimeCheck(j,Sdate.time(),Edate.time())
#                         if chkResult == 0:
#                             print(str(j) +"not possible")
#                             break
#                         else:
#                             if j.eTime.date() == Edate.date(): #same end date
#                                 endChkResult = endTimeCheck(j,Edate.time())
#                                 if endChkResult == 0:
#                                     print(str(j) + "not possible")
#                                     break
#                                 else:
#                                     print(str(j) + " possible")
#                                     a.append(i.name)
#                     else:

#                         #no hall booking at the same date but need to check end date
#                         for x in obid:
#                             if x.hallNo.no == i.no and x.eTime.date() == Edate.date():
#                                 n = 1
#                                 Rslt = endTimeCheck(x,Edate.time())
#                                 if Rslt == 0:
#                                     print(str(j) + "not possible")
#                                 else:
#                                     print(str(j) + " possible")
#                                     a.append(i.name)
#                 if n == 0:
#                     a.append(i.name)
#             if len(a) != 0:
#                 return HttpResponse(a)
#             else:
#                 return HttpResponse("No Halls Available")





#             #return HttpResponseRedirect('/result/?initDate=%s' %(dateForm.cleaned_data['sdate'],))

#     return render(request,'home.html',{'form':detail()})

# def sartTimeCheck(bookId,Time,Time2):
#     #checking for same start time or new booking starts b/w a ongoing event

#     if bookId.sTime.time() == Time or (Time > bookId.sTime.time() and Time < bookId.eTime.time()): 
#         return 0
#     else:
#         return endTimeCheck(bookId,Time2)

# def endTimeCheck(bookId,Time):
#     #same end time if end time of the booking is b/w the booking

#     if Time > bookId.sTime.time() : 
#         #or (Time > bookId.sTime.time() and Time < bookId.eTime.time())

#         return 0
#     else : 
#         return 1



def result(request):
    sdate = datetime.datetime.strptime(request.GET.get('sdate')[:-10], '%Y-%m-%d %H:%M')
    edate = datetime.datetime.strptime(request.GET.get('edate')[:-10], '%Y-%m-%d %H:%M')
    halls=list(Hall.objects.all())
    for i in halls:
        # if Booking.objects.filter(Q(hallNo=i) & ((Q(sTime_lte=sdate) & Q(eTime_gte=sdate)) | (Q(sTime_lte=edate) & Q(eTime_gte=edate)))).exists():
        if Booking.objects.filter(Q(hallNo=i) & ((Q(sTime__lte=sdate) & Q(eTime__gte=sdate)) | (Q(sTime__lte=edate) & Q(eTime__gte=edate)))).exists():
            halls.remove(i)
            print(i)
    print(halls)
    return render(request,'home.html',{'form':detail()})


def home(request):

    global value,sdate,edate,stime,etime,hall,available

    if 'check' in request.POST: #get time and redirect to next page
        dateForm = detail(request.POST)
        if dateForm.is_valid():
            Sdate = dateForm.cleaned_data['sdate']
            Edate = dateForm.cleaned_data['edate']
            c="\n{} \n{}\n"
            print(c.format(Sdate,Edate))
            return HttpResponseRedirect('/result/?sdate=%s&edate=%s' %(dateForm.cleaned_data['sdate'],dateForm.cleaned_data['edate']))

    return render(request,'home.html',{'form':detail()})

   