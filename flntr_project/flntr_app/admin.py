from django.contrib import admin
from flntr_app.models import Student, Landlord, Room, StudentProfile, RoomDescription


admin.site.register(Student)
admin.site.register(Landlord)
admin.site.register(Room)
admin.site.register(StudentProfile)
admin.site.register(RoomDescription)