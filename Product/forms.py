from django import forms
from Branch.models import Branch

from Product.models import  Category, Foot_Wear, Product, Product_Type, Size, Suit, Top

class CategoryForm(forms.ModelForm):
    """Form definition for Category."""

    class Meta:
        """Meta definition for Categoryform."""

        model = Category
        fields = '__all__'
        

class SizeForm(forms.ModelForm):
    """Form definition for Size."""

    class Meta:
        """Meta definition for Sizeform."""

        model = Size
        fields = '__all__'

        
class ProductTypeForm(forms.ModelForm):
    """Form definition for Product_Type."""

    class Meta:
        """Meta definition for Product_Typeform."""

        model = Product_Type
        fields = '__all__'
        
class ProductForm(forms.ModelForm):
    """Form definition for Product."""
    sizes = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                queryset=Size.objects.all(),required=False)
    
    class Meta:
        """Meta definition for Productform."""

        model = Product
        fields = '__all__'
        
class SuitForm(forms.ModelForm):
    """Form definition for Suit."""
    sizes = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                queryset=Size.objects.all(),
                                                required=False)
    
    class Meta:
        """Meta definition for Suitform."""

        model = Suit
        fields = '__all__'
        
class TopForm(forms.ModelForm):
    """Form definition for Top."""
    sizes = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                queryset=Size.objects.all(),required=False)
    
    class Meta:
        """Meta definition for Topform."""

        model = Top
        fields = '__all__'
    
class FootWearForm(forms.ModelForm):
    """Form definition for FootWear."""
    sizes = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                queryset=Size.objects.all(),required=False)
    
    class Meta:
        """Meta definition for FootWearform."""

        model = Foot_Wear
        fields = '__all__'

