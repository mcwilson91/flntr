from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from flntr_app.models import Flat, FlatImage, StudentProfile, Landlord, Room, Request
from flntr_app.forms import AddFlatForm, FlatSearchForm, RoommateSearchForm, AgeForm, UserForm, AddFlatImageForm, ProfileForm, AddRoomForm, RequestForm, EditFlatForm, ContactForm, LoginForm
# from flntr_app.middleware import AjaxMessaging
from django.contrib.auth.models import User, Group
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from django.contrib import messages
import requests
from django.forms.formsets import formset_factory
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic.edit import FormView
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template
from django.db.models import Q

# Create your views here.
def index(request):
	recent_flat_list = Flat.objects.filter(availableRooms__gte=1).order_by('-dayAdded')[:3]

	try:
		recent_flat_images = FlatImage.objects.filter(flat__in=recent_flat_list, imageNumber=1)
	except FlatImage.DoesNotExist:
		recent_flat_images = None

	most_viewed_flats = Flat.objects.filter(availableRooms__gte=1).order_by('-views')[:3]

	try:
		viewed_flat_images = FlatImage.objects.filter(flat__in=most_viewed_flats, imageNumber=1)
	except FlatImage.DoesNotExist:
		viewed_flat_images = None

	context_dict = {'recentflats': recent_flat_list, 'mostviewed':most_viewed_flats, 'recent_flat_images':recent_flat_images, 'viewed_flat_images':viewed_flat_images}

	return render(request, 'flntr/index.html', context_dict)

def about(request):
	contact_form = ContactForm()

	if request.method == 'POST':
		form = ContactForm(data=request.POST)

		if form.is_valid():
			contact_name = request.POST.get('contact_name', '')
			contact_email = request.POST.get('contact_email', '')
			form_content = request.POST.get('content', '')

			# Email the profile with the
			# contact information

			context = {
			'contact_name': contact_name,
			'contact_email': contact_email,
			'form_content': form_content,
			}
			content = get_template('email_forms/contact_template.txt').render(context)
			email = EmailMessage("New contact form submission",	content, "flntr" +'', ['contact@flntr.co.uk'],
			headers = {'Reply-To': contact_email })

			email.send()
			return redirect('about')

	context_dict = {'contact_form': contact_form }
	return render(request, 'flntr/about.html', context_dict)

def search(request):
	search_form = FlatSearchForm();
	roommate_form = RoommateSearchForm();
	if request.method == 'POST':
		room_form = FlatSearchForm(request.POST)
		roommate_form = RoommateSearchForm(request.POST)
		if room_form.is_valid(): # All validation rules pass
			min_price = room_form.cleaned_data['min_price']
			max_price = room_form.cleaned_data['max_price']
			min_rooms = room_form.cleaned_data['min_rooms']
			max_rooms = room_form.cleaned_data['max_rooms']
			date_added = room_form.cleaned_data['date']
			max_distance = room_form.cleaned_data['distance']
			flatmate_gender = 'mixed'
			flatmate_gender2 = 'Male'
			flatmate_gender3 = 'Female'
			flatmate_min_age = 0
			flatmate_max_age = 999

			if roommate_form.is_valid() and request.user.is_authenticated:
				profile = StudentProfile.objects.get(user=request.user)
				if roommate_form.cleaned_data['gender'] == '2':
					user_gender = profile.gender.lower()
					if user_gender == 'male' or user_gender == 'female':
						flatmate_gender = user_gender
						flatmate_gender2 = user_gender
						flatmate_gender3 = user_gender
				if roommate_form.cleaned_data['age'] == '2':
					user_age = profile.age
					flatmate_min_age = int(user_age * 0.85)
					flatmate_max_age = int(user_age * 1.15)


			params = {'min_price': min_price, 'max_price':max_price, 'min_rooms':min_rooms, 'max_rooms':max_rooms, 'date_added':date_added, 'max_distance':max_distance, 'gender':flatmate_gender, 'gender2':flatmate_gender2, 'gender3':flatmate_gender3, 'min_age':flatmate_min_age, 'max_age':flatmate_max_age}
			print(params)
			return results(request, params)
	return render(request, 'flntr/search.html', {'search_form':search_form, 'roommate_form':roommate_form})

