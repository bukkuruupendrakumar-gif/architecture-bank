from django.contrib import admin
from .models import Category, Design, Wishlist, Booking

admin.site.register(Category)
admin.site.register(Design)
admin.site.register(Wishlist)
admin.site.register(Booking)