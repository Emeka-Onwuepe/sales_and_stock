from rest_framework import serializers
from Credit_Sales.models import Credit_Sale, Payment

from Sales.models import Items, Sales


class CreditSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit_Sale
        # depth = 1
        fields = '__all__'
        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        # depth = 1
        fields = '__all__'