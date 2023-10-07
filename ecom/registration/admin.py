# from django.contrib import admin
from django.contrib import admin
from .models import CustomUser  # Import your custom user model
# # Register your models here.



# Register the CustomUser model with the admin site
admin.site.register(CustomUser)

