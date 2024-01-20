from rest_framework import serializers

from Product.models import (Foot_Wear, Product, Suit, 
                            Top,Category,Size,Product_Type)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # depth = 1
        exclude = ('image',)
        
class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        # depth = 1
        fields = '__all__'
        
class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Type
        # depth = 1
        fields = '__all__'

class SuitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suit
        # depth = 1
        exclude = ('date','image','publish')
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # depth = 1
        exclude = ('date','image','publish')
        
class TopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Top
        # depth = 1
        exclude = ('date','image','publish')
        
class FootWearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foot_Wear
        # depth = 1
        exclude = ('date','image','publish')