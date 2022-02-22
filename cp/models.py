from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime

GENDER_CHOICES = (
    ('male', 'male'),
    ('female', 'female'),
    ('LGBTQ', 'LGBTQ'),
)
WOMEN_ONLY_CHOICES = (
	('True', 'True'),
	('False','False'),)
VEHICLE_TYPE_CHOICES =(
	('Car', 'Car'),
	('Bike', 'Bike'),
	('Van', 'Van'))

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	user_img = models.ImageField(default = 'default.png', upload_to = 'profile_pics')
	gender = models.CharField(max_length=20, choices = GENDER_CHOICES, default= 'male')
	address = models.TextField(blank = True, default = 'press the edit button to add address')
	liscence_number = models.CharField(max_length = 10,blank = True)
	liscence_picture = models.ImageField(blank = True, upload_to = 'liscence_pics')
	delete_count = models.IntegerField(default = 0)
	instagram = models.CharField(max_length = 50, blank = True, default = '@user')
	facebook = models.CharField(max_length = 50, blank = True, default = '@user')
	twitter = models.CharField(max_length = 50, blank = True, default = '@user')
	rating_lis = models.CharField(max_length = 1000, blank = True, default = '')
	rating = models.FloatField(default = 0)

	def __str__(self):
		return self.user.username



class Share(models.Model):
	from_location = models.CharField(max_length=100)
	to_location = models.CharField(max_length=100)
	date = models.DateField()
	time = models.TimeField()
	#date_posted = models.DateTimeField(default=timezone.now)
	spots_in_the_car = models.IntegerField()
	women_only = models.BooleanField(default=False,choices = WOMEN_ONLY_CHOICES)
	fare = models.IntegerField(default = 0)
	username = models.ForeignKey(User, on_delete=models.CASCADE, null =True)
	deleted = models.BooleanField(default=False)
	room_no = models.CharField(blank = True, max_length=8)
	vehicle_info = models.CharField(blank = True, max_length = 100)
	vehicle_type = models.CharField(max_length=20, choices =VEHICLE_TYPE_CHOICES , default= 'Car')
	user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null =True)
	intermediate_locations = models.CharField(blank = True, max_length = 10000000000)


	def __str__(self):
		return self.username.username+'('+str(self.id)+')'


class Ride_Requests(models.Model):
	from_user = models.ForeignKey(User, on_delete=models.CASCADE, null =True, related_name = 'ride_request_from')
	to_user = models.ForeignKey(User, on_delete=models.CASCADE, null =True, related_name = 'ride_request_to')
	ride_data = models.ForeignKey('Share', on_delete=models.CASCADE, null =True, blank = True, related_name= 'ride_info')
	ride_status = models.BooleanField(default=False)
	visited = models.BooleanField(default=False)
	spots = models.IntegerField(blank = True, default=0)
	class Meta:
		unique_together = ["from_user", "to_user", "ride_data"]
	def __str__(self):
		return self.from_user.username+"->"+self.to_user.username+'('+str(self.id)+')'

	

class Inter_loc(models.Model):
	ride_data_ob = models.ForeignKey('Share', on_delete=models.CASCADE, null =True, blank = True, related_name= 'ride_information')
	lat_arr = models.CharField(max_length = 10000)
	long_arr = models.CharField(max_length = 10000, blank = True)
	


class Room(models.Model):
    name = models.CharField(max_length=1000)
class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)