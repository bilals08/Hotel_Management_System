from django.urls import path
from . import views



urlpatterns=[
    path('',views.index,name='index'),
    path('signup',views.signup, name='signup'),
    path('register',views.register, name='register'),
    path('login',views.signup, name='login'),
     path('loggedin',views.loggedin, name='loggedin'),
    path('home',views.Home, name='home'),
    path('addroom',views.addroom, name='addroom'),
    path('removeroom',views.removeroom, name='removeroom'),
    path('logout',views.logout, name='logout'),
    path('updateroom',views.UpdateRoom, name='updateroom'),
    
    path('addservice',views.addService, name='addservice'),
    path('updateservice',views.UpdateService, name='updateservice'),
    path('removeservice',views.RemoveService, name='removeservice'),
    
    path('makebooking',views.MakeBooking, name='makebooking'),
    path('makebooking1',views.MakeBooking1, name='makebooking1'),
    path('makebooking2',views.MakeBooking2, name='makebooking2'),
    
    path('viewrooms',views.ViewRooms, name='viewrooms'),
    path('viewservices',views.ViewServices, name='viewservices'),
    path('viewbookings',views.ViewBookings, name='viewbookings'),
    
    path('payment',views._Payment, name='payment'),
    path('bookingreport',views.BookingReport, name='bookingreport'),
    path('financereport',views.FinanceReport, name='financereport'),
]
