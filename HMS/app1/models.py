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
    
class Booking(models.Model):
    name=models.CharField(max_length=30)
    checkin=models.DateField()
    cnic=models.CharField(max_length=13 , null=True)
    email=models.EmailField(null=True)
    phone=models.CharField(max_length=15)
    desc=models.CharField(max_length=1000, null=True)
    isActive=models.BooleanField(default=True)
    services=models.ManyToManyField(Services, null=True, blank=True)
    
class Rooms(models.Model):
    room_id=models.CharField(max_length=100, null=False , primary_key=True)
    capacity=models.IntegerField()
    floor=models.CharField(max_length=105, null=False )
    booking=models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True, default=None)