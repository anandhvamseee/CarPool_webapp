from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
#from notify.signals import notify
from .models import Share, Ride_Requests,UserProfile,Room,Message,Inter_loc
from .forms import UserRegistrationForm, UserProfileForm
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import F
from geopy.exc import GeocoderTimedOut
import json
import reverse_geocode
import math
from django.core.mail import EmailMessage
from geopy.geocoders import GoogleV3
import googlemaps


def index(request):
	return render(request, 'cp/index.html')

@login_required(login_url = 'LOGIN')
def search(request):
	username = request.user
	user_ob = User.objects.all().filter(username = username).first()
	user_pro_ob = UserProfile.objects.all().filter(user = user_ob).first()
	gender = user_pro_ob.gender
	return render(request, 'cp/search.html', {'gender':gender})

@login_required(login_url = 'LOGIN')
def share(request):
	username = request.user
	user_ob = User.objects.all().filter(username = username).first()
	user_pro_ob = UserProfile.objects.all().filter(user = user_ob).first()
	gender = user_pro_ob.gender
	return render(request, 'cp/share.html', {'gender':gender})

@login_required(login_url = 'LOGIN')
def trips(request):
	driver = User.objects.filter(username = request.user).first()
	rider = User.objects.filter(username = request.user).first()
	driving= Ride_Requests.objects.all().filter(to_user = driver).filter(visited = False)
	driving_trips = Ride_Requests.objects.all().filter(to_user = driver).filter(ride_status = True)
	driving_trips_objects = []
	for i in driving_trips:
		driving_trips_objects.append(i.ride_data)
	driving_trips_objects = list(set(driving_trips_objects))
	"""for i in driving_trips:
		if i.ride_data.id in driving_trips_ids:
			driving_trips_objects.append(i.ride_data)"""
	print(driving_trips_objects)
	#print(driving_trips_ids)
	print(driving_trips)
	riding = Ride_Requests.objects.all().filter(from_user = rider)
	"""for i in driving:
		r = Ride_Requests.objects.all().filter(ride_data = i)
		inner_driving.append(r)
		for j in r:
			print(j.from_user)
		print('------------')"""

	return render(request, 'cp/trips.html', {'driving':driving, 'riding':riding, 'driving_trips_objects':driving_trips_objects, 'driving_trips':driving_trips})

@csrf_exempt
def login(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get("password")

		user = authenticate(request, username=username, password=password)

		if user is not None:
			auth_login(request, user)
			return redirect('SEARCH')
		else:
			messages.info(request, 'username or password is incorrect')
	context={}
	return render(request,'cp/login.html', context)
@csrf_exempt
def logout(request):
	auth_logout(request)
	return redirect('LOGIN')

@csrf_exempt
def signup(request):
	if request.method == "POST":
		form = UserRegistrationForm(request.POST)
		profile_form = UserProfileForm(request.POST)
		if form.is_valid() and profile_form.is_valid():
			user = form.save()

			profile = profile_form.save(commit=False)
			profile.user = user
			profile.save()

			username = form.cleaned_data.get('username')
			print("hello",username)
			messages.success(request, 'Account was created for '+ username)
			subject = 'welcome to Easy Ride'
			message = f'Hi {user.username}, thank you for registering in Easy Ride.'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email, ]
			send_mail( subject, message, email_from, recipient_list )
			return redirect('LOGIN')
	else:
		form = UserRegistrationForm()
		profile_form = UserProfileForm()  
	return render(request, 'cp/signup.html', {'form':form,'profile_form':profile_form})
