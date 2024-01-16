from django.db import models
from Branch.models import Branch

from Product.models import Foot_Wear, Product, Size, Suit, Top


# Create your models here.

class Returned_Product_Abstract(models.Model):
    """Model definition for Returned_Product_Abstract."""

    # TODO: Define fields here
    qty = models.IntegerField("qty",null=False,blank=False)
    unit_price = models.DecimalField("unit_price", max_digits=50, decimal_places=2,null=False,blank=False)
    total_price = models.DecimalField("total_price", max_digits=50, decimal_places=2,null=False,blank=False) 
    date_of_purchase = models.DateField("date_of_purchase", auto_now=False, auto_now_add=False,null=False,blank=False)
    date_of_return = models.DateTimeField("date_of_return", auto_now=False, auto_now_add=False,null=False,blank=False)

    class Meta:
        """Meta definition for Returned_Product_Abstract."""
        abstract = True

      

class Returned_Product(Returned_Product_Abstract):
    """Model definition for Returned_Product."""

    # TODO: Define fields here
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name = "returned_product_product_type")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="returned_product_branch")
    size_instance = models.ForeignKey(Size, verbose_name="size_instance", on_delete=models.CASCADE,
                        related_name="returned_product_size_instance",null=True, blank=True)

    class Meta:
        """Meta definition for Returned_Product."""

        verbose_name = 'Returned_Product'
        verbose_name_plural = 'Returned_Products'

    def __str__(self):
        """Unicode representation of Returned_Product."""
        return f" {self.branch} - {self.product} - {self.total_price}"
    
    
class Returned_Suit(Returned_Product_Abstract):
    """Model definition for Returned_Suit."""

    # TODO: Define fields here
    product = models.ForeignKey(Suit,verbose_name='suit',
                                on_delete=models.CASCADE,related_name = "Returned_Suit_product_type")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="Returned_Suit_branch")
    size_instance = models.ForeignKey(Size, verbose_name="size_instance", on_delete=models.CASCADE,
                        related_name="Returned_Suit_size_instance",null=True, blank=True)

    class Meta:
        """Meta definition for Returned_Suit."""

        verbose_name = 'Returned_Suit'
        verbose_name_plural = 'Returned_Suits'

    def __str__(self):
        """Unicode representation of Returned_Suit."""
        return f" {self.branch} - {self.product} - {self.total_price}"
    
class Returned_Top(Returned_Product_Abstract):
    """Model definition for Returned_Top."""

    # TODO: Define fields here
    product = models.ForeignKey(Top,verbose_name='top'
                                , on_delete=models.CASCADE,related_name = "Returned_Top_product_type")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="Returned_Top_branch")
    size_instance = models.ForeignKey(Size, verbose_name="size_instance", on_delete=models.CASCADE,
                        related_name="Returned_Top_size_instance",null=True, blank=True)
    

    class Meta:
        """Meta definition for Returned_Top."""

        verbose_name = 'Returned_Top'
        verbose_name_plural = 'Returned_Tops'

    def __str__(self):
        """Unicode representation of Returned_Top."""
        return f" {self.branch} - {self.product} - {self.total_price}"
    
class Returned_Foot_Wear(Returned_Product_Abstract):
    """Model definition for Returned_Foot_Wear."""

    # TODO: Define fields here
    product = models.ForeignKey(Foot_Wear,verbose_name='foot_wear'
                                , on_delete=models.CASCADE,related_name = "returned_foot_wear_product_type")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="returned_foot_wear_branch")
    size_instance = models.ForeignKey(Size, verbose_name="size_instance", on_delete=models.CASCADE,
                        related_name="returned_foot_wear_size_instance",null=True, blank=True)
    

    class Meta:
        """Meta definition for Returned_foot_wear."""

        verbose_name = 'Returned_Foot_Wear'
        verbose_name_plural = 'Returned_Foot_Wears'

    def __str__(self):
        """Unicode representation of Returned_Foot_Wear."""
        return f" {self.branch} - {self.product} - {self.total_price}"