import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flntr_project.settings')

import django
django.setup()
from flntr_app.models import Student, Landlord, Room, StudentProfile, RoomDescription

def populate():
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
		"rooms": [{ "location": "123 Byres Road", "price": 123.45}, {"location": "456 Dumbarton Road", "price": 678.90}]
		}]
				
	for s in students:
		add_student(s['fname'], s['sname'], s['email'])
	
	for l in landlords:
		owner = add_landlord(l['fname'], l['sname'], l['email'])
		for r in l['rooms']:
			add_room(owner, r['location'], r['price'])
		
		
		
def add_student(fname, sname, email):
	s = Student.objects.get_or_create(fname=fname, sname=sname, email=email)[0]
	s.save()
	p = StudentProfile.objects.get_or_create(student=s)[0]
	p.save()
	print(fname, sname, email)
	
def add_landlord(fname, sname, email):
	l = Landlord.objects.get_or_create(fname=fname, sname=sname, email=email)[0]
	l.save()
	return l;
	print(fname, sname, email)
	
def add_room(owner, location, price):
	r = Room.objects.get_or_create(owner=owner, location=location,price=price)[0]
	r.save()
	d = RoomDescription.objects.get_or_create(room=r)[0]
	d.save()
	print(owner, location, price)

if __name__ == '__main__':
	print('populating')
	populate()