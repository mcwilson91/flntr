from django.contrib import admin
from flntr_app.models import Student, Landlord, Room, StudentProfile, RoomDescription

class RoomAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('location',)}

admin.site.register(Student)
admin.site.register(Landlord)
admin.site.register(Room, RoomAdmin)
admin.site.register(StudentProfile)
admin.site.register(RoomDescription)