@csrf_exempt
def share_form_submission(request):
	print("hello")
	from_location= request.POST["from_location"]
	to_location = request.POST["to_location"]
	date = request.POST["date"]
	time = request.POST["time"]
	#date_posted = request.POST["date_posted"]
	spots_in_the_car = request.POST["spots_in_the_car"]
	women = request.POST.get("women_only", False)
	women = True if women else False
	fare = request.POST["fare"]
	username = request.user
	user_ob = User.objects.all().filter(username = username).first()
	user_pro_ob = UserProfile.objects.all().filter(user = user_ob).first()
	user_profile = user_pro_ob
	gender = user_pro_ob.gender
	print(gender)
	delete = request.POST.get("deleted", False)
	room_no = get_random_string(8)
	vehicle_info = request.POST['vehicle_details']
	vehicle_type = request.POST['type']
	intermediate_locations = ''
	#print(vehicle_type)
	if vehicle_type == '1':
		vehicle_type = 'Car'
	elif vehicle_type == '2':
		vehicle_type = 'Bike'
	else:
		vehicle_type = 'Van'
	user_shares = Share.objects.all().filter(username = request.user) 
	user_share_filter = user_shares.filter(from_location = from_location).filter(to_location = to_location).filter(date = date).filter(time = time).filter(deleted = False)
	if len(user_share_filter) == 0:
		print("its okay")
		share = Share(from_location=from_location,to_location=to_location, date=date, time=time, spots_in_the_car=spots_in_the_car, women_only=women, fare=fare, username = username, room_no = room_no, vehicle_info = vehicle_info, vehicle_type = vehicle_type, intermediate_locations = intermediate_locations, user_profile = user_profile )
		share.save()
		messages.success(request, 'Your Ride has been Posted!')
	else:
		messages.success(request, 'Your have already posted this ride!' )
	return render(request, 'cp/share.html',{'from_location':from_location, 'to_location':to_location, 'gender':gender})

from geopy.geocoders import Nominatim
def search_results(request):
	from_loc= request.POST["from_location"]
	to_loc = request.POST["to_location"]
	dat = request.POST["date"]
	women = request.POST.get("women_only", False)
	women = True if women else False
	#print(women)
	spots = request.POST["spots_in_the_car"]   
	vehicle_type = request.POST['type']
	print(vehicle_type)
	if vehicle_type == '1':
		vehicle_type = 'Car'
	elif vehicle_type == '2':
		vehicle_type = 'Bike'
	else:
		vehicle_type = 'Van'

	data = Share.objects.all()
	final_inter_list = []
	lat_lng = []
	geolocator = GoogleV3(api_key='AIzaSyBaaURpmG729XBqeASRVkQsbbUA9S5QAmE')
	gmaps = googlemaps.Client(key='AIzaSyBaaURpmG729XBqeASRVkQsbbUA9S5QAmE')
	geocode_result = gmaps.geocode(to_loc)
	print("this is googlr",geocode_result)
	to_loc_ = geolocator.geocode(to_loc)
	to_loc_latlng = [to_loc_.latitude,to_loc_.longitude]
	if women:
		search_results_list = data.filter(women_only = women).filter(from_location = from_loc).filter(to_location = to_loc).filter(date = dat).filter(spots_in_the_car__gte = spots).filter(vehicle_type = vehicle_type)
	else:
		search_results_list = data.filter(from_location = from_loc).filter(to_location = to_loc).filter(date = dat).filter(spots_in_the_car__gte = spots).filter(vehicle_type = vehicle_type)
	if len(search_results_list) == 0:
		share_inter_list = data.filter(from_location = from_loc).filter(date = dat).filter(spots_in_the_car__gte = spots).filter(vehicle_type = vehicle_type)
		for i in share_inter_list:
			print("in share_inter_list")
			print(i.intermediate_locations)
			if i.intermediate_locations == '':
				print('in []')
				continue
			else:
				print("in else []")
				lll = json.loads(i.intermediate_locations)
				if to_loc in lll:
					final_inter_list.append(i)
		if len(final_inter_list) > 0:
			return render(request, 'cp/search.html', {'search_results_list':search_results_list, 'from_loc':from_loc, 'to_loc':to_loc, 'spots':spots,'final_inter_list':final_inter_list})
		else:
			print("in else case")
			for i in share_inter_list:
				flocation = geolocator.geocode(i.from_location)
				tlocation = geolocator.geocode(i.to_location)
				lat_lng.append([i.id,flocation.latitude,flocation.longitude,tlocation.latitude,tlocation.longitude])

	return render(request, 'cp/search.html', {'search_results_list':search_results_list, 'from_loc':from_loc, 'to_loc':to_loc, 'spots':spots, 'lat_lng':lat_lng, 'to_loc_latlng':to_loc_latlng,'final_inter_list':final_inter_list})


