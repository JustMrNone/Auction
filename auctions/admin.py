from django.contrib import admin
from .models import * 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('name', 'lastname', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
admin.site.register(bids)
admin.site.register(auction_listing)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Watchlist)
admin.site.register(Comment)
