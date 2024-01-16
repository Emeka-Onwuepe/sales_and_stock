from django import forms

from Stock.models import Foot_Wear_Stock, Product_Stock,Suit_Stock,Tops_Stock


class ProductStockForm(forms.ModelForm):
    """Form definition for ProductStock."""

    class Meta:
        """Meta definition for ProductStockform."""

        model = Product_Stock
        fields = '__all__'
        
class SuitStockForm(forms.ModelForm):
    """Form definition for SuitStock."""

    class Meta:
        """Meta definition for SuitStockform."""

        model = Suit_Stock
        fields ='__all__'
        
class TopsStockForm(forms.ModelForm):
    """Form definition for TopsStock."""

    class Meta:
        """Meta definition for TopsStockform."""

        model = Tops_Stock
        fields ='__all__'
        
class FootWearStockForm(forms.ModelForm):
    """Form definition for FootWearStockForm."""

    class Meta:
        """Meta definition for FootWearStockForm."""

        model = Foot_Wear_Stock
        fields ='__all__'