def results(request, params):
	results = Flat.objects.filter(
						Q(availableRooms__gte=1),
						Q(averageRoomPrice__gte=params['min_price']),
						Q(averageRoomPrice__lte=params['max_price']),
						Q(numberOfRooms__gte=params['min_rooms']),
						Q(numberOfRooms__lte=params['max_rooms']),
						Q(dayAdded__gte=datetime.now() - timedelta(days=int(params['date_added']))),
						Q(distanceFromUniversity__lte=params['max_distance']),
						Q(flatmateGender=params['gender']) | Q(flatmateGender__isnull=True) |
						Q(flatmateGender=params['gender2']) | Q(flatmateGender=params['gender3']),
						Q(averageAge__gte=params['min_age']) | Q(averageAge__isnull=True),
						Q(averageAge__lte=params['max_age']) | Q(averageAge__isnull=True))


	try:
		flat_images = FlatImage.objects.filter(flat__in=results, imageNumber=1)
	except FlatImage.DoesNotExist:
		flat_images = None

	context_dict = {'results':results, 'flat_images':flat_images}
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
		login_form = LoginForm(data=request.POST)
		username = login_form.data['username']
		password = login_form.data['password']
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("Your flntr account is disabled.")
		else:
			messages.info(request, 'Invalid login details')
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponseRedirect(reverse('login'))
	else:
		login_form = LoginForm()
		context_dict = {'login_form': login_form}
		return render(request, 'flntr/login.html', context_dict)

def property(request):
	all_flat_list = Flat.objects.order_by('-dayAdded')

	try:
		flat_images = FlatImage.objects.filter(flat__in=all_flat_list, imageNumber=1)
	except FlatImage.DoesNotExist:
		flat_images = None

	context_dict = {'allflats': all_flat_list, 'flat_images': flat_images}
	return render(request, 'flntr/property.html', context_dict)

def show_property(request, flat_id_slug):
	context_dict = {}
	context_dict['flat_id_slug'] = flat_id_slug
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

# def show_user(request):
# 	return render(request, 'flntr/show_user.html')

def show_user_invitations(request):
	return render(request, 'flntr/show_user_invitations.html')

def show_user_requests(request, landlord_id_slug):

	# request_formset = formset_factory(RequestResponseForm)

	# # if request.method == 'POST':
	# # 	request_response_form = RequestResponseForm(request.POST)
	# # 	studentslug = request_response_form.data['studentSlug']
	# # 	student = StudentProfile.objects.get(slug=studentslug)
	# # 	requestmade = Request.objects.get(student=student)
	# # 	requestmade.delete()
	# if request.method =='POST':
	# 	for request_form in request_formset:
	# 		if request_form.data['response'] == 1:
	# 			roomnumber = request_form.data['room']
	# 			flattitle = request_form.data['flat']
	# 			flat = Flat.objects.get(title=flattitle)
	# 			room = Room.objects.get(roomNumber=roomnumber, flat=flat)

	# 			room.student = student
	# 			room.save()
	# return redirect('show_user_requests', landlord_id_slug=landlord_id_slug)


	landlord = Landlord.objects.get(slug=landlord_id_slug)
	request_list = Request.objects.filter(landlord=landlord)
	context_dict = {'requests': request_list, 'landlordname': "%s %s" % (landlord.user.first_name, landlord.user.last_name)}
	return render(request, 'flntr/show_user_requests.html', context_dict)

def show_user_requests_aRequest(request, landlord_id_slug, student_profile_slug):
	student = StudentProfile.objects.get(slug=student_profile_slug)
	requestmade = Request.objects.get(student=student)

	if request.method == 'POST':
		if 'accept' in request.POST:
			room = requestmade.room
			room.student = student
			room.flat.availableRooms = room.flat.availableRooms - 1
			room.save()
		requestmade.delete()
		return redirect('show_user_requests', landlord_id_slug=requestmade.room.flat.owner.slug)
	return render(request, 'flntr/show_user_requests_aRequest.html', {'request': requestmade})

def show_user_requests_profile(request, landlord_id_slug, student_profile_slug):
	profile = StudentProfile.objects.get(slug=student_profile_slug)
	context_dict = {'studentprofile': profile}
	return render(request, 'flntr/show_user_profile.html', context_dict)

