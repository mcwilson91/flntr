from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from flntr_app.models import Flat, FlatImage, StudentProfile, Landlord, Room
from flntr_app.forms import AddFlatForm, FlatSearchForm, RoommateSearchForm, AgeForm, UserForm, AddFlatImageForm, ProfileForm
from django.contrib.auth.models import User, Group
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from django.contrib import messages
import requests

# Create your views here.
def index(request):
	recent_flat_list = Flat.objects.order_by('-dayAdded')[:3]
	most_viewed_flats = Flat.objects.order_by('-views')[:3]
	context_dict = {'recentflats': recent_flat_list, 'mostviewed':most_viewed_flats}
	return render(request, 'flntr/index.html', context_dict)

def about(request):
	return render(request, 'flntr/about.html')

def search(request):
	search_form = FlatSearchForm();
	roommate_form = RoommateSearchForm();
	if request.method == 'POST':
		room_form = FlatSearchForm(request.POST)
		if room_form.is_valid(): # All validation rules pass
			#print(room_form.cleaned_data['min_price'])
			min_price = room_form.cleaned_data['min_price']
			max_price = room_form.cleaned_data['max_price']
			min_rooms = room_form.cleaned_data['min_rooms']
			max_rooms = room_form.cleaned_data['max_rooms']
			date_added = room_form.cleaned_data['date']
			max_distance = room_form.cleaned_data['distance']
			params = {'min_price': min_price, 'max_price':max_price, 'min_rooms':min_rooms, 'max_rooms':max_rooms, 'date_added':date_added, 'max_distance':max_distance}
			return results(request, params)
	return render(request, 'flntr/search.html', {'search_form':search_form, 'roommate_form':roommate_form})

def results(request, params):

	results = Flat.objects.filter(
						averageRoomPrice__gte=params['min_price'],
						averageRoomPrice__lte=params['max_price'],
						numberOfRooms__gte=params['min_rooms'],
						numberOfRooms__lte=params['max_rooms'],
						dayAdded__gte=datetime.now() - timedelta(days=int(params['date_added'])),
						distanceFromUniversity__lte=params['max_distance'])


	context_dict = {'results':results}
	return render(request, 'flntr/results.html', context_dict)

def register(request):
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		age_form = AgeForm(data=request.POST)
		if user_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			group_choice = request.POST.get('group_choice')

			user.save()
			if group_choice == 'Student':
				g = Group.objects.get(name='students')
				g.user_set.add(user)
				profile = age_form.save(commit=False)
				profile.user = user

				profile.save()
			else:
				g = Group.objects.get(name='landlords')
				g.user_set.add(user)
				p = Landlord.objects.get_or_create(user=user)[0]
				p.save()
			registered = True
		else:
			print(user_form.errors)
	else:
		user_form = UserForm()
		age_form = AgeForm()


	return render(request, 'flntr/register.html',
					{'user_form': user_form,
					'age_form': age_form,
					'registered': registered})




def user_login(request):
	if request.method == 'POST':

		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)


		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
				# An inactive account was used - no logging in!
				return HttpResponse("Your flntr account is disabled.")
		else:
			# Bad login details were provided. So we can't log the user in.
			messages.info(request, 'Invalid login details')
			# print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponseRedirect(reverse('login'))
	else:
		return render(request, 'flntr/login.html', {})

def property(request):
	all_flat_list = Flat.objects.order_by('-dayAdded')
	context_dict = {'allflats': all_flat_list}
	return render(request, 'flntr/property.html', context_dict)

def show_property(request, flat_id_slug):
	context_dict = {}
	try:
		flat = Flat.objects.get(slug=flat_id_slug)
		flat.views = flat.views + 1
		flat.save()
		context_dict['flat'] = flat
		try:
			image_list = FlatImage.objects.filter(flat=flat)
			context_dict['imagelist'] = image_list
		except FlatImage.DoesNotExist:
			context_dict['imagelist'] = None
		try:
			room_list = Room.objects.filter(flat=flat).order_by('roomNumber')
			context_dict['roomlist'] = room_list
		except Room.DoesNotExist:
			context_dict['roomlist'] = None
	except Flat.DoesNotExist:
		context_dict['flat'] = None
	return render(request, 'flntr/show_property.html', context_dict)


def show_property_user_profile(request, flat_id_slug, student_profile_slug):
	context_dict = {}
	try:
		profile = StudentProfile.objects.get(slug=student_profile_slug)
		context_dict['studentprofile'] = profile
	except StudentProfile.DoesNotExist:
		context_dict['studentprofile'] = None
	return render(request, 'flntr/show_user_profile.html', context_dict)

def show_user(request):
	return render(request, 'flntr/show_user.html')

def show_user_invitations(request):
	return render(request, 'flntr/show_user_invitations.html')

def show_user_requests(request):
	return render(request, 'flntr/show_user_requests.html')

def show_user_account(request, username):
	user = User.objects.get(username=username)
	try:
		studentProfile = StudentProfile.objects.get(user=user)
		return redirect('show_user_profile', student_profile_slug=studentProfile.slug)
	except StudentProfile.DoesNotExist:
		landlord = Landlord.objects.get(user=user)
		return redirect('show_user_properties', landlord_id_slug=landlord.slug)


