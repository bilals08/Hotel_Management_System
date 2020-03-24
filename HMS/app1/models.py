from django.db import models

# Create your models here.

class UserAccount (models.Model):
    user_id=models.CharField(max_length=100, null=False , primary_key=True)
    email=models.EmailField(null=True)
    contact_no=models.CharField(max_length=13)
    password=models.CharField(max_length=100)
    
class Rooms(models.Model):
    room_id=models.CharField(max_length=100, null=False , primary_key=True)
    capacity=models.IntegerField()
    floor=models.IntegerField()
