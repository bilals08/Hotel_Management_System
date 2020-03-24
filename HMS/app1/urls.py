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
]
