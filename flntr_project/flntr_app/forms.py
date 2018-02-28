from django import forms
from flntr_app.models import Room, RoomDescription

class RoomForm(forms.ModelForm):
	location = forms.CharField(max_length=64)
	price = forms.DecimalField(max_digits=6, decimal_places=2)
	
	class Meta:
		model = Room
		fields = ('location', 'price',)
		
class RoomDescriptionForm(forms.ModelForm):
	class Meta:
		model = RoomDescription
		fields = ('description', 'picture')