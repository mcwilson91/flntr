from django.contrib import admin
from flntr_app.models import Flat, FlatImage, StudentProfile

# class FlatAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug':('title',)}

admin.site.register(Flat)
admin.site.register(StudentProfile)
