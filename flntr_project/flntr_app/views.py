from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from flntr_app.models import Flat, FlatImage, StudentProfile, Landlord
from flntr_app.forms import FlatForm, FlatSearchForm, RoommateSearchForm, RegistrationForm
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# Create your views here.
def index(request):
    recent_flat_list = Flat.objects.order_by('-price')[:3]
    context_dict = {'recentflats': recent_flat_list}
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
			params = {'min_price': min_price, 'max_price':max_price, 'min_rooms':min_rooms, 'max_rooms':max_rooms, 'date_added':date_added}
			return results(request, params)
	return render(request, 'flntr/search.html', {'search_form':search_form, 'roommate_form':roommate_form})

def results(request, params):
	
	results = Flat.objects.filter(
						price__gte=params['min_price'],
						price__lte=params['max_price'],
						numberOfRooms__gte=params['min_rooms'],
						numberOfRooms__lte=params['max_rooms'],
						dayAdded__gte=datetime.now() - timedelta(days=int(params['date_added'])),)
	

	context_dict = {'results':results}
	return render(request, 'flntr/results.html', context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = RegistrationForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
    else:
            user_form = RegistrationForm()

    return render(request, 'flntr/register.html',
                    {'user_form': user_form,
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
            print("Invalid login details: {0}, {1}").format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'flntr/login.html')

def property(request):
    all_flat_list = Flat.objects.order_by('-price')
    context_dict = {'allflats': all_flat_list}
    return render(request, 'flntr/property.html', context_dict)

def show_property(request, flat_id_slug):
    context_dict = {}
    try:
        flat = Flat.objects.get(slug=flat_id_slug)
        context_dict['flat'] = flat
    except Flat.DoesNotExist:
        context_dict['flat'] = None
    return render(request, 'flntr/show_property.html', context_dict)


def user(request):
    return render(request, 'flntr/user.html')

def show_user(request):
    return render(request, 'flntr/show_user.html')

def show_user_invitations(request):
    return render(request, 'flntr/show_user_invitations.html')

def show_user_requests(request):
    return render(request, 'flntr/show_user_requests.html')

def show_user_account(request):
    return render(request, 'flntr/show_user_account.html')

def show_user_profile(request):
    return render(request, 'flntr/show_user_profile.html')

def show_user_properties(request, landlord_id_slug):
    context_dict = {}
    landlord = Landlord.objects.get(slug=landlord_id_slug)
    context_dict['landlordname'] = landlord.user.first_name + " " + landlord.user.last_name
    landlord_flat_list = Flat.objects.filter(owner=landlord).order_by('-dayAdded')
    context_dict['landlordflats'] = landlord_flat_list
    return render(request, 'flntr/show_user_properties.html', context_dict)

def show_user_properties_aProperty(request):
    return render(request, 'flntr/show_user_properties_aProperties.html')

def user_logout(request):
    return render(request, 'flntr/user_logout.html')

def add_room(request):
	form = FlatForm();
	if request.method == 'POST':
		room_form = FlatForm(data=request.POST)
		if room_form.is_valid():
			room = room_form.save(commit=False)
			room.owner = User.objects.get(username="willie.mcsporran@yahoo.com")
			room.save()
			return index(request)
		else:
			print(room_form.errors, description_form.errors)
	else:
		room_form = FlatForm()
	return render(request, 'flntr/add_room.html', {'room_form':room_form})
