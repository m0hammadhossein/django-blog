from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserForm, CustomUserChangeForm
from accounts.models import CustomUser


@admin.register(CustomUser)
class CustomeUserAdmin(UserAdmin):
    add_form = CustomUserForm
    form = CustomUserChangeForm

    add_fieldsets = UserAdmin.add_fieldsets + (('Profile', {'fields': ('avatar', 'biography')}),)
    fieldsets = UserAdmin.fieldsets + (('Profile', {'fields': ('avatar', 'biography')}),)
