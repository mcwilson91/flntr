import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flntr_project.settings')

from django.core.files.images import ImageFile
import django
django.setup()
from flntr_app.models import Flat, StudentProfile, FlatImage, Landlord, Room
from flntr_project import settings
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
		{"fname": "Nils", "sname": "Nilsson", "email": "n.nilsson@gmail.com", "pictureName": "nils-nilsson.png" , "bio": description, "age": 19, "gender": "Male"},
		{"fname": "Rosebud", "sname": "Forsyth", "email": "rosef@gmail.com", "pictureName": "rosebud-forsyth.png", "bio": description, "age": 24, "gender": "Female"}]

	images = [{ "imagename": "Kelvingrove-Art-Gallery-and-Museum.jpg"}, {"imagename": "Kelvingrove-Art-Gallery-2.jpg"}]

	rooms1 = [
		{"size": "double", "price": 123.45}, {"size": "single", "price": 123.45}]

	rooms2 = [
		{"size": "double", "price": 678.90}, {"size": "double", "price": 678.90}, {"size": "single", "price": 678.90}]

	rooms3 = [
		{"size": "double", "price": 445.00}, {"size": "double", "price": 445.00}, {"size": "single", "price": 445.00}]

	rooms4 = [
		{"size": "double", "price": 760.00}, {"size": "single", "price": 760.00}]

	rooms5 = [
		{"size": "double", "price": 400.00}, {"size": "single", "price": 400.00}]

	rooms6 = [
		{"size": "double", "price": 890.50}, {"size": "single", "price": 890.50}, {"size": "double", "price": 890.50}, {"size": "double", "price": 890.50}, {"size": "single", "price": 890.50}]

	rooms7 = [
		{"size": "double", "price": 459.00}, {"size": "double", "price": 459.00}, {"size": "single", "price": 459.00}]

	rooms8 = [
		{"size": "double", "price": 950.32}, {"size": "double", "price": 950.32}, {"size": "single", "price": 950.32}, {"size": "double", "price": 950.32}, {"size": "single", "price": 950.32},
		{"size": "double", "price": 950.32}, {"size": "double", "price": 950.32}, {"size": "single", "price": 950.32}, {"size": "double", "price": 950.32}, {"size": "single", "price": 950.32},
		{"size": "double", "price": 950.32}, {"size": "double", "price": 950.32}, {"size": "single", "price": 950.32}, {"size": "double", "price": 950.32}, {"size": "single", "price": 950.32},
		{"size": "double", "price": 950.32}, {"size": "double", "price": 950.32}, {"size": "single", "price": 950.32}, {"size": "double", "price": 950.32}, {"size": "single", "price": 950.32}]


	flats1 = [
		{"address": "123 Byres Road", "averageRoomPrice": 123.45, "numberOfRooms": 2, "postcode": "G12 8TT", "description": description, "title": "A quaint 2 bedroom abode in the heart of Glasgow's west end", "distance": 174, "distanceText": "0.1 mi", "rooms": rooms1, "images": None},
		{"address": "456 Dumbarton Road", "averageRoomPrice": 678.90, "numberOfRooms": 3, "postcode": "G11 6SQ", "description": description, "title": "A dilapidated shack", "distance": 1526, "distanceText": "0.9 mi", "rooms": rooms2, "images": None},
		{"address": "25 Great George Street", "averageRoomPrice": 445.00, "numberOfRooms": 3, "postcode": "G12 8LN", "description": description, "title": "Spacious 3 bedroom flat near Glasgow University", "distance": 560, "distanceText": "0.3 mi", "rooms": rooms3, "images": None},
		{"address": "101 Great Western Road", "averageRoomPrice": 760.00, "numberOfRooms": 2, "postcode": "G4 9AH", "description": description, "title": "Recently Refurbished 2 bedroom flat", "distance": 2205, "distanceText": "1.4 mi", "rooms": rooms4, "images": None}]
		
	flats2 = [
		{"address": "168 Great George Street", "averageRoomPrice": 400.00, "numberOfRooms": 2, "postcode": "G12 8AJ", "description": description, "title": "Traditional two bedroom apartment", "distance": 278, "distanceText": "0.2 mi", "rooms": rooms5, "images": None},
		{"address": "9 Turnberry Road", "averageRoomPrice": 890.50, "numberOfRooms": 5, "postcode": "G11 5AG", "description": description, "title": "Spacious five bedroom tenement flat", "distance": 765, "distanceText": "0.5 mi", "rooms": rooms6, "images": None},
		{"address": "38 Clarence Drive", "averageRoomPrice": 459.00, "numberOfRooms": 3, "postcode": "G12 9TQ", "description": description, "title": "Commanding 3 bedroom, red sandstone tenement flat", "distance": 1077, "distanceText": "0.7 mi", "rooms": rooms7, "images": None},
		{"address": "Kelvingrove Art Gallery and Museum", "averageRoomPrice": 950.32, "numberOfRooms": 20, "postcode": "G3 8AG", "description": description, "title": "40 bedroom Neo-Gothic mansion (beware of dinosarurs)", "distance": 914, "distanceText": "0.6 mi", "rooms": rooms8, "images": images}]
		
	landlords = [
		{
		"fname": "Willie",
		"sname": "McSporran",
		"email": "willie.mcsporran@yahoo.com",
		"flats": flats1
		},
		{
		"fname": "Ebenezer",
		"sname": "Scrooge",
		"email": "scrooge@humbug.com",
		"flats": flats2
		}]
		
		
	for k in groups:
		add_groups(k['name'])

	for s in students:
		add_student(s['fname'], s['sname'], s['email'], s['pictureName'], s['bio'], s['age'], s['gender'])

	for l in landlords:
		owner = add_landlord(l['fname'], l['sname'], l['email'])
		for f in l['flats']:
			flat = add_flat(owner, f['address'], f['averageRoomPrice'], f['postcode'], f['numberOfRooms'], f['description'], f['title'], f['distance'], f['distanceText'])
			if (f['images'] != None):
				i = 1
				for fi in f['images']:
					add_flat_image(flat, i, fi['imagename'])
					i = i + 1
			i = 1
			for r in f['rooms']:
				add_room(flat, i, r['size'], r['price'])
				i = i + 1
	

