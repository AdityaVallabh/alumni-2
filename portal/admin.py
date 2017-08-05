from django.contrib import admin

from .models import UserProfile, Address, Qualification, WorkExperience

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Address)
admin.site.register(Qualification)
admin.site.register(WorkExperience)
