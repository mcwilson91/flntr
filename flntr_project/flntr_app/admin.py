from django.contrib import admin
from flntr_app.models import Flat, FlatImage, StudentProfile, Landlord, Room, Request

class FlatAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}


admin.site.register(Flat, FlatAdmin)
admin.site.register(FlatImage)
admin.site.register(StudentProfile)
admin.site.register(Landlord)
admin.site.register(Room)
admin.site.register(Request)
