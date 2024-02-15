from django.contrib import admin
from .models import Seller, UserProfile,User

admin.site.register(UserProfile)
admin.site.register(Seller)
# admin.site.register(WholeSeller)
admin.site.register(User)