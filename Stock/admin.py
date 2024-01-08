from django.contrib import admin

from .models import  Product_Stock, Suit_Stock, Tops_Stock

# Register your models here.

admin.site.register(Product_Stock)
admin.site.register(Tops_Stock)
admin.site.register(Suit_Stock)
