from django.urls import path
from . import views

urlpatterns = [
    path('', views.signin, name="signin"),
    path('home/', views.home, name="home"),
    path('result/',views.result,name="result"),
    path('book/',views.book,name="book")
]
