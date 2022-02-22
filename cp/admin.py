from django.contrib import admin
from .models import Share, UserProfile, Ride_Requests,Room,Message,Inter_loc


admin.site.register(Share)
admin.site.register(UserProfile)
admin.site.register(Ride_Requests)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Inter_loc)

