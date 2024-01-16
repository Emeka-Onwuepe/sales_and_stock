from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from Branch.models import (Branch_Foot_Wear, Branch_Product, 
                           Branch_Suit, Branch_Tops, 
                           Foot_Wear_Size, Product_Size,
                           Suit_Size, Tops_Size)
from Stock.models import Foot_Wear_Stock, Product_Stock, Suit_Stock, Tops_Stock

def manage_stock(instance,model,action='add'):
    mapper = {'product':[Branch_Product,Product_Size,Product_Stock],
              'suit':[Branch_Suit,Suit_Size,Suit_Stock],
              'top':[Branch_Tops,Tops_Size,Tops_Stock],
              'foot_wear':[Branch_Foot_Wear,Foot_Wear_Size,Foot_Wear_Stock],
              }
    
    branch_product,created = mapper[model][0].objects.get_or_create(branch = instance.branch,
                                                                    product = instance.product)
    product_size,created_ = mapper[model][1].objects.get_or_create(branch_instance = branch_product,
                                                                        size = instance.size_instance)
    # if model == 'product':
    #     product_size,created_ = mapper[model][1].objects.get_or_create(branch_instance = branch_product,
    #                                                                     size = instance.size_instance) 
    # elif model == 'suit':
    #     product_size,created_ = mapper[model][1].objects.get_or_create(branch_instance = branch_product,
    #                                                                     size = instance.size_instance)
    # elif model == "top":
    #     product_size,created_ = mapper[model][1].objects.get_or_create(branch_instance = branch_product,
    #                                                                     size = instance.size_instance)
    
    if action == 'delete':
        product_size.current_qty -= instance.qty
        product_size.save()
        return
    
    if instance.pk:
        old_instance = mapper[model][2].objects.get(pk=instance.pk)
        diff = instance.qty - old_instance.qty
        product_size.current_qty += diff
        product_size.save()
    else:  
        product_size.current_qty += instance.qty
        product_size.save()

@receiver(pre_save, sender=Product_Stock)
def stock_added(sender, instance, *args, **kwargs):
    manage_stock(instance,'product')


@receiver(pre_save, sender=Suit_Stock)
def stock_added(sender, instance, *args, **kwargs):
    manage_stock(instance,'suit')
    
@receiver(pre_save, sender=Tops_Stock)
def stock_added(sender, instance, *args, **kwargs):
    manage_stock(instance,'top')
    
@receiver(pre_save, sender=Foot_Wear_Stock)
def stock_added(sender, instance, *args, **kwargs):
    manage_stock(instance,'foot_wear')

        
@receiver(post_delete, sender=Product_Stock)
def stock_deleted(sender, instance, *args, **kwargs): 
    manage_stock(instance,'product','delete')
    
@receiver(post_delete, sender=Suit_Stock)
def stock_deleted(sender, instance, *args, **kwargs): 
    manage_stock(instance,'suit','delete')
    
@receiver(post_delete, sender=Tops_Stock)
def stock_deleted(sender, instance, *args, **kwargs): 
    manage_stock(instance,'top','delete')
    
@receiver(post_delete, sender=Foot_Wear_Stock)
def stock_deleted(sender, instance, *args, **kwargs): 
    manage_stock(instance,'foot_wear','delete')