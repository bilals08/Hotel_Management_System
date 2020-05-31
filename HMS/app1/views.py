from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.shortcuts import redirect
from .models import UserAccount, Rooms, Services, Booking, PayByCard, Payment
from datetime import *

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
            Price=room.get('Price')

            if len(roomId)<=1:
                message="Please Enter Correct Records."
                return render(request, 'Addroomform.html',{'message': message })
            if Rooms.objects.filter(pk=roomId):
                message="Room Already Exist."
                return render(request, 'Addroomform.html',{'message': message })
            
            db_Object=Rooms(room_id=roomId, capacity=capacity, floor=floor, price=Price)
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
        Price=service.get('Price')
        
        if len(sId)<=1: #Checking if ID is correct
            message="Please Enter Correct Records."
            return render(request, 'addservices.html',{'message': message })
        if Services.objects.filter(pk=sId): #chech if already exist
            message="Service Already Exist."
            return render(request, 'addservices.html',{'message': message })
        
        db_Object=Services(service_id=sId, service_type=sType, service_desc=sDesc, price=Price)
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
        email=book.get('email')
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
        
        return render(request, 'roomdetail.html',{'roomid': getroom.room_id,'capacity':getroom.capacity,'floor':getroom.floor, 'status':status, 'Price':getroom.price})
        
    else:
        rooms=Rooms.objects.all().values_list('room_id', flat=True)
        return render(request, 'viewrooms.html',{'Rooms': rooms})
    
def ViewServices(request):
    if not request.session.get('id'):
        return redirect('login')
    
    if request.POST:
        serviceid=request.POST.dict().get('service')
        getservice=Services.objects.get(pk=serviceid)
        
        return render(request, 'servicedetail.html',{'id': getservice.service_id,'type':getservice.service_type,'desc':getservice.service_desc,'Price':getservice.price })
        
    else:
        services=Services.objects.all().values_list('service_id', flat=True)
        return render(request, 'viewservices.html',{'Services': services})
    
def ViewBookings(request):
    if not request.session.get('id'):
        return redirect('login')
    
    if request.POST:
        VB=request.POST.dict().get('VB')
        UB=request.POST.dict().get('UB')
        DB=request.POST.dict().get('DB')
        MP=request.POST.dict().get('MP')
        UBA=request.POST.dict().get('UBA')
        Search=request.POST.dict().get('Search')
        MC=request.POST.dict().get('MC')
        DropB=request.POST.dict().get('DropB')
        
        print('Hello' + str(MC))
        if Search:
            opt=request.POST.dict().get('Option')
            text=request.POST.dict().get('SearchText')
            message=""
            if opt=='SBN':  ##Search BY Name
                bookings=Booking.objects.filter(name__contains=text).filter(isActive=True)
                if len(bookings)<1:
                    message="No Match Found"
            elif opt=='SBD': ##Search BY Date
                if len(text)==10:
                    bookings=Booking.objects.filter(checkin=text).filter(isActive=True)
                    if len(bookings)<1:
                        message="No Match Found"
                else:
                    message="Invalid Date Format. Format Must be (YYYY-MM-DD)" 
            if message:
                return render(request, 'makebookingmessage.html',{'message': message })
            else:
                bookings=bookings.values_list('id', flat=True)
                return render(request, 'viewbookings.html',{'bookings': bookings, 'Searched':"True", 'Query': text})
        elif DropB:
            booking=Booking.objects.get(pk=DropB)
            booking.checkout=date.today()
            booking.isActive=False
            if booking.payment:
                payment=Payment.objects.get(pk=booking.payment.id)
                payment.delete()
            booking.payment=None
            booking.save()
            message="Booking Droped." 
            return render(request, 'makebookingmessage.html',{'message': message })
        elif MC:
            booking=Booking.objects.get(pk=MC)
            booking.checkout=date.today()
            booking.isActive=False
            booking.save()
            message="Marked Check-out" 
            return render(request, 'makebookingmessage.html',{'message': message })
        elif UBA:
            print(UBA)
            booking=Booking.objects.get(pk=UBA)
            book=request.POST.dict()
            _name=book.get('name')
            _date=book.get('checkin')
            _cnic=book.get('cnic')
            _phone=book.get('phone')
            _email=book.get('email')
            _desc=book.get('desc')
            _rooms=request.POST.getlist('Room')
            _services=request.POST.getlist('Service')
            
            ###Delete Rooms
            frooms=Rooms.objects.filter(booking=booking.id)
            for room in frooms:
                room.booking=None
                room.save()    
            #### Delete Services
            booking.services.clear()
            booking.services.all()                  
            #### Update
            booking.name=_name
            booking.checkin=_date
            booking.cnic=_cnic
            booking.phone=_phone
            booking.email=_email
            booking.desc=_desc
            print(_services)
            print(_rooms)
            for service in _services:
                booking.services.add(service)
            for i in range(len(_rooms)):
                room=Rooms.objects.get(pk=_rooms[i])
                room.booking=booking
                room.save()
            booking.save()
            message="Booking Updated."
            return render(request, 'makebookingmessage.html',{'message': message })
                
        
        elif MP:
            booking=Booking.objects.get(pk=MP)
            if date.today()>booking.checkin:
                NumberOfDays=date.today()-booking.checkin
                NumberOfDays=int(NumberOfDays.days+1)
            else:
                NumberOfDays=1
            
            ###Calculate Subtotal and Tax and Total
            subtotal=0
            rooms= Rooms.objects.filter(booking=booking.id)
            for room in rooms:
                subtotal+=float(room.price)*NumberOfDays
            for service in booking.services.all():
                subtotal+=float(service.price)
            tax=int(subtotal*0.14)
            total=subtotal+tax
            booking.totalAmount=total
            booking.save()
            return render(request, 'paymentdetail.html',{'Days': NumberOfDays, 'Booking':booking, 'Rooms': rooms, 'Services':booking.services.all(),
                                                          'Subtotal':subtotal,
                                                         'Tax':tax, 'Total':total})
        elif VB:
            booking=Booking.objects.get(pk=VB)
            rooms= Rooms.objects.filter(booking=booking.id)         
            services=booking.services.all()
            return render(request, 'bookdetail.html',{'booking': booking, 'rooms': rooms, 'services':services })
        elif UB:
            booking=Booking.objects.get(pk=UB)
            rooms= Rooms.objects.filter(booking=None ) | Rooms.objects.filter(booking=booking)
            roomsall=rooms.values_list('room_id', flat=True)         
            servicesall=Services.objects.all().values_list('service_id', flat=True) 
            
            rooms=Rooms.objects.filter(booking=booking ).values_list('room_id', flat=True)
            services=booking.services.all().values_list('service_id', flat=True) 
            return render(request, 'updatebooking.html',{'booking': booking, 'Rooms': rooms, 'Services':services,
                                                          'RoomsAll':roomsall, 'ServicesAll':servicesall})
            
        elif DB:
            booking=Booking.objects.get(pk=DB)
            rooms= Rooms.objects.filter(booking= booking.id).booking=None
            
            Booking.objects.filter(id=booking.id).delete()
            message="Booking Deleted."
            return render(request, 'makebookingmessage.html',{'message': message })
            
  
                

        
    else:
        bookings=Booking.objects.filter(isActive=True).values_list('id', flat=True)
        return render(request, 'viewbookings.html',{'bookings': bookings})
    
