from django.contrib import admin
from .models import Category, Subcategory, ShopItem, Cart, CartItem, Order, OrderItem

# Register your models here.

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(ShopItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