def show_user_profile(request, student_profile_slug):
		context_dict = {}
		try:
			profile = StudentProfile.objects.get(slug=student_profile_slug)
			context_dict['studentprofile'] = profile
			profile_form = UserForm(initial={'bio': profile.bio, 'picture': profile.picture})
			age_form = AgeForm(initial={'age': profile.age, 'gender': profile.gender})
		except StudentProfile.DoesNotExist:
			context_dict['studentprofile'] = None
		return render(request, 'flntr/show_user_profile.html', context_dict)

def edit_profile(request):
	edit = False
	user = request.user
	current_user = user
	try:
		profile = StudentProfile.objects.get(user=user)
	except StudentProfile.DoesNotExist:
		profile = None
	if  request.method == 'POST':

		profile_form = ProfileForm(data=request.POST, instance=profile)
		age_form = AgeForm(data=request.POST, instance=profile)
		if profile_form.is_valid() and age_form.is_valid():
			profile = profile_form.save(commit=False)
			age = age_form.save(commit=False)

			profile.user = current_user
			age.user = current_user
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()
			age.save()
			edit = True
			return redirect('show_user_profile', student_profile_slug=profile.slug)
			#HttpResponseRedirect(reverse('show_user_account user.username'))
		else:
			print(profile_form.errors, age_form.errors)
	else:
		context_dict = {}
		try:
			profile = StudentProfile.objects.get(user=user)
			context_dict['studentprofile'] = profile
			profile_form = ProfileForm(instance=profile, initial={'bio': profile.bio, 'picture': profile.picture})
			age_form = AgeForm(instance=profile, initial={'age': profile.age, 'gender': profile.gender})
			context_dict['profile_form'] = profile_form
			context_dict['age_form'] = age_form
		except StudentProfile.DoesNotExist:
			context_dict['studentprofile'] = None

		return render(request, 'flntr/edit_profile.html', context_dict)

def delete_profile(request):

	deleted = False
	if request.method == 'POST':
		password = request.POST.get('password')
		username = request.user.username
		user = authenticate(username=username, password=password)
		if user:
			user.delete()
			messages.success(request, "User deleted")
			#deleted = True
			return redirect('index')
		else:
			user = request.user
			# do something that alerts unsuccessful
	context_dict = {}
	profile = StudentProfile.objects.get(user=request.user)
	context_dict['studentprofile'] = profile
	context_dict['deleted'] = deleted
	return render(request, 'flntr/delete_profile.html', context_dict)




def show_user_properties(request, landlord_id_slug):
	context_dict = {}
	landlord = Landlord.objects.get(slug=landlord_id_slug)
	context_dict['landlordname'] = landlord.user.first_name + " " + landlord.user.last_name
	landlord_flat_list = Flat.objects.filter(owner=landlord).order_by('-dayAdded')
	context_dict['landlordflats'] = landlord_flat_list
	return render(request, 'flntr/show_user_properties.html', context_dict)

def show_user_properties_aProperty(request, landlord_id_slug, flat_id_slug):
	context_dict = {}
	try:
		flat = Flat.objects.get(slug=flat_id_slug)
		context_dict['flat'] = flat
		try:
			image_list = FlatImage.objects.filter(flat=flat)
			context_dict['imagelist'] = image_list
		except FlatImage.DoesNotExist:
			context_dict['imagelist'] = None
		try:
			room_list = Room.objects.filter(flat=flat).order_by('roomNumber')
			context_dict['roomlist'] = room_list
		except Room.DoesNotExist:
			context_dict['roomlist'] = None
	except Flat.DoesNotExist:
		context_dict['flat'] = None
	return render(request, 'flntr/show_property.html', context_dict)


@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

def add_flat(request):
	flat_form = AddFlatForm()
	image_form = AddFlatImageForm()
	if request.method == 'POST':
		flat_form = AddFlatForm(request.POST)
		image_form = AddFlatImageForm(request.POST, request.FILES)
		if flat_form.is_valid():
			flat = flat_form.save(commit=False)
			flat.owner = Landlord.objects.get(pk=1)

			originAddress = flat_form.cleaned_data['streetAddress'].replace(" ", "+")
			destinationAddress = "University of Glasgow".replace(" ", "+")
			key = "AIzaSyBW0crhPrG5Yc6_hh9fbjb8_LqqW2Je3Ho"
			url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={},Glasgow&destinations={}&key={}".format(originAddress, destinationAddress, key)
			print(url)
			r = requests.get(url)
			js = r.json()
			distance = int(js['rows'][0]['elements'][0]['distance']['value'])
			flat.distanceFromUniversity = distance
			flat.distanceText = js['rows'][0]['elements'][0]['distance']['text']
			print(distance)

			flat.save()

			picture = image_form.save(commit=False)
			picture.flat = flat
			if 'image' in request.FILES:
				picture.image = request.FILES['image']
			picture.save()
			return index(request)
		else:
			print(flat_form.errors)
	else:
		room_form = AddFlatForm()
	return render(request, 'flntr/add_flat.html', {'flat_form':flat_form, 'image_form':image_form})

#def edit_flat(request):