def request_ride(request,username, id, spots):
	print(spots)
	#print(id)
	try:
		from_us = User.objects.filter(username = request.user).first()
		to_us = User.objects.filter(username = username).first()
		shar = Share.objects.filter(id = id).first()
		spots = spots

		if from_us == to_us:
			messages.success(request, 'you are the owner of the ride')
			return render(request, 'cp/search.html')
		else:
			rr = Ride_Requests(from_user = from_us, to_user = to_us, ride_data = shar, spots = spots)
			#print(rr.from_user,rr.to_user)
			rr.save()
			messages.success(request, 'Your request has been sent!' )
			#print(from_us,to_us,shar)
			return render(request, 'cp/search.html')
	except:
		messages.success(request, 'You have already requested!')
		return render(request, 'cp/search.html')
def ride_status_accept(request, id):
	print("this is", id)
	r_r_m = Ride_Requests.objects.all().filter(id = id).first()
	csc = r_r_m.ride_data.spots_in_the_car
	spots = r_r_m.spots
	if csc == 0:
		messages.success(request, 'you have no spots left!')
	else:
		r_r_m.ride_data.spots_in_the_car = csc - spots
		print(r_r_m.ride_data.spots_in_the_car)
		r_r_m.ride_data.save()
		user = r_r_m.from_user
		o_user = r_r_m.to_user
		subject = 'Trip Accepted'
		message = 'Hi {}, {} has accepted your ride request. You can contact {} by using this room name {} in our messages'.format(user.username,o_user.username,o_user.username,r_r_m.ride_data.room_no)
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [user.email, ]
		send_mail( subject, message, email_from, recipient_list )
		r_r_m.ride_status = True
		r_r_m.visited = True
		r_r_m.save()
	return trips(request)


def ride_status_reject(request, id):
	r_r_m = Ride_Requests.objects.all().filter(id = id).first()
	user = r_r_m.from_user
	o_user = r_r_m.to_user
	subject = 'Trip Rejected'
	message = 'Hi {}, {} has rejected your ride request.'.format(user.username,o_user.username)
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [user.email, ]
	send_mail( subject, message, email_from, recipient_list )
	r_r_m.ride_status = False
	r_r_m.visited = True
	r_r_m.save()
	return trips(request)

@login_required(login_url = 'LOGIN')
def user_profiles(request):
	usr = request.user.id
	print(type(request.user))
	usr_ob = User.objects.all().filter(id = usr).first()
	usr_pro_ob = UserProfile.objects.all().filter(user = usr_ob).first()
	driving= Share.objects.all().filter(username = usr_ob)
	return render(request, 'cp/profile.html', {'usr_pro_ob':usr_pro_ob, 'driving':driving})
@csrf_exempt
def user_driving_details(request):
	liscence_number = request.POST['number']
	liscence_picture = request.POST['picture']
	usr = request.user.id
	usr_ob = User.objects.all().filter(id = usr).first()
	usr_pro_ob = UserProfile.objects.all().filter(user = usr_ob).first()
	usr_pro_ob.liscence_number = liscence_number
	usr_pro_ob.liscence_picture = liscence_picture
	usr_pro_ob.save()
	return user_profiles(request)


def del_trip_pro(request, id):
	messages.warning(request, 'Your Ride has been deleted! But Please remember, if you delete your rides more than 3 times your account wiil be blocked')
	share_ob = Share.objects.all().filter(id = id).first()
	user_ob = share_ob.username
	user_pro_ob = UserProfile.objects.all().filter(user = user_ob).first()
	count = user_pro_ob.delete_count
	if count == 3 and usr_pro_ob.rating <= 1.5:
		User.objects.all().filter(username = user_ob).delete()
		return logout(request)
	else:
		user_pro_ob.delete_count = count+1
		user_pro_ob.save()
		share_ob.deleted = True
		share_ob.save()
		return user_profiles(request)

def edit_profile(request):
	usr = request.user.id
	usr_ob = User.objects.all().filter(id = usr).first()
	usr_pro_ob = UserProfile.objects.all().filter(user = usr_ob).first()
	driving= Share.objects.all().filter(username = usr_ob)
	return render(request, 'cp/edit_profile.html', {'usr_pro_ob':usr_pro_ob, 'driving':driving})

