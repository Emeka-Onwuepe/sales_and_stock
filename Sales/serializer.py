from rest_framework import serializers

from Sales.models import Items, Sales


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        # depth = 1
        fields = '__all__'
        
class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        # depth = 1
        fields = '__all__'