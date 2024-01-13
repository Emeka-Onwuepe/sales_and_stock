from django.db import models

# Create your models here.

class Branch(models.Model):
    """Model definition for Branch."""

    # TODO: Define fields here
    name = models.CharField('Branch Name', max_length = 200)

    class Meta:
        """Meta definition for Branch."""

        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'

    def __str__(self):
        """Unicode representation of Branch."""
        return self.name


class Branch_Product(models.Model):
    """Model definition for Branch_Product."""

    # TODO: Define fields here
    branch = models.ForeignKey(Branch, verbose_name="branch", 
                on_delete=models.CASCADE, related_name="branch_product_branch")  
    product = models.ForeignKey("Product.Product", verbose_name="product", 
                on_delete=models.CASCADE, related_name="branch_product_product") 
  
  
    class Meta:
        """Meta definition for Branch_Product."""

        verbose_name = 'Branch_Product'
        verbose_name_plural = 'Branch_Products'

    def __str__(self):
        """Unicode representation of Branch_Product."""
        return f'{self.branch} - {self.product}'
    

class Product_Size(models.Model):
    """Model definition for product_Size."""

    # TODO: Define fields here
    branch_instance = models.ForeignKey(Branch_Product, verbose_name="branch_product",
                                       related_name = 'branch_product_size',
                                       on_delete=models.CASCADE)
    size = models.ForeignKey("Product.Size", related_name='branch_product_sizes',
                             on_delete=models.CASCADE)
    current_qty = models.IntegerField("current_qty", default=0)
    returned_qty = models.IntegerField("returned_qty", default=0)
    bad_qty = models.IntegerField("bad_qty", default=0)

    class Meta:
        """Meta definition for product_Size."""

        verbose_name = 'product_Size'
        verbose_name_plural = 'product_Sizes'

    def __str__(self):
        """Unicode representation of product_Size."""
        return f'{self.branch_instance} - {self.size}'


class Branch_Suit(models.Model):
    """Model definition for Branch_Suit."""

    # TODO: Define fields here
    branch = models.ForeignKey(Branch, verbose_name="branch", 
                on_delete=models.CASCADE, related_name="branch_suit_branch")  
    product = models.ForeignKey("Product.Suit", verbose_name="product", 
                on_delete=models.CASCADE, related_name="branch_suit_product") 


    class Meta:
        """Meta definition for Branch_Suit."""

        verbose_name = 'Branch_Suit'
        verbose_name_plural = 'Branch_Suits'

    def __str__(self):
        """Unicode representation of Branch_Suit."""
        return f'{self.branch} - {self.product}'
    

class Suit_Size(models.Model):
    """Model definition for Suit_size."""

    # TODO: Define fields here
    branch_instance = models.ForeignKey(Branch_Suit, verbose_name="Branch_Suit",
                                    related_name = 'branch_suit_size',
                                       on_delete=models.CASCADE)
    # Suit_size = models.CharField('product size',max_length=25)
    size = models.ForeignKey("Product.Size", related_name='branch_suit_sizes',
                             on_delete=models.CASCADE)
    current_qty = models.IntegerField("current_qty", default=0)
    returned_qty = models.IntegerField("returned_qty", default=0)
    bad_qty = models.IntegerField("bad_qty", default=0)

    class Meta:
        """Meta definition for Suit_size."""

        verbose_name = 'Suit_size'
        verbose_name_plural = 'Suit_sizes'

    def __str__(self):
        """Unicode representation of Suit_size."""
        return f'{self.branch_instance} - {self.size}'


class Branch_Tops(models.Model):
    """Model definition for Branch_Tops."""

    # TODO: Define fields here
    branch = models.ForeignKey(Branch, verbose_name="branch", 
                on_delete=models.CASCADE, related_name="branch_tops_branch")  
    product = models.ForeignKey("Product.Top", verbose_name="product", 
                on_delete=models.CASCADE, related_name="branch_tops_product") 



    class Meta:
        """Meta definition for Branch_Tops."""

        verbose_name = 'Branch_Tops'
        verbose_name_plural = 'Branch_Tops'

    def __str__(self):
        """Unicode representation of Branch_Tops."""
        return f'{self.branch} - {self.product}'
    

class Tops_Size(models.Model):
    """Model definition for Top_Size."""

    # TODO: Define fields here
    branch_instance = models.ForeignKey(Branch_Tops, verbose_name="Branch_Tops",
                                    related_name = 'branch_tops_size',
                                       on_delete=models.CASCADE)
    # Top_Size = models.CharField('product size',max_length=25)
    size = models.ForeignKey("Product.Size", related_name='branch_tops_sizes',
                             on_delete=models.CASCADE)
    current_qty = models.IntegerField("current_qty", default=0)
    returned_qty = models.IntegerField("returned_qty", default=0)
    bad_qty = models.IntegerField("bad_qty", default=0)

    class Meta:
        """Meta definition for Top_Size."""

        verbose_name = 'Top_Size'
        verbose_name_plural = 'Top_Sizes'

    def __str__(self):
        """Unicode representation of Top_Size."""
        return f'{self.branch_instance} - {self.size}'
