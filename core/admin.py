from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from . import models 

# Register your models here.

from .models import State

admin.site.register(State)

#class CustomUserAdmin(UserAdmin):
