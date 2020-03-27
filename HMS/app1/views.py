from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.shortcuts import redirect
from .models import UserAccount, Rooms, Services, Booking

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

def addService(request):
    if not request.session.get('id'):
        return redirect('login')
    if request.POST:
        service=request.POST.dict() #Extracting Data from Form
        sId=service.get('serviceId')
        sType=service.get('serviceType')
        sDesc=service.get('serviceDesc')
        
        if len(sId)<=1: #Checking if ID is correct
            message="Please Enter Correct Records."
            return render(request, 'addservices.html',{'message': message })
        if Services.objects.filter(pk=sId): #chech if already exist
            message="Service Already Exist."
            return render(request, 'addservices.html',{'message': message })
        
        db_Object=Services(service_id=sId, service_type=sType, service_desc=sDesc)
        db_Object.save()
        message="Service Added."
        return render(request, 'addservices.html',{'message': message })
            
    else:
        return render(request,'addservices.html')
    
def UpdateService(request):
    if not request.session.get('id'):
        return redirect('login')
    if request.POST:
        service=request.POST.dict() #Extracting Data from Form
        sId=service.get('serviceId')
        sType=service.get('serviceType')
        sDesc=service.get('serviceDesc')
        
        if not Services.objects.filter(pk=sId): #chech if already exist
            message="Service Doesn't Exist."
            return render(request, 'updateservice.html',{'message': message })
        
        s=Services.objects.get(pk=sId)
        s.service_type=sType
        s.service_desc=sDesc
        s.save()
        message="Service Updated."
        return render(request, 'updateservice.html',{'message': message })
    else:
        return render(request, 'updateservice.html')
        
def RemoveService(request):
    if not request.session.get('id'):
        return redirect('login')
    if request.POST:
        service=request.POST.dict() #Extracting Data from Form
        sId=service.get('serviceId')
        
        if Services.objects.filter(service_id=sId):
            Services.objects.filter(service_id=sId).delete()
            message="Service Deleted."
            return render(request, 'removeservice.html',{'message': message })
        else:
            message="Service Doesn't Exist."
            return render(request, 'removeservice.html',{'message': message })
    else:
        return render(request, 'removeservice.html') 
    
    
def MakeBooking(request):
    if not request.session.get('id'):
        return redirect('login')
    
    if request.POST:
        book=request.POST.dict()
        name=book.get('name')
        date=book.get('checkin')
        cnic=book.get('cnic')
        phone=book.get('phone')
        email=book.get('emai')
        desc=book.get('desc')
        
        message="" #Conditions to get valid values
        if cnic and len(cnic)<13:
            message="Invalid CNIC NO.(Length Must be 13 Digits)"
        elif len(phone)<11:
            message="Invalid Phone No.(Length Must be 11 Digits)"
        if message:
            return render(request, 'makebooking.html',{'message': message })
        
        db_Object=Booking(name=name,checkin=date,cnic=cnic,phone=phone,email=email,desc=desc ) #Saving Data
        db_Object.save()
        bid=db_Object.id
        
        rooms=Rooms.objects.all().filter(booking=None).values_list('room_id', flat=True)
        return render(request, 'selectroom.html',{'message': message, 'bid':bid, 'Rooms':rooms })
    else:
         return render(request, 'makebooking.html')
        
def MakeBooking1(request):
    if not request.session.get('id'):
        return redirect('login')
    
    if request.POST:
        rooms=request.POST.getlist('Room')
        bookN=request.POST.dict().get('bid')
         
        
        message=""
        if not bookN:
            message="Booking Id Error"
            return render(request, 'makebooking.html')
        elif len(rooms)<1:
            message="Please Select At Least 1 Room."
       
        bookNo=Booking.objects.get(pk=bookN) #Retrieving booking object
        
        if message:
            rooms=Rooms.objects.all().filter(booking=None).values_list('room_id', flat=True)
            return render(request, 'selectroom.html',{'message': message, 'bid':bookN, 'Rooms':rooms })
            
        for i in range(len(rooms)): #Assigning the book object to Room
            obj=Rooms.objects.get(pk=rooms[i])
            obj.booking=bookNo
            obj.save()
            
            services=Services.objects.all().values_list('service_id', flat=True)
            return render(request, 'selectservices.html',{'message': message, 'bid':bookN, 'Services':services })
            
    else:
        return redirect('makebooking')
    

def MakeBooking2(request):
    if not request.session.get('id'):
        return redirect('login')

    if request.POST:
        service=request.POST.getlist('Service')
        bookN=request.POST.dict().get('bid')
        
        
        if not bookN:
            message="Booking Id Error"
            return redirect('makebooking')
        
        bookNo=Booking.objects.get(pk=bookN) #Retrieving booking object
        
        for i in range(len(service)):
            bookNo.services.add(service[i])
            
        bookNo.save()
        message="Booking Added."
        return render(request, 'makebookingmessage.html',{'message': message, })
    else:
        return redirect('makebooking')
    
def ViewRooms(request):
    if not request.session.get('id'):
        return redirect('login')
    
    if request.POST:
        roomid=request.POST.dict().get('room')
        getroom=Rooms.objects.get(pk=roomid)
        
        status=""
        if getroom.room_id.startswith('A'):
            status="Executive"
        elif getroom.room_id.startswith('B'):
            status="Delux"
        else:
            status="classic"
        
        return render(request, 'roomdetail.html',{'roomid': getroom.room_id,'capacity':getroom.capacity,'floor':getroom.floor, 'status':status})
        
    else:
        rooms=Rooms.objects.all().values_list('room_id', flat=True)
        return render(request, 'viewrooms.html',{'Rooms': rooms})
    
def ViewServices(request):
    if not request.session.get('id'):
        return redirect('login')
    
    if request.POST:
        serviceid=request.POST.dict().get('service')
        getservice=Services.objects.get(pk=serviceid)
        
        return render(request, 'servicedetail.html',{'id': getservice.service_id,'type':getservice.service_type,'desc':getservice.service_desc})
        
    else:
        services=Services.objects.all().values_list('service_id', flat=True)
        return render(request, 'viewservices.html',{'Services': services})