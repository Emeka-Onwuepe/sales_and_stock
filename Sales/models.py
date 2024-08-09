from django.db import models
from django.forms import BooleanField
from Branch.models import Branch
from Product.models import Foot_Wear, Product, Size, Suit, Top
from User.models import Customer

# Create your models here.

class Items(models.Model):
    """Model definition for Items."""
    
    SUIT = 'suit'
    FOOT_WEAR = 'foot_wear'
    TOP = 'top'
    PRODUCT = 'product'

    P_GROUP = {SUIT:'suit',
               FOOT_WEAR:'foot_wear',
               TOP :'top',
               PRODUCT :'product',
                } 
    
    p_group = models.CharField(
        max_length=10,
        choices=P_GROUP,
        default=PRODUCT,
    )
    
    product = models.ForeignKey(Product, verbose_name="product", 
                    related_name="selected_product", on_delete=models.CASCADE,null=True, blank=True)
    suit = models.ForeignKey(Suit, verbose_name="suit", 
                    related_name="selected_suit", on_delete=models.CASCADE,null=True, blank=True)
    top = models.ForeignKey(Top, verbose_name="top", 
                    related_name="selected_top", on_delete=models.CASCADE,null=True, blank=True)
    foot_wear = models.ForeignKey(Foot_Wear, verbose_name="foot_wear", 
                    related_name="selected_foot_wear", on_delete=models.CASCADE,null=True, blank=True)
    product_type = models.CharField('product_type', max_length = 200)
    size_instance = models.ForeignKey(Size, verbose_name="size_instance", on_delete=models.CASCADE,
                        related_name="items_size_instance",null=True, blank=True)
    qty = models.IntegerField("qty")
    unit_price = models.DecimalField("unit_price", max_digits=10, decimal_places=2)
    total_price = models.DecimalField("total_price", max_digits=10, decimal_places=2)
    mini_price = models.DecimalField("mini_price", max_digits=10, decimal_places=2)
    expected_price = models.DecimalField("expected_price", max_digits=10, decimal_places=2)
    

    # TODO: Define fields here

    def get_product(self):
        if self.p_group == 'suit':
            return self.suit
        elif self.p_group == 'foot_wear':
            return self.foot_wear
        elif self.p_group == 'top':
            return self.top
        elif self.p_group == 'product':
            return self.product
        
    class Meta:
        """Meta definition for Items."""

        verbose_name = 'Items'
        verbose_name_plural = 'Items'

    def __str__(self):
        """Unicode representation of Items."""
        return f"{self.product_type} - {str(self.total_price)}"


class Sales(models.Model):
    """Model definition for Sales."""
    CHANNEL_CHOICES = (
        ('web', 'web'),
        ('store', 'store'),
    )
    PAYMENT_CHOICES = (
        ('transfer', 'transfer'),
        ('cash', 'cash'),
        ('credit', 'credit'),
        ('on_web', 'on_web'),
    )

    # TODO: Define fields here
    branch = models.ForeignKey(Branch,related_name="sales_branch", verbose_name="branch", on_delete=models.CASCADE)
    total_amount = models.DecimalField("total_amount", max_digits=10, decimal_places=2)
    expected_amount = models.DecimalField("expected_amount", max_digits=10, decimal_places=2)
    logistics = models.DecimalField("logistics", max_digits=10, decimal_places=2,default=0.00)
    destination = models.CharField("destination", max_length=256,default="not set",blank=True)
    remark = models.CharField("remark", max_length=200)
    channel = models.CharField("channel", max_length=5, choices=CHANNEL_CHOICES, default='store')
    payment_method = models.CharField("payment_method", max_length=8, choices=PAYMENT_CHOICES, default='cash')
    date = models.DateField("date", auto_now=False, auto_now_add=True)
    customer = models.ForeignKey(Customer, verbose_name="customer",related_name="sales_customer",on_delete=models.CASCADE)
    items = models.ManyToManyField(Items, verbose_name="items",related_name="items")
    purchase_id = models.CharField("purchase_id", max_length=150,unique=True)
    paid = models.BooleanField("paid",default=True)
    
    class Meta:
        """Meta definition for Sales."""

        verbose_name = 'Sales'
        verbose_name_plural = 'Sales'
        ordering = ["-date"]

    def __str__(self):
        """Unicode representation of Sales."""
        return f"{self.purchase_id} - {str(self.total_amount)}"
