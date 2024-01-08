from typing import Any
from django.db import models
from Branch.models import Branch
from Product.models import Product, Size, Size, Suit, Top

# Create your models here.
   
class Stock(models.Model):
    """Model definition for Product_Stock."""

    # TODO: Define fields here
    qty = models.IntegerField("qty", null=False, blank=False)
    date = models.DateTimeField("date",auto_now_add=True)

    class Meta:
        """Meta definition for Stock."""
        abstract = True

    
class Product_Stock(Stock):
   
    """Model definition for Product_Stock."""

    # TODO: Define fields here
    
    branch = models.ForeignKey(Branch, verbose_name="branch", on_delete=models.CASCADE,
                        related_name="product_stock_branch")
    size_instance = models.ForeignKey(Size, verbose_name="size_instance", on_delete=models.CASCADE,
                        related_name="product_stock_size_instance",null=True, blank=True)
    product = models.ForeignKey(Product, verbose_name="product", on_delete=models.CASCADE,
                        related_name="product_stock")

    class Meta:
        """Meta definition for Product_Stock."""

        verbose_name = 'Product Stock'
        verbose_name_plural = 'Product Stocks'
        

    def __str__(self):
        """Unicode representation of Product_Stock."""
        return f'{self.branch} - {self.product} - ({self.qty})'
    
    
class Suit_Stock(Stock):
    
    branch = models.ForeignKey(Branch, verbose_name="branch", on_delete=models.CASCADE,
                        related_name="suit_stock_branch")
    size_instance = models.ForeignKey(Size, verbose_name="size_instance", on_delete=models.CASCADE,
                        related_name="suit_stock_size_instance",null=True, blank=True)    
    product = models.ForeignKey(Suit, verbose_name="suit", on_delete=models.CASCADE,
                        related_name="suit_stock")
    
    
    class Meta:
        """Meta definition for Suit_Stock."""

        verbose_name = 'Suit Stock'
        verbose_name_plural = 'Suit Stocks'
        

    def __str__(self):
        """Unicode representation of Suit_Stock."""
        return f'{self.branch} - {self.product} - ({self.qty})'
    

class Tops_Stock(Stock):
    
    branch = models.ForeignKey(Branch, verbose_name="branch", on_delete=models.CASCADE,
                        related_name="tops_stock_branch")
    size_instance = models.ForeignKey(Size, verbose_name="size_instance", on_delete=models.CASCADE,
                        related_name="tops_stock_size_instance",null=True, blank=True)
    product = models.ForeignKey(Top, verbose_name="tops", on_delete=models.CASCADE,
                        related_name="top_stock")
        
        
    class Meta:
        """Meta definition for Tops_Stock."""

        verbose_name = 'Tops Stock'
        verbose_name_plural = 'Tops Stocks'
        

    def __str__(self):
        """Unicode representation of Tops_Stock."""
        return f'{self.branch} - {self.product} - ({self.qty})'
    
    