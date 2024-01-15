from rest_framework import serializers

from Product.models import Product, Suit, Top


class SuitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suit
        # depth = 1
        exclude = ('description','date','image','publish')
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # depth = 1
        exclude = ('description','date','image','publish')
        
class TopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Top
        # depth = 1
        exclude = ('description','date','image','publish')