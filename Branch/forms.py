from django import forms
from Branch.models import (Branch, Branch_Product, Branch_Suit, 
                           Branch_Tops, Product_Size, Suit_Size, Tops_Size)

class BranchForm(forms.ModelForm):
                            
    class Meta:
        model = Branch
        fields = '__all__'
        
class BranchProductForm(forms.ModelForm):
    """Form definition for BranchProduct."""

    class Meta:
        """Meta definition for BranchProductform."""

        model = Branch_Product
        fields = '__all__'

        
class BranchSuitForm(forms.ModelForm):
    """Form definition for BranchSuit."""

    class Meta:
        """Meta definition for BranchSuitform."""

        model = Branch_Suit
        fields = '__all__'
  
        
class BranchTopsForm(forms.ModelForm):
    """Form definition for BranchTops."""

    class Meta:
        """Meta definition for BranchTopsform."""

        model = Branch_Tops
        fields = '__all__'
        
class ProductSizeForm(forms.ModelForm):
    """Form definition for ProductSize."""

    class Meta:
        """Meta definition for ProductSizeform."""

        model = Product_Size
        fields = '__all__'
        
class TopsSizeForm(forms.ModelForm):
    """Form definition for TopsSize."""

    class Meta:
        """Meta definition for TopsSizeform."""

        model = Tops_Size
        fields = '__all__'
        
class SuitSizeForm(forms.ModelForm):
    """Form definition for SuitSize."""

    class Meta:
        """Meta definition for SuitSizeform."""

        model = Suit_Size
        fields = '__all__'
