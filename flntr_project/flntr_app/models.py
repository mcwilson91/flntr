from django.db import models

#class FlntrUser(models.Model):
#	fname = models.CharField(max_length=32)
#	sname = models.CharField(max_length=32)
#	email = models.CharField(max_length=64)
#
#	def __str__(self):
#			return self.fname + ' ' + self.sname


class Student(models.Model):
	fname = models.CharField(max_length=32)
	sname = models.CharField(max_length=32)
	email = models.CharField(max_length=64)

	def __str__(self):
			return self.fname + ' ' + self.sname

class Landlord(models.Model):
	fname = models.CharField(max_length=32)
	sname = models.CharField(max_length=32)
	email = models.CharField(max_length=64)

	def __str__(self):
			return self.fname + ' ' + self.sname

class Room(models.Model):
	owner = models.ForeignKey(Landlord)
	location = models.CharField(max_length=64)
	price = models.DecimalField(max_digits=6, decimal_places=2)

	def __str__(self):
		return self.location

class StudentProfile(models.Model):
	student = models.OneToOneField(Student, on_delete=models.CASCADE,)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	bio = models.TextField(blank=True)

	def __str__(self):
		return self.student.fname

class RoomDescription(models.Model):
	room = models.OneToOneField(Room, on_delete=models.CASCADE,)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.room.location