def _Payment(request):
    if not request.session.get('id'):
        return redirect('login')
    
    if request.POST:
        PTCard=request.POST.dict().get('PTCard')
        PTCash=request.POST.dict().get('PTCash')
        CardPayment=request.POST.dict().get('CardPayment')
        
        if PTCard:
            booking=Booking.objects.get(pk=PTCard)
            
            if booking.payment:
                message="Already Paid."
                return render(request, 'makebookingmessage.html',{'message': message })
            
            return  render(request, 'paybycard.html',{'booking': booking})
        elif CardPayment:
            name=request.POST.dict().get('name')
            email=request.POST.dict().get('email')
            address=request.POST.dict().get('address')
            city=request.POST.dict().get('city')
            country=request.POST.dict().get('country')
            zipcode=request.POST.dict().get('zip')
            cardname=request.POST.dict().get('cardname')
            cardnumber=request.POST.dict().get('cardnumber')
            expmonth=request.POST.dict().get('expmonth')
            expyear=request.POST.dict().get('expyear')
            
            ##Making PayByCard Instance
            obj=PayByCard(name=name, email=email, address=address, city=city, 
                          country=country, zipcode=zipcode, nameOnCard=cardname,
                          cardNo=cardnumber, expMonth=expmonth, expYear=expyear)
            obj.save()
            
            ##Making Payment Instance
            booking=Booking.objects.get(pk=CardPayment)
            obj1=Payment(totalAmount=booking.totalAmount, paidAmount=booking.totalAmount,
                         date=date.today(), PayByCard=obj)
            obj1.save()
            booking.payment=obj1
            booking.save()
            
            message="Payment Successful."
            return render(request, 'makebookingmessage.html',{'message': message })
        
        elif PTCash:
            booking=Booking.objects.get(pk=PTCash)
            if booking.payment:
                message="Already Paid."
                return render(request, 'makebookingmessage.html',{'message': message })
            
            
            Amount=request.POST.dict().get('Amount')   
            obj1=Payment(totalAmount=booking.totalAmount, paidAmount=Amount,
                         date=date.today(), PayByCard=None)
            obj1.save()
            booking.payment=obj1
            booking.save()
            message="Payment Successful."
            return render(request, 'makebookingmessage.html',{'message': message })
        
    else:
        return redirect('viewbookings')
    
def BookingReport(request):
    
    if not request.session.get('id'):
        return redirect('login')
    
    if request.POST:
        SD=request.POST.dict().get('SD')
        ED=request.POST.dict().get('ED')
        
        booking=Booking.objects.filter(checkin__gte=SD).filter(checkin__lte=ED)
        active=0
        drop=0
        finish=0
        for b in booking:
            if b.isActive:
                active+=1
            elif not b.isActive and b.payment:
                finish+=1
            elif not b.isActive and not b.payment:
                drop+=1
                
        total=active+finish+drop
                
        return render(request, 'bookingreport.html',{'bookings': booking, 'total':total, 'finish':finish, 'drop':drop,'active':active,
                                                     'date':date.today()})
    
    return render(request, 'bookingreport.html')

def FinanceReport(request):
    if not request.session.get('id'):
        return redirect('login')
    
    if request.POST:
        SD=request.POST.dict().get('SD')
        ED=request.POST.dict().get('ED')
        
        booking=Booking.objects.filter(checkin__gte=SD).filter(checkin__lte=ED)
        total=0
        earning=0
        loss=0
        for b in booking:
            total+=b.totalAmount
            if b.payment:
                earning+=b.payment.paidAmount
        
        loss=total-earning
                
        return render(request, 'financereport.html',{'bookings': booking, 'total':total, 'earning':earning, 'loss':loss,
                                                     'date':date.today()})
        
    return render(request, 'financereport.html')
   