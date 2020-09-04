from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin, name="signin"),
    path('details/', views.details, name="details"),
    path('', views.home, name="home"),
    path('home/', views.home, name="home"),
    path('result/',views.result,name="result"),
    path('book/',views.book,name="book"),
    path('hall/',views.hall,name="hall"),
    path('exportcsv/',views.csvdown,name="exportcsv"),
    path('confirm/<str:uid>/<str:token>/<str:bid>',views.confirm,name='confirm'),
    path('verified/<str:uid>/<str:token>/<str:bid>/<str:stat>/',views.verified,name='verified'),
]