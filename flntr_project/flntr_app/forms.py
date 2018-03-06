from django import forms
from django.contrib.auth.models import User, Group
from flntr_app.models import Flat, FlatImage, StudentProfile





class FlatForm(forms.ModelForm):
	streetAddress = forms.CharField(help_text="Please enter the adress of the room")
	title =  forms.CharField(help_text="Please enter a brief description of the room")
	postCode = forms.CharField()
	numberOfRooms = forms.IntegerField()
	description = forms.CharField(widget=forms.Textarea)
	price = forms.DecimalField(max_digits=6, decimal_places=2)

	class Meta:
		model = Flat
		fields = ('streetAddress', 'title', 'postCode', 'numberOfRooms', 'description', 'price')


class FlatSearchForm(forms.Form):

	min_price_options = [ (0, '<100'), (100, '100'), (200, '200'), (300, '300'), (400, '400'), (500, '500'), (600, '600'), (700, '700'), (800, '800') ]
	max_price_options = [ (0, '<100'), (100, '100'), (200, '200'), (300, '300'), (400, '400'), (500, '500'), (600, '600'), (700, '700'), (9999, '800+') ]
	min_price = forms.CharField(label='Min price', widget=forms.Select(choices=min_price_options))
	max_price = forms.CharField(label='Max price', widget=forms.Select(choices=max_price_options))

	min_room_options = [ (1, '1'), (2, '2'), (3, '3'), (4, '4') ]
	min_rooms = forms.CharField(label='Min number of rooms', widget=forms.Select(choices=min_room_options))

	max_room_options = [ (1, '1'), (2, '2'), (3, '3'), (99, '4+') ]
	max_rooms = forms.CharField(label='Max number of rooms', widget=forms.Select(choices=max_room_options))

	distance_options = [ (0.5, '0.5'), (1, '1'), (1.5, '1.5'), (2, '2'), (3, '3'), (4, '4'), (5, '5+') ]
	distance = forms.CharField(label='Max distance from University', widget=forms.Select(choices=distance_options))

	date_options = [ (1, 'past hour'), (2, 'today'), (3, 'this week'), (4, 'this month'), (5, 'all') ]
	date = forms.CharField(label='date added', widget=forms.Select(choices=date_options))

class RoommateSearchForm(forms.Form):
	age_options=[ ( 1 ,'Don\'t mind'), (2,'Similar Age')]
	age = forms.ChoiceField(choices=age_options, widget=forms.RadioSelect())

	gender_options =[ ( 1 ,'Don\'t mind'), (2,'Same Gender') ]
	gender = forms.ChoiceField(choices=gender_options, widget=forms.RadioSelect())

class RegistrationForm(forms.Form):
	username = forms.CharField(help_text='Username')
	first_name = forms.CharField(help_text='First Name')
	last_name = forms.CharField(help_text='Last Name')
	age  = forms.ChoiceField(choices=[(x, x) for x in range(16, 99)])
	group_options = [ (1, 'Student'), (2, 'Landlord')]
	groups = forms.ChoiceField(choices=group_options, widget=forms.RadioSelect())
	email = forms.CharField(help_text='Email')
	password = forms.CharField(help_text='Password')
