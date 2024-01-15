from django import forms

from Bad_Product.models import Bad_Product, Bad_Suit, Bad_Top

class BadProductForm(forms.ModelForm):
    """Form definition for BadProduct."""
    class Meta:
        """Meta definition for BadProductform."""

        model = Bad_Product
        fields = '__all__'
        
class BadSuitForm(forms.ModelForm):
    """Form definition for BadSuit."""

    class Meta:
        """Meta definition for BadSuitform."""

        model = Bad_Suit
        fields = '__all__'
        
class BadTopForm(forms.ModelForm):
    """Form definition for BadTop."""

    class Meta:
        """Meta definition for BadTopform."""

        model = Bad_Top
        fields = '__all__'
