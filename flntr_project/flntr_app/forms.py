from django import forms
from django.contrib.auth.models import User, Group
from flntr_app.models import Flat, FlatImage, StudentProfile





class AddFlatForm(forms.ModelForm):
	streetAddress = forms.CharField(help_text="Please enter the adress of the room")
	title =  forms.CharField(help_text="Please enter a brief description of the room")
	postCode = forms.CharField()
	numberOfRooms = forms.IntegerField()
	description = forms.CharField(widget=forms.Textarea)
	price = forms.DecimalField(max_digits=6, decimal_places=2)

	class Meta:
		model = Flat
		fields = ('streetAddress', 'title', 'postCode', 'numberOfRooms', 'description', 'price')

class AddFlatImageForm(forms.ModelForm):
	class Meta:
		model = FlatImage
		fields = ('image',)

class FlatSearchForm(forms.Form):

	min_price_options = [ (0, '<100'), (100, '100'), (200, '200'), (300, '300'), (400, '400'), (500, '500'), (600, '600'), (700, '700'), (800, '800') ]
	max_price_options = [ (100, '100'), (100, '100'), (200, '200'), (300, '300'), (400, '400'), (500, '500'), (600, '600'), (700, '700'), (9999, '800+') ]
	min_price = forms.CharField(label='Min price', widget=forms.Select(choices=min_price_options))
	max_price = forms.CharField(label='Max price', widget=forms.Select(choices=max_price_options))

	min_room_options = [ (1, '1'), (2, '2'), (3, '3'), (4, '4') ]
	min_rooms = forms.CharField(label='Min number of rooms', widget=forms.Select(choices=min_room_options))

	max_room_options = [ (1, '1'), (2, '2'), (3, '3'), (99, '4+') ]
	max_rooms = forms.CharField(label='Max number of rooms', widget=forms.Select(choices=max_room_options))

	distance_options = [ (800, '0.5'), (1600, '1'), (2400, '1.5'), (3200, '2'), (3, '3'), (4800, '4'), (500000, '5+') ]
	distance = forms.CharField(label='Max distance from University', widget=forms.Select(choices=distance_options))

	date_options = [ (1, 'today'), (7, 'this week'), (30, 'this month'), (999, 'all') ]
	date = forms.CharField(label='date added', widget=forms.Select(choices=date_options))

class RoommateSearchForm(forms.Form):
	age_options=[ ( 1 ,'Don\'t mind'), (2,'Similar Age')]
	age = forms.ChoiceField(choices=age_options, widget=forms.RadioSelect())

	gender_options =[ ( 1 ,'Don\'t mind'), (2,'Same Gender') ]
	gender = forms.ChoiceField(choices=gender_options, widget=forms.RadioSelect())


class UserForm(forms.ModelForm):
	password = forms.CharField(min_length=6, widget=forms.PasswordInput())
	group_options = [ (1, 'Student'), (1, 'Landlord') ]
	groups = forms.ChoiceField(label='I am a ', choices=group_options, widget=forms.RadioSelect())

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'username', 'email', 'groups', 'password')

class AgeForm(forms.ModelForm):
	age  = forms.ChoiceField(choices=[(x, x) for x in range(16, 99)])

	gender_options = [ (1, 'Female'), (2, 'Male'), (3, 'Other') ]
	gender = forms.ChoiceField(label='Gender', choices=gender_options, widget=forms.RadioSelect())
	class Meta:
		model = StudentProfile
		fields = ('age', 'gender',)


class ProfileForm(forms.ModelForm):
	class Meta:
		model = StudentProfile
		fields = ('bio', 'picture')