def add_groups(name):
	k = Group.objects.get_or_create(name= name)[0]
	k.save()
	print(name)

def add_student(fname, sname, email, pictureName, bio, age, gender):
	s = User.objects.get_or_create(username = email, first_name=fname, last_name=sname, email=email)[0]
	s.set_password("piaudwefhpdf")
	g = Group.objects.get(name='students')
	g.user_set.add(s)
	s.save()
	p = StudentProfile.objects.get_or_create(user=s, bio=bio, age=age, gender=gender)[0]
	file = open("%s/%s" % (settings.MEDIA_ROOT, pictureName), 'rb')
	p.picture.save(pictureName, file, save=False)
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

def add_flat(owner, location, averageRoomPrice, postcode, numberOfRooms, description, title, distance, distanceText):
	f = Flat.objects.get_or_create(owner=owner, streetAddress=location, averageRoomPrice=averageRoomPrice, postCode=postcode, numberOfRooms=numberOfRooms, description=description, title=title, distanceFromUniversity=distance, distanceText=distanceText)[0]
	f.save()
	#d = RoomDescription.objects.get_or_create(room=r)[0]
	#d.save()
	print(owner, location, averageRoomPrice)
	return f;

def add_flat_image(flat, imageNumber, imagename):
	fi = FlatImage.objects.get_or_create(flat=flat, imageNumber=imageNumber)[0]
	file = open("%s/%s" % (settings.MEDIA_ROOT, imagename), 'rb')
	fi.image.save(imagename, file, save=False)
	fi.save()

def add_room(flat, roomNumber, size, price):
	r = Room.objects.get_or_create(flat=flat, roomNumber=roomNumber, size=size, price=price)[0]
	r.save()
	print(flat, size)

if __name__ == '__main__':
	print('populating')
	populate()
	print('creating superuser')
	User.objects.create_superuser(username='superuser', password='superuser', email='')