def edit_profile_form(request):
	e_name = request.POST['username']
	address = request.POST['address']
	e_email = request.POST['email']
	insta = request.POST['instagram']
	fac = request.POST['facebook']
	twit = request.POST['twitter']
	print(e_name,e_email,address)
	usr = request.user
	usr_ob = User.objects.all().filter(username = usr).first()
	usr_pro_ob = UserProfile.objects.all().filter(user = usr_ob).first()
	usr_ob.username = e_name
	usr_ob.email = e_email
	usr_pro_ob.address = address
	usr_pro_ob.instagram = insta
	usr_pro_ob.facebook = fac
	usr_pro_ob.twitter = twit
	usr_ob.save()
	usr_pro_ob.save()
	return user_profiles(request)

@login_required(login_url = 'LOGIN')
def home(request):
	username = request.user
	return render(request, 'cp/home.html', {'username':username})


def room(request, room):
    username = request.user
    room_details = Room.objects.get(name=room)
    return render(request, 'cp/room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('cp'+'/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('cp'+'/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})
def approve_msg(request):
	messages.success(request, 'Your request has been approved by the ride owner. You can contact him through the messages portal using the CODE given in the table')
	return trips(request)
def denied_msg(request):
	messages.success(request, 'Your Request ha been rejected by the ride owner.')
	return trips(request)

def pending_msg(request):
	messages.success(request, 'Your Request has been sent to the ride owner. Please verify after some to know the status.')
	return trips(request)

def deleted_msg(request):
	messages.success(request, 'We are sorry to inform you that, the ride you have request for is deleted by the owner.Please if there are any other ride in your route.')
	return trips(request)

def inter(request):
	return render(request, 'cp/intermediate.html')

@csrf_exempt
def edit_list(request):
	print("ajax!")
	#geolocator = Nominatim(user_agent="geoapiExercises")
	arr = request.POST.getlist('result[]')
	to = request.POST.get('to')
	print(arr,to)
	intermediate_locations_list = []
	for i in arr:
		so = Share.objects.all().filter(id = int(i)).first()
		if so.intermediate_locations == '':
			intermediate_locations_list.append(to)
			intermediate_locations_str = json.dumps(intermediate_locations_list)
			so.intermediate_locations = intermediate_locations_str
			so.save()
		else:
			intermediate_locations_list = json.loads(so.intermediate_locations)
			intermediate_locations_list.append(to)
			intermediate_locations_str = json.dumps(intermediate_locations_list)
			so.intermediate_locations = intermediate_locations_str
			so.save()
	return HttpResponse("success")

def query_mail(request):
	user = request.user
	subject = 'User Query'
	message = request.POST['query']
	email = EmailMessage(subject=subject, body=message, from_email=user.email, to=[settings.EMAIL_HOST_USER,], reply_to=[user.email])
	email.send()
	return user_profiles(request)



def index_query_mail(request):
	name = request.POST['name']
	uemail = request.POST['email']
	subject = request.POST['subject']
	message = request.POST['message']
	email = EmailMessage(subject=subject, body=message, from_email=uemail, to=[settings.EMAIL_HOST_USER,], reply_to=[uemail])
	email.send()
	return HttpResponse('Message sent successfully')


def handler404(request,exception):
	return render(request, 'cp/notfound.html')

@csrf_exempt
def rating(request,id):
	print("in rating")
	rating = request.POST['rating']
	us_id = id
	usr = UserProfile.objects.all().filter(id = us_id).first()
	usr.rating_lis = usr.rating_lis+rating
	avg_rat = 0
	for i in usr.rating_lis:
		avg_rat = avg_rat+int(i)
	usr.rating = avg_rat/len(usr.rating_lis)
	print()
	usr.save()
	print("this is ",us_id)
	print("rating",rating)

	return trips(request)

def view_profile(request,id):
	usr_ob = User.objects.all().filter(id = id).first()
	usr_pro_ob = UserProfile.objects.all().filter(user = usr_ob).first()
	driving= Share.objects.all().filter(username = usr_ob)
	return render(request, 'cp/profile.html', {'usr_pro_ob':usr_pro_ob, 'driving':driving})





