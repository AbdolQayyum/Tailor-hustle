from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from authentication.forms import UserForm, CustomUserChangeForm
from .models import *

# Register your models here.

User = get_user_model()


# ModelAdmin

class CustomUserAdmin(UserAdmin):
    add_form = UserForm
    form = CustomUserChangeForm
    model = User
    add_fieldsets = (
        ('Personal Details', {'fields': ('email', 'full_name', 'first_name', 'last_name', 'username', 'user_type',
                                         'phone_number', 'email_verified', 'claimed', 'picture', 'password1',
                                         'password2')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    fieldsets = (
        ('Personal Details', {'fields': ('email', 'full_name', 'first_name', 'last_name', 'username', 'user_type',
                                         'phone_number', 'email_verified', 'claimed', 'picture', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(FriendRequest)
admin.site.register(Follow)
admin.site.register(Notification)
