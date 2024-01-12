from django import forms

from Stock.models import Product_Stock,Suit_Stock,Tops_Stock


class ProductStockForm(forms.ModelForm):
    """Form definition for ProductStock."""

    class Meta:
        """Meta definition for ProductStockform."""

        model = Product_Stock
        fields = '__all__'
        
class ProductStockEditForm(forms.ModelForm):
    """Form definition for ProductStockEdit."""
    
    class Meta:
        """Meta definition for ProductStockEditform."""

        model = Product_Stock
        fields = ['qty']
        
class SuitStockForm(forms.ModelForm):
    """Form definition for SuitStock."""

    class Meta:
        """Meta definition for SuitStockform."""

        model = Suit_Stock
        fields ='__all__'
        
class SuitStockEditForm(forms.ModelForm):
    """Form definition for SuitStockEdit."""
    
    class Meta:
        """Meta definition for SuitStockEditform."""

        model = Suit_Stock
        fields = ['qty']
        
class TopsStockForm(forms.ModelForm):
    """Form definition for TopsStock."""

    class Meta:
        """Meta definition for TopsStockform."""

        model = Tops_Stock
        fields ='__all__'
        
class TopsStockEditForm(forms.ModelForm):
    """Form definition for TopsStockEdit."""
    
    class Meta:
        """Meta definition for TopsStockEditform."""

        model = Tops_Stock
        fields = ['qty']