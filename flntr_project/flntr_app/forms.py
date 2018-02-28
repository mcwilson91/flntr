from django import forms
from django.contrib.auth.models import User
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
