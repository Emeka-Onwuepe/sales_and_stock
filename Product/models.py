from typing import Any
from django.db import models

from Branch.models import Branch
# Create your models here.

class Category(models.Model):
    """Model definition for Category."""

    # TODO: Define fields here
    name = models.CharField("Category",max_length = 150,null=False,blank=False)
    image = models.ImageField(verbose_name="image", default="image",null=True,blank=True)
    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """Unicode representation of Category."""
        return self.name


class Product_Type(models.Model):
    """Model definition for Product_Type."""
    
    SUITS = 'suits'
    FOOT_WEAR = 'foot_wear'
    TOP = 'top'
    PRODUCT = 'product'

    P_GROUP = {SUITS:'suits',
               FOOT_WEAR:'foot_wear',
               TOP :'top',
               PRODUCT :'product',
                } 

    # TODO: Define fields here
    name = models.CharField("name",max_length = 200,null=False,blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="category")
    p_group = models.CharField(
        max_length=10,
        choices=P_GROUP,
        default=PRODUCT,
    )
    
    
    
    class Meta:
        """Meta definition for Product_Type."""

        verbose_name = 'Product_Type'
        verbose_name_plural = 'Product_Types'

    def __str__(self):
        """Unicode representation of Product_Type."""
        return f"{self.category} - {self.name}"


class Size(models.Model):
    """Model definition for Size."""
    
    FEMALE = 'F'
    MALE = 'M'
    UNISEX = 'U'
    ADULT = 'A'
    CHILDREN = 'C'


    GENDER = {FEMALE:'Female',
              MALE:"Male",
              UNISEX:'Unisex',
              }
    AGE_GROUP = {ADULT:'Adult',
                 CHILDREN:'Children'
                 }
    
    product_type = models.ForeignKey(Product_Type, on_delete=models.CASCADE,related_name="size_product_type")
    size = models.CharField(verbose_name="size", max_length=150)
    gender = models.CharField(
        max_length=2,
        choices=GENDER,
        default=UNISEX,
    )
    age_group = models.CharField(
        max_length=2,
        choices=AGE_GROUP,
        default=ADULT,
    )
    price = models.IntegerField(verbose_name="price")
   

    class Meta:
        """Meta definition for Size."""

        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'

    def __str__(self):
        """Unicode representation of Topping."""
        return f' {self.product_type}-{self.size}-{self.price}'
    
    
class Product_Abstract(models.Model):
    """Model definition for Product."""
    
    FEMALE = 'F'
    MALE = 'M'
    UNISEX = 'U'
    ADULT = 'A'
    CHILDREN = 'C'

    GENDER = {FEMALE:'Female',
              MALE:"Male",
              UNISEX:'Unisex',
              }
    AGE_GROUP = {ADULT:'Adult',
                 CHILDREN:'Children'
                 }
    
    # TODO: Define fields here
    # product_type = models.ForeignKey(Product_Type, on_delete=models.CASCADE, related_name="product_type")
    # size = models.CharField(verbose_name="size",default="0", max_length=150,null=True,blank=True)
    description = models.TextField(verbose_name="description", max_length=150,null=False,blank=False)
    # sizes = models.ManyToManyField(
    #     Size, verbose_name="sizes", related_name="sizes", blank=True)
    color = models.CharField("color",max_length = 200,null=False,blank=False)
    image = models.ImageField(verbose_name="image", default="image",null=True,blank=True)
    gender = models.CharField(
        max_length=2,
        choices=GENDER,
        default=UNISEX,
    )
    age_group = models.CharField(
        max_length=2,
        choices=AGE_GROUP,
        default=ADULT,
    )
    

    type = models.CharField(verbose_name="type",default=None, max_length=50,null=True,blank=True)
    brand = models.CharField(verbose_name="brand",default=None, max_length=50,null=True,blank=True)
    type = models.CharField(verbose_name="type",default=None, max_length=100,null=True,blank=True)
    # price = models.DecimalField("price", max_digits=50,default=0, decimal_places=2,null=True,blank=True)
    date = models.DateField("date", auto_now=False, auto_now_add=True)
    publish = models.BooleanField(default=False)
    # branches = models.ManyToManyField(Branch, verbose_name="branches",related_name="products_branches",blank=True)

    class Meta:
        """Meta definition for Product."""
        abstract = True

    
class Product(Product_Abstract):
    product_type = models.ForeignKey(Product_Type, on_delete=models.CASCADE, related_name="product_type")
    sizes = models.ManyToManyField(
        Size, verbose_name="sizes", related_name="product_sizes", blank=True)
    
    
    class Meta:
        """Meta definition for Product."""

        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        # ordering = ['-date']
        # abstract = True

    def __str__(self):
        """Unicode representation of Product."""
        return f"{self.product_type} - {self.color}"
        
class Suit(Product_Abstract):
    product_type = models.ForeignKey(Product_Type, on_delete=models.CASCADE, related_name="suit_product_type")
    sizes = models.ManyToManyField(
        Size, verbose_name="sizes", related_name="sizes", blank=True)
    # sleeves = models.CharField(verbose_name="sleeves",default=None, max_length=25,null=True,blank=True)
    breasted = models.CharField(verbose_name="breasted",default=None, max_length=25,null=True,blank=True)
    button = models.CharField(verbose_name="button",default=None, max_length=25,null=True,blank=True)
    pics = models.CharField(verbose_name="pics",default=None, max_length=25,null=True,blank=True)
    golden_button = models.CharField(verbose_name="golden button",default=None, max_length=25,null=True,blank=True)
    
    class Meta:
        """Meta definition for Suit."""

        verbose_name = 'Suit'
        verbose_name_plural = 'Suits'
        ordering = ['-date']
        
    def __str__(self):
        """Unicode representation of Suits."""
        return f"{self.product_type} - {self.color}"
    


class Top(Product_Abstract):
    product_type = models.ForeignKey(Product_Type, on_delete=models.CASCADE, related_name="top_product_type")
    sizes = models.ManyToManyField(
        Size, verbose_name="sizes", related_name="top_sizes", blank=True)
    sleeves = models.CharField(verbose_name="sleeves",default=None, max_length=25,null=True,blank=True)
    
    class Meta:
        """Meta definition for Top."""

        verbose_name = 'Top'
        verbose_name_plural = 'Tops'
        ordering = ['-date']
        
    def __str__(self):
        """Unicode representation of Tops."""
        return f"{self.product_type} - {self.color}"
    
class Foot_Wear(Product_Abstract):
    product_type = models.ForeignKey(Product_Type, on_delete=models.CASCADE, related_name="foot_wear_product_type")
    sizes = models.ManyToManyField(
        Size, verbose_name="sizes", related_name="foot_wear_sizes", blank=True)
    sole_color = models.CharField(verbose_name="Sole Color",default=None, max_length=25,null=True,blank=True)
    
    class Meta:
        """Meta definition for Foot_Wear."""

        verbose_name = 'Foot_Wear'
        verbose_name_plural = 'Foot_Wears'
        ordering = ['-date']
        
    def __str__(self):
        """Unicode representation of Foot_Wears."""
        return f"{self.product_type} - {self.color}"
