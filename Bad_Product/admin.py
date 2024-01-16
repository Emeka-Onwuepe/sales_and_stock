from django.contrib import admin

from Bad_Product.models import Bad_Foot_Wear, Bad_Product, Bad_Suit, Bad_Top

# Register your models here.
admin.site.register(Bad_Product)
admin.site.register(Bad_Suit)
admin.site.register(Bad_Top)
admin.site.register(Bad_Foot_Wear)