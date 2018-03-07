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

	rooms1 = [
		{"address": "123 Byres Road", "price": 123.45, "rooms": 2, "postcode": "G12 8TT", "description": description, "title": "A quaint 2 bedroom abode in the heart of Glasgow's west end", "distance": 174, "distanceText": "0.1 mi"},
		{"address": "456 Dumbarton Road", "price": 678.90, "rooms": 3, "postcode": "G11 6SQ", "description": description, "title": "A dilapidated shack", "distance": 1526, "distanceText": "0.9 mi"},
		{"address": "25 Great George Street", "price": 445.00, "rooms": 3, "postcode": "G12 8LN", "description": description, "title": "Spacious 3 bedroom flat near Glasgow University", "distance": 560, "distanceText": "0.3 mi"},
		{"address": "101 Great Western Road", "price": 760.00, "rooms": 2, "postcode": "G4 9AH", "description": description, "title": "Recently Refurbished 2 bedroom flat", "distance": 2205, "distanceText": "1.4 mi"}]
		
	rooms2 = [
		{"address": "168 Great George Street", "price": 400.00, "rooms": 2, "postcode": "G12 8AJ", "description": description, "title": "Traditional two bedroom apartment", "distance": 278, "distanceText": "0.2 mi"},
		{"address": "9 Turnberry Road", "price": 890.50, "rooms": 5, "postcode": "G11 5AG", "description": description, "title": "Spacious five bedroom tenement flat", "distance": 765, "distanceText": "0.5 mi"},
		{"address": "38 Clarence Drive", "price": 459.00, "rooms": 3, "postcode": "G12 9TQ", "description": description, "title": "Commanding 3 bedroom, red sandstone tenement flat", "distance": 1077, "distanceText": "0.7 mi"},
		{"address": "Kelvingrove Art Gallery and Museum", "price": 9950.32, "rooms": 40, "postcode": "G3 8AG", "description": description, "title": "40 bedroom Neo-Gothic mansion (beware of dinosarurs)", "distance": 914, "distanceText": "0.6 mi"}]
		
	landlords = [
		{
		"fname": "Willie",
		"sname": "McSporran",
		"email": "willie.mcsporran@yahoo.com",
		"rooms": rooms1
		},
		{
		"fname": "Ebenezer",
		"sname": "Scrooge",
		"email": "scrooge@humbug.com",
		"rooms": rooms2
		}]
		
		
	for k in groups:
		add_groups(k['name'])

	for s in students:
		add_student(s['fname'], s['sname'], s['email'])

	for l in landlords:
		owner = add_landlord(l['fname'], l['sname'], l['email'])
		for r in l['rooms']:
			add_room(owner, r['address'], r['price'], r['postcode'], r['rooms'], r['description'], r['title'], r['distance'], r['distanceText'])

	

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
	return p;

def add_room(owner, location, price, postcode, rooms, description, title, distance, distanceText):
	r = Flat.objects.get_or_create(owner=owner, streetAddress=location, price=price, postCode=postcode, numberOfRooms=rooms, description=description, title=title, distanceFromUniversity=distance, distanceText=distanceText)[0]
	r.save()
	#d = RoomDescription.objects.get_or_create(room=r)[0]
	#d.save()
	print(owner, location, price)

if __name__ == '__main__':
	print('populating')
	populate()
	print('creating superuser')
	User.objects.create_superuser(username='superuser', password='superuser', email='')
