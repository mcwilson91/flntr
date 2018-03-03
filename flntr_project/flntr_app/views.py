from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from flntr_app.models import Flat, FlatImage, StudentProfile
from flntr_app.forms import FlatForm, FlatSearchForm, RoommateSearchForm
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    top_property_list = Flat.objects.order_by('-price')[:5]
    context_dict = {'topproperties': top_property_list}
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
			params = {'min_price': min_price, 'max_price':max_price, 'min_rooms':min_rooms, 'max_rooms':max_rooms}
			return results(request, params)
	return render(request, 'flntr/search.html', {'search_form':search_form, 'roommate_form':roommate_form})

def results(request, params):
	results = Flat.objects.filter(
						price__gte=params['min_price'], 
						price__lte=params['max_price'],
						numberOfRooms__gte=params['min_rooms'],
						numberOfRooms__lte=params['max_rooms'],)

	context_dict = {'results':results}
	return render(request, 'flntr/results.html', context_dict)
	
def register(request):
	return render(request, 'flntr/register.html')

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
    all_property_list = Flat.objects.order_by('-price')
    context_dict = {'allproperties': all_property_list}
    return render(request, 'flntr/property.html', context_dict)

def show_property(request, property_id_slug):
    context_dict = {}
    try:
        property = Flat.objects.get(slug=property_id_slug)
        context_dict['property'] = property
    except Flat.DoesNotExist:
        context_dict['property'] = None
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

def show_user_properties(request):
    return render(request, 'flntr/show_user_properties.html')

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
