
from django.contrib import admin

from Branch.models import Branch, Branch_Product, Branch_Suit, Branch_Tops, Product_Size, Suit_Size, Tops_Size

# Register your models here.

admin.site.register(Branch)
admin.site.register(Branch_Product)
admin.site.register(Product_Size)
admin.site.register(Branch_Suit)
admin.site.register(Suit_Size)
admin.site.register(Branch_Tops)
admin.site.register(Tops_Size)