from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.UserAccount)
admin.site.register(models.Rooms)
admin.site.register(models.Services)
admin.site.register(models.Booking)
admin.site.register(models.PayByCard)
admin.site.register(models.Payment)
