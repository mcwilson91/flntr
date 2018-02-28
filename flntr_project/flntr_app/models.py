from django.db import models
from django.contrib.auth.models import User, Group
from django.template.defaultfilters import slugify
from datetime import datetime


class Flat(models.Model):
	owner = models.ForeignKey(User)
	title = models.CharField(max_length=250)
	numberOfRooms = models.IntegerField()
	streetAddress = models.CharField(max_length=64)
	postCode = models.CharField(max_length=8)
	# picture = models.ImageField(upload_to='flat_images', blank=True)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	slug = models.SlugField(unique=True)
	dayAdded = models.DateField(default=datetime.now)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.streetAddress)
		super(Flat, self).save(*args, **kwargs)
	def __str__(self):
		return self.title

class FlatImage(models.Model):
	flat = models.ForeignKey(Flat, related_name='images')
	image = models.ImageField(upload_to='flat_images', blank=True)
	def __str__(self):
		return self.flat.title

class StudentProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	bio = models.TextField(blank=True)
	properties = models.ForeignKey(Flat, null=True, blank=True)
	def __str__(self):
		return self.user.fname
