from django.db import models
from django.contrib.auth.models import User, Group
from django.template.defaultfilters import slugify
from datetime import datetime

class Landlord(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,)
	slug = models.SlugField(unique=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.user.first_name + " " + self.user.last_name)
		super(Landlord, self).save(*args, **kwargs)

	def __str__(self):
		return self.user.username

class Flat(models.Model):
	owner = models.ForeignKey(Landlord)
	title = models.CharField(max_length=250)
	numberOfRooms = models.IntegerField(default=0)
	availableRooms = models.IntegerField(default=0)
	streetAddress = models.CharField(max_length=64)
	postCode = models.CharField(max_length=8)
	description = models.TextField(blank=True)
	averageRoomPrice = models.DecimalField(max_digits=6, decimal_places=2, null=True)
	slug = models.SlugField(unique=True)
	dayAdded = models.DateTimeField(default=datetime.now)
	views = models.IntegerField(default=0)
	distanceFromUniversity = models.IntegerField(default = 0)
	distanceText = models.CharField(max_length=8, default = "0 mi")

	def save(self, *args, **kwargs):
		self.slug = slugify(self.streetAddress)
		super(Flat, self).save(*args, **kwargs)
	def __str__(self):
		return self.title

class StudentProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	bio = models.TextField(blank=True)
	properties = models.ForeignKey(Flat, null=True, blank=True)
	age = models.IntegerField(default=0)
	gender = models.CharField(max_length=10)
	slug = models.SlugField(unique=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.user.first_name + " " + self.user.last_name)
		super(StudentProfile, self).save(*args, **kwargs)

	def __str__(self):
		return self.user.username

class Room(models.Model):
	flat = models.ForeignKey(Flat)
	roomNumber = models.IntegerField()
	size = models.CharField(max_length=8)
	price = models.DecimalField(max_digits=9, decimal_places=2)
	student = models.OneToOneField(StudentProfile, null=True, blank=True)

	def __str__(self):
		return "%s %s" % (self.flat.title, self.roomNumber)

class FlatImage(models.Model):
	flat = models.ForeignKey(Flat, related_name='images')
	imageNumber = models.IntegerField(default=0)
	image = models.ImageField(upload_to='flat_images', blank=True)
	
	def __str__(self):
		return "%s %s" % (self.flat.title, self.imageNumber)

class Request(models.Model):
	room = models.ForeignKey(Room)
	landlord = models.ForeignKey(Landlord, null=True, blank=True)
	student = models.OneToOneField(StudentProfile)
	message = models.TextField(blank=True)

	#def save(self):
	#	if not self.id:
	#		self.landlord = self.room.flat.owner
	#	super(Request, self).save()

	def __str__(self):
		return "%s %s" % (self.room, self.student)



