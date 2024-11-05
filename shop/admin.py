from .models import Product, Order, CartItem, UserProfile
from django.contrib import admin

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(UserProfile)