from django.contrib import admin
from .models import Category, Product, Product_Type,  Size, Suit, Top

# Register your models here.
admin.site.register(Category)
admin.site.register(Product_Type)
admin.site.register(Product)
admin.site.register(Suit)
admin.site.register(Top)
# admin.site.register(Returned_Product)
admin.site.register(Size)





