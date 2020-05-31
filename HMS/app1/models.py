from django.db import models

# Create your models here.

class UserAccount (models.Model):
    user_id=models.CharField(max_length=100, null=False , primary_key=True)
    email=models.EmailField(null=True)
    contact_no=models.CharField(max_length=13)
    password=models.CharField(max_length=100)
    
class Services(models.Model):
    service_id=models.CharField(max_length=10, null=False, primary_key=True)
    service_type=models.CharField(max_length=15, null=False)
    service_desc=models.CharField(max_length=1000, null=True)
    price=models.DecimalField( max_digits=12, decimal_places=2, default="0")
    
class PayByCard(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(null=True)
    address=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    country=models.CharField(max_length=50)
    zipcode=models.IntegerField()
    nameOnCard=models.CharField(max_length=30)
    cardNo=models.CharField(max_length=20)
    expMonth=models.CharField(max_length=10)
    expYear=models.DecimalField(max_digits=4, decimal_places=0)
    
class Payment(models.Model):
    date=models.DateField()
    totalAmount=models.DecimalField( max_digits=12, decimal_places=2, default="0")
    paidAmount=models.DecimalField( max_digits=12, decimal_places=2, default="0")
    PayByCard=models.OneToOneField(PayByCard, on_delete=models.CASCADE, null=True)
    desc=models.CharField(max_length=1000, null=True)
    
    
    
    
class Booking(models.Model):
    name=models.CharField(max_length=30)
    checkin=models.DateField()
    checkout=models.DateField(null=True)
    cnic=models.CharField(max_length=15 , null=True)
    email=models.EmailField(null=True)
    phone=models.CharField(max_length=30)
    desc=models.CharField(max_length=1000, null=True)
    isActive=models.BooleanField(default=True)
    services=models.ManyToManyField(Services, blank=True)
    totalAmount=models.DecimalField( max_digits=12, decimal_places=2, default="0")
    payment=models.OneToOneField(Payment, on_delete=models.CASCADE,null=True)


    
class Rooms(models.Model):
    room_id=models.CharField(max_length=100, null=False , primary_key=True)
    capacity=models.IntegerField()
    floor=models.CharField(max_length=105, null=False )
    booking=models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    price=models.DecimalField( max_digits=12, decimal_places=2, default="0")