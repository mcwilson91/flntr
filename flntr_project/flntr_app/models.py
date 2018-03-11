from django.db import models
from django.contrib.auth.models import User, Group
from django.template.defaultfilters import slugify
from datetime import datetime

class Landlord(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,)
	slug = models.SlugField()

	def save(self, *args, **kwargs):
		self.slug = slugify(self.user.first_name + " " + self.user.last_name)
		super(Landlord, self).save(*args, **kwargs)

	def __str__(self):
		return self.user.fname

class Flat(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE,)
	title = models.CharField(max_length=250)
	numberOfRooms = models.IntegerField()
	streetAddress = models.CharField(max_length=64)
	postCode = models.CharField(max_length=8)
	# picture = models.ImageField(upload_to='flat_images', blank=True)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	slug = models.SlugField(unique=True)
	dayAdded = models.DateField(default=datetime.now)
	views = models.IntegerField(default=0)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.streetAddress)
		super(Flat, self).save(*args, **kwargs)
	def __str__(self):
		return self.title

class FlatImage(models.Model):
	flat = models.ForeignKey(Flat, related_name='images', on_delete=models.CASCADE,)
	image = models.ImageField(upload_to='flat_images', blank=True)
	def __str__(self):
		return self.flat.title

class StudentProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	bio = models.TextField(blank=True)
	properties = models.ForeignKey(Flat, null=True, blank=True, on_delete=models.CASCADE,)
	age = models.IntegerField(default=0)
	gender = models.CharField(max_length=10)
	slug = models.SlugField()

	def save(self, *args, **kwargs):
		self.slug = slugify(self.user.first_name + " " + self.user.last_name)
		super(StudentProfile, self).save(*args, **kwargs)

	def __str__(self):
		return self.user.fname


