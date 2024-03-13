'''
This file will be used to register models to the admin panel 
'''
from django.contrib import admin
from .models import *

# Register your models here so they can be edited in admin panel.
admin.site.register(Task)
admin.site.register(Profile)

