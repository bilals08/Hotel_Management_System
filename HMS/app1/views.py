from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.shortcuts import redirect
from .models import UserAccount, Rooms

# Create your views here.
def index(request):
    return redirect('login')

def logout(request):
    if request.session.get('id'):
        del request.session['id']
    return redirect('/login')
    
def signup(request):
    return render(request,'project.html')

def register(request):
    if request.method=='POST':
        signup=request.POST.dict()
        username=signup.get("signup_id")
        password=signup.get("signup_pass")
        email=signup.get("signup_email")
        contact_no=signup.get("signup_contact")
        term=signup.get("terms")
        print(contact_no)
        if  UserAccount.objects.filter(pk=username):
            message="User Already Exist."
            return render(request, "authentication_message.html",{'message':message})
        if  email  and UserAccount.objects.filter(email=email):
            message="Email Already Exist."
            return render(request, "authentication_message.html",{'message':message})
        if  contact_no and UserAccount.objects.filter(contact_no=contact_no):
            message="Phone Number Already Exist."
            return render(request, "authentication_message.html",{'message':message})
        if username is None:
             message="Please Enter Information."
             return render(request, "authentication_message.html",{'message':message})
        if term!='on':
             message="Please Agree to the terms."
             return render(request, "authentication_message.html",{'message':message})
         
        db_Object=UserAccount(user_id=username, password=password, email=email, contact_no=contact_no)
        db_Object.save()
        message="Account Created."
        return render(request, "authentication_message.html",{'message':message})
    else:
        message="Please Sign Up."
        return render(request, "authentication_message.html",{'message':message})
    
def loggedin(request):
    if (request.POST):
        login=request.POST.dict()
        username=login.get("login_id")
        password=login.get("login_pass")
        
        ###Checking Whether the user exist by id,email and phone No
        isUser=False
        if UserAccount.objects.filter(pk=username):
            auth=UserAccount.objects.get(pk=username)
            isUser=True
        elif  UserAccount.objects.filter(email=username):
            auth=UserAccount.objects.get(email=username)
            isUser=True
        elif UserAccount.objects.filter(contact_no=username):
            auth=UserAccount.objects.get(contact_no=username)
            isUser=True
        
        if(isUser):
            if auth.password==password:
                request.session['id']=username
                return redirect('/home')
                
            else:
                message="Password Doesn't Match."
                return render(request, "authentication_message.html",{'message':message})
        
        else:
            message="User Doesn't Exist."
            return render(request, "authentication_message.html",{'message':message})
        

def Home(request):
    if not request.session.get('id') is None:
        return render(request, "home.html")
    else:
        return redirect ('/login')
    
def addroom(request):
    if request.session.get('id'):
        if request.POST:
            room=request.POST.dict()
            roomId=room.get('RoomNo')
            capacity=room.get('Capacity')
            floor=room.get('FloorNo')
            
            if len(roomId)<=1:
                message="Please Enter Correct Records."
                return render(request, 'Addroomform.html',{'message': message })
            if Rooms.objects.filter(pk=roomId):
                message="Room Already Exist."
                return render(request, 'Addroomform.html',{'message': message })
            
            db_Object=Rooms(room_id=roomId, capacity=capacity, floor=floor)
            db_Object.save()
            message="Room Added."
            return render(request, 'Addroomform.html',{'message': message })
        else:
            return render(request, 'Addroomform.html')

    else:
        return redirect('login')
    
def removeroom(request):
    if request.session.get ('id'):
        if request.POST:
            roomno=request.POST.get("RoomNo")
            if Rooms.objects.filter(room_id=roomno):
                Rooms.objects.filter(room_id=roomno).delete()
                message="Room Deleted."
                return render(request, 'removeroomform.html',{'message': message })
            else:
                message="Room Doesn't Exist."
                return render(request, 'removeroomform.html',{'message': message })
        else:
           return render(request, 'removeroomform.html') 
    else:
        return redirect('login')

def UpdateRoom(request):
    if not request.session.get('id'):
        return redirect('login')
    
    if request.POST:
        room=request.POST.dict()
        roomId=room.get('RoomNo')
        capacity=room.get('Capacity')
        floor=room.get('FloorNo')
        
        if not Rooms.objects.filter(room_id=roomId):
            message="Room Doesn't Exist."
            return render(request, 'updateroomform.html',{'message': message })
        r=Rooms.objects.get(room_id=roomId)
        r.capacity=capacity
        r.floor=floor
        r.save()
        message="Room Updated."
        return render(request, 'updateroomform.html',{'message': message })
    
    return render(request,'updateroomform.html')
        
