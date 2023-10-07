from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Product,Cart,Order,OrderItem,CartItem,Category # Import your custom user model

# Register the CustomUser model with the admin site
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Category)