from django.db import models
from Branch.models import Branch

from Product.models import Product, Size, Suit, Top

# Create your models here.
class Bad_Product_Abstract(models.Model):
    """Model definition for Bad_Product_Abstract."""

    # TODO: Define fields here
    qty = models.IntegerField("qty",null=False,blank=False)
    date = models.DateField("date", auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Bad_Product_Abstract."""
        abstract = True


class Bad_Product(Bad_Product_Abstract):
    """Model definition for Bad_Product."""

    # TODO: Define fields here
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name = "bad_product_product_type")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="bad_product_branch")
    size_instance = models.ForeignKey(Size, verbose_name="size_instance", on_delete=models.CASCADE,
                        related_name="bad_product_size_instance",null=True, blank=True)
    
    
    class Meta:
        """Meta definition for Bad_Product."""

        verbose_name = 'Bad_Product'
        verbose_name_plural = 'Bad_Products'
        ordering = ['-date']

    def __str__(self):
        """Unicode representation of Bad_Product."""
        return f'{self.branch} - {self.product} ({self.date})'
    
class Bad_Suit(Bad_Product_Abstract):
    """Model definition for Bad_Suit."""

    # TODO: Define fields here
    product = models.ForeignKey(Suit, on_delete=models.CASCADE,related_name = "Bad_Suit_product_type")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="Bad_Suit_branch")
    size_instance = models.ForeignKey(Size, verbose_name="size_instance", on_delete=models.CASCADE,
                        related_name="Bad_Suit_size_instance",null=True, blank=True)
    
    
    class Meta:
        """Meta definition for Bad_Suit."""

        verbose_name = 'Bad_Suit'
        verbose_name_plural = 'Bad_Suits'
        ordering = ['-date']

    def __str__(self):
        """Unicode representation of Bad_Suit."""
        return f'{self.branch} - {self.product} ({self.date})'
    
    
class Bad_Top(Bad_Product_Abstract):
    """Model definition for Bad_Top."""

    # TODO: Define fields here
    product = models.ForeignKey(Top, on_delete=models.CASCADE,related_name = "Bad_Top_product_type")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="Bad_Top_branch")
    size_instance = models.ForeignKey(Size, verbose_name="size_instance", on_delete=models.CASCADE,
                        related_name="Bad_Top_size_instance",null=True, blank=True)
    
    
    class Meta:
        """Meta definition for Bad_Top."""

        verbose_name = 'Bad_Top'
        verbose_name_plural = 'Bad_Tops'
        ordering = ['-date']

    def __str__(self):
        """Unicode representation of Bad_Top."""
        return f'{self.branch} - {self.product} ({self.date})'
    
