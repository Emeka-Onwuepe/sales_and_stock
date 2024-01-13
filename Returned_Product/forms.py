from django import forms

from Returned_Product.models import Returned_Product,Returned_Suit,Returned_Top


class ReturnedProductForm(forms.ModelForm):
    """Form definition for ReturnedProduct."""

    class Meta:
        """Meta definition for ReturnedProductform."""

        model = Returned_Product
        exclude =("product","size_instance")
        widgets = {
            "date_of_purchase" : forms.widgets.DateInput(attrs={'type':'date'}),
            "date_of_return"  : forms.widgets.DateInput(attrs={'type':'date'})     
        }
        
class ReturnedSuitForm(forms.ModelForm):
    """Form definition for ReturnedSuit."""

    class Meta:
        """Meta definition for ReturnedSuitform."""

        model = Returned_Suit
        exclude =("product","size_instance")
        widgets = {
            "date_of_purchase" : forms.widgets.DateInput(attrs={'type':'date'}),
            "date_of_return"  : forms.widgets.DateInput(attrs={'type':'date'})     
        }
        
class ReturnedTopForm(forms.ModelForm):
    """Form definition for ReturnedProduct."""

    class Meta:
        """Meta definition for ReturnedTopform."""

        model = Returned_Top
        exclude =("product","size_instance")
        widgets = {
            "date_of_purchase" : forms.widgets.DateInput(attrs={'type':'date'}),
            "date_of_return"  : forms.widgets.DateInput(attrs={'type':'date'})     
        }