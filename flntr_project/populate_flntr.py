import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flntr_project.settings')

import django
django.setup()
from flntr_app.models import Flat, StudentProfile, FlatImage, Landlord
from django.contrib.auth.models import User, Group

description = "In publishing and graphic design, lorem ipsum is a filler text or greeking commonly used to demonstrate the textual elements of a graphic document or visual presentation. Replacing meaningful content with placeholder text allows designers to design the form of the content before the content itself has been produced."

def populate():
	groups = [
		{
		"name": "students"
		},
		{
		"name": "landlords"
		}
	]

	students = [
		{
		"fname": "Nils",
		"sname": "Nilsson",
		"email": "n.nilsson@gmail.com"
		},
		{
		"fname": "Rosebud",
		"sname": "Forsyth",
		"email": "rosef@gmail.com"
		}]

	landlords = [
		{
		"fname": "Willie",
		"sname": "McSporran",
		"email": "willie.mcsporran@yahoo.com",
		"rooms": [
		{"address": "123 Byres Road", "price": 123.45, "rooms": 2, "postcode": "G12 8TT", "description": description, "title": "A quaint 2 bedroom abode in the heart of Glasgow's west end"},
		{"address": "456 Dumbarton Road", "price": 678.90, "rooms": 3, "postcode": "G81 4DR", "description": description, "title": "A dilapidated shack"}]
		}]

	for k in groups:
		add_groups(k['name'])

	for s in students:
		add_student(s['fname'], s['sname'], s['email'])

	for l in landlords:
		owner = add_landlord(l['fname'], l['sname'], l['email'])
		for r in l['rooms']:
			add_room(owner, r['address'], r['price'], r['postcode'], r['rooms'], r['description'], r['title'])

	

def add_groups(name):
	k = Group.objects.get_or_create(name= name)[0]
	k.save()
	print(name)

def add_student(fname, sname, email):
	s = User.objects.get_or_create(username = email, first_name=fname, last_name=sname, email=email)[0]
	s.set_password("piaudwefhpdf")
	g = Group.objects.get(name='students')
	g.user_set.add(s)
	s.save()
	p = StudentProfile.objects.get_or_create(user=s)[0]
	p.save()
	print(fname, sname, email)

def add_landlord(fname, sname, email):
	l = User.objects.get_or_create(username = email, first_name=fname, last_name=sname, email=email)[0]
	l.set_password("piaudwefhpdf")
	g = Group.objects.get(name='landlords')
	g.user_set.add(l)
	l.save()
	p = Landlord.objects.get_or_create(user=l)[0]
	p.save()
	print(fname, sname, email)
	return l;

def add_room(owner, location, price, postcode, rooms, description, title):
	r = Flat.objects.get_or_create(owner=owner, streetAddress=location, price=price, postCode=postcode, numberOfRooms=rooms, description=description, title=title)[0]
	r.save()
	#d = RoomDescription.objects.get_or_create(room=r)[0]
	#d.save()
	print(owner, location, price)

if __name__ == '__main__':
	print('populating')
	populate()
