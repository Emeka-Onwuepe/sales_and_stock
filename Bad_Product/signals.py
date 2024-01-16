from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from Branch.models import Branch_Foot_Wear, Branch_Product, Branch_Suit, Branch_Tops, Foot_Wear_Size, Product_Size, Suit_Size, Tops_Size
from Bad_Product.models import Bad_Foot_Wear, Bad_Product, Bad_Suit, Bad_Top


def manage_stock(instance,model,action='add'):
    mapper = {'product':[Branch_Product,Product_Size,Bad_Product],
              'suit':[Branch_Suit,Suit_Size,Bad_Suit],
              'top':[Branch_Tops,Tops_Size,Bad_Top],
              'foot_wear':[Branch_Foot_Wear,Foot_Wear_Size,Bad_Foot_Wear],
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
        product_size.bad_qty -= instance.qty
        product_size.current_qty += instance.qty
        product_size.save()
        return
    
    if instance.pk:
        old_instance = mapper[model][2].objects.get(pk=instance.pk)
        diff = instance.qty - old_instance.qty
        product_size.bad_qty += diff
        product_size.current_qty -= diff
        product_size.save()
    else:  
        product_size.bad_qty += instance.qty
        product_size.current_qty -= instance.qty
        product_size.save()

@receiver(pre_save, sender=Bad_Product)
def stock_added(sender, instance, *args, **kwargs):
    manage_stock(instance,'product')


@receiver(pre_save, sender=Bad_Suit)
def stock_added(sender, instance, *args, **kwargs):
    manage_stock(instance,'suit')
    
@receiver(pre_save, sender=Bad_Top)
def stock_added(sender, instance, *args, **kwargs):
    manage_stock(instance,'top')
    
@receiver(pre_save, sender=Bad_Foot_Wear)
def stock_added(sender, instance, *args, **kwargs):
    manage_stock(instance,'foot_wear')

        
@receiver(post_delete, sender=Bad_Product)
def stock_deleted(sender, instance, *args, **kwargs): 
    manage_stock(instance,'product','delete')
    
@receiver(post_delete, sender=Bad_Suit)
def stock_deleted(sender, instance, *args, **kwargs): 
    manage_stock(instance,'suit','delete')
    
@receiver(post_delete, sender=Bad_Top)
def stock_deleted(sender, instance, *args, **kwargs): 
    manage_stock(instance,'top','delete')
    
@receiver(post_delete, sender=Bad_Foot_Wear)
def stock_deleted(sender, instance, *args, **kwargs): 
    manage_stock(instance,'foot_wear','delete')