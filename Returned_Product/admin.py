from django.contrib import admin

from Returned_Product.models import (Returned_Foot_Wear, Returned_Product, 
                                     Returned_Suit, Returned_Top)

# Register your models here.
admin.site.register(Returned_Product)
admin.site.register(Returned_Suit)
admin.site.register(Returned_Top)
admin.site.register(Returned_Foot_Wear)