def show_user_account(request):
	# user = User.objects.get(username=username)
	user = request.user
	try:
		studentProfile = StudentProfile.objects.get(user=user)
		return redirect('show_user_profile', student_profile_slug=studentProfile.slug)
	except StudentProfile.DoesNotExist:
		landlord = Landlord.objects.get(user=user)
		return redirect('show_user_properties', landlord_id_slug=landlord.slug)


def show_user_profile(request, student_profile_slug):

	if request.method == 'POST':
		if request.POST == 'withdraw':
			student = StudentProfile.objects.get(slug=student_profile_slug)
			requestmade = Request.objects.get(student=student)
			requestmade.delete()

	context_dict = {}
	try:
		profile = StudentProfile.objects.get(slug=student_profile_slug)
		context_dict['studentprofile'] = profile
		try:
			studentRequest = Request.objects.get(student=profile)
			context_dict['requestsent'] = studentRequest
		except Request.DoesNotExist:
			context_dict['requestsent'] = None
		profile_form = UserForm(initial={'bio': profile.bio, 'picture': profile.picture})
		age_form = AgeForm(initial={'age': profile.age, 'gender': profile.gender})
	except StudentProfile.DoesNotExist:
		context_dict['studentprofile'] = None
	return render(request, 'flntr/show_user_profile.html', context_dict)

@login_required
def edit_profile(request):
	edit = False
	user = request.user
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

			profile.user = user
			age.user = user
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()
			age.save()
			edit = True
			return redirect('show_user_profile', student_profile_slug=profile.slug)
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

@login_required
def delete_profile(request):

	deleted = False
	if request.method == 'POST':
		password = request.POST.get('password')
		username = request.user.username
		user = authenticate(username=username, password=password)
		if user:
			user.delete()
			messages.success(request, "User deleted")
			deleted = True
			return redirect('index')
		else:
			user = request.user
			messages.info(request, 'Incorrect Password')
			# print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponseRedirect(reverse('delete_profile'))
			# do something that alerts unsuccessful
	context_dict = {}
	u = request.user
	try:
		profile = StudentProfile.objects.get(user=request.user)
	except StudentProfile.DoesNotExist:
		profile = Landlord.objects.get(user=u)

	context_dict['studentprofile'] = profile
	context_dict['deleted'] = deleted
	return render(request, 'flntr/delete_profile.html', context_dict)

@login_required
def change_password(request):
	if request.method == 'POST':
		user = request.user
		change_password_form = PasswordChangeForm(user, request.POST)
		if change_password_form.is_valid():

			user = change_password_form.save()
			update_session_auth_hash(request, user)
			messages.success(request, 'Your password is now updated!')
			return redirect('change_password')
		else:
			messages.error(request, "Something went wrong, please try again.")
	else:
		change_password_form = PasswordChangeForm(request.user)
	return render(request, 'flntr/change_password.html', {'change_password_form': change_password_form } )



def show_user_properties(request, landlord_id_slug):
	context_dict = {}
	landlord = Landlord.objects.get(slug=landlord_id_slug)
	context_dict['landlord'] = landlord
	context_dict['landlordname'] = "%s %s" % (landlord.user.first_name, landlord.user.last_name)
	landlord_flat_list = Flat.objects.filter(owner=landlord).order_by('-dayAdded')
	context_dict['landlordflats'] = landlord_flat_list

	try:
		landlord_flat_images = FlatImage.objects.filter(flat__in=landlord_flat_list, imageNumber=1)
	except FlatImage.DoesNotExist:
		landlord_flat_images = None

	context_dict['landlord_flat_images'] = landlord_flat_images

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

@login_required
def delete_flat(request, flat_id_slug):
	flat = Flat.objects.get(slug=flat_id_slug)
	flat.delete()
	return HttpResponseRedirect(reverse('show_user_account'))

@login_required
def edit_flat(request, flat_id_slug):
	flat = Flat.objects.get(slug=flat_id_slug)
	context_dict = {}
	if request.method == 'POST':
		edit_flat_form = EditFlatForm(data=request.POST, instance=flat)

		if edit_flat_form.is_valid():
			flat = edit_flat_form.save(commit=False)

			flat.save()
			return HttpResponseRedirect(reverse('show_user_account'))
		else:
			print(edit_flat_form.errors)
	else:

		context_dict['flat'] = flat
		edit_flat_form = EditFlatForm(instance=flat, initial={'title': flat.title, 'description': flat.description})
		context_dict['edit_flat_form'] = edit_flat_form

	return render(request, 'flntr/edit_flat.html', context_dict)


def add_flat(request):
	flat_form = AddFlatForm()
	image_form = AddFlatImageForm()
	room_formset = formset_factory(AddRoomForm)
	if request.method == 'POST':
		flat_form = AddFlatForm(request.POST)
		image_form = AddFlatImageForm(request.POST, request.FILES)
		room_formset = room_formset(request.POST)
		if flat_form.is_valid():
			flat = flat_form.save(commit=False)
			flat.owner = Landlord.objects.get(user=request.user)

			originAddress = flat_form.cleaned_data['streetAddress'].replace(" ", "+")
			destinationAddress = "University of Glasgow".replace(" ", "+")
			key = "AIzaSyBW0crhPrG5Yc6_hh9fbjb8_LqqW2Je3Ho"
			url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={},Glasgow&destinations={}&key={}".format(originAddress, destinationAddress, key)
			print(url)
			r = requests.get(url)
			js = r.json()

			if js['rows'][0]['elements'][0]['status'] == 'NOT_FOUND':
				return render(request, 'flntr/add_flat_error.html', {'address': originAddress.replace("+", " ")})
				#return HttpResponse("Could not find {}".format(originAddress).replace("+", " "))

			distance = int(js['rows'][0]['elements'][0]['distance']['value'])
			flat.distanceFromUniversity = distance
			flat.distanceText = js['rows'][0]['elements'][0]['distance']['text']
			print(distance)

			url2 = "https://maps.googleapis.com/maps/api/geocode/json?address={},Glasgow&key={}".format(originAddress, key)
			r2 = requests.get(url2)
			js2 = r2.json()
			if js2['status'] == 'OK':
				lat = js2['results'][0]['geometry']['location']['lat']
				lng = js2['results'][0]['geometry']['location']['lng']
				flat.latitude = lat
				flat.longitude = lng

			flat.save()

			if image_form.is_valid():
				image_num = 0;
				for file in image_form.cleaned_data['files']:
					image_num += 1
					FlatImage.objects.create(image=file, imageNumber=image_num, flat=flat)

			if room_formset.is_valid():
				room_num = 0
				averagePrice = 0

				for room_form in room_formset:
					size = room_form.cleaned_data.get('size')
					price = room_form.cleaned_data.get('price')
					averagePrice += price
					room_num += 1

					if size and price:
						Room.objects.create(flat=flat, roomNumber=room_num, size=size, price=price)

				averagePrice = averagePrice / room_num
				flat.averageRoomPrice = averagePrice
				flat.numberOfRooms = room_num
				flat.availableRooms = room_num
				flat.save()

			return redirect('show_property', flat_id_slug=flat.slug)
		else:
			print(flat_form.errors)
	else:
		flat_form = AddFlatForm()
	return render(request, 'flntr/add_flat.html', {'flat_form':flat_form, 'image_form':image_form, 'room_formset':room_formset})


def send_request(request, flat_id_slug, room_number):

	request_form = RequestForm()

	params = request.get_full_path().split('/')
	flat = Flat.objects.get(slug=params[3])
	room = Room.objects.get(flat=flat, roomNumber=params[5])

	student = StudentProfile.objects.get(user=request.user)

	try:
		hasRequested = Request.objects.get(student=student)
		return render(request, 'flntr/request_sent.html', {'has_requested':True})
	except Request.DoesNotExist:
		pass

	if request.method== 'POST':
		request_form=RequestForm(request.POST)
		if request_form.is_valid():
			flat = Flat.objects.get(slug=flat_id_slug)
			room = Room.objects.get(flat=flat, roomNumber=room_number)
			#student = request.user
			#student = User.objects.get(username='n.nilsson@gmail.com')
			student = StudentProfile.objects.get(user=request.user)
			landlord = flat.owner
			message = request_form.cleaned_data.get('message')

			Request.objects.create(room=room, student=student, landlord=landlord, message=message)

			return render(request, 'flntr/request_sent.html', {'has_requested':False})

	return render(request, 'flntr/send_request.html', {'request_form':request_form, 'flat':flat, 'room':room})


#def edit_flat(request):
#def is_full(flat_slug):
#	flat = Flat.objects.get(slug=flat_slug)
#	rooms = Room.objects.all.filter(flat=flat, student__isnull=True)
#	if rooms.len() > 0:
#		return False
#	else:
#		return True
