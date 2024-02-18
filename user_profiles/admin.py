from django.contrib import admin
from .models import Seller, UserProfile,User

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['email_or_phone','is_active',"is_seller"]
    list_filter = ["is_active",'is_seller']
    search_fields = ["is_seller"]
