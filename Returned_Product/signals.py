from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from Branch.models import Branch_Product, Branch_Suit, Branch_Tops, Product_Size, Suit_Size, Tops_Size
from Returned_Product.models import Returned_Product, Returned_Suit, Returned_Top


def manage_stock(instance,model,action='add'):
    mapper = {'product':[Branch_Product,Product_Size,Returned_Product],
              'suit':[Branch_Suit,Suit_Size,Returned_Suit],
              'top':[Branch_Tops,Tops_Size,Returned_Top],
              }
    print(model)
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
        product_size.returned_qty -= instance.qty
        product_size.current_qty -= instance.qty
        product_size.save()
        return
    
    if instance.pk:
        old_instance = mapper[model][2].objects.get(pk=instance.pk)
        diff = instance.qty - old_instance.qty
        product_size.returned_qty += diff
        product_size.current_qty += diff
        product_size.save()
    else:  
        product_size.returned_qty += instance.qty
        product_size.current_qty += instance.qty
        product_size.save()

@receiver(pre_save, sender=Returned_Product)
def stock_added(sender, instance, *args, **kwargs):
    manage_stock(instance,'product')


@receiver(pre_save, sender=Returned_Suit)
def stock_added(sender, instance, *args, **kwargs):
    manage_stock(instance,'suit')
    
@receiver(pre_save, sender=Returned_Top)
def stock_added(sender, instance, *args, **kwargs):
    manage_stock(instance,'top')

        
@receiver(post_delete, sender=Returned_Product)
def stock_deleted(sender, instance, *args, **kwargs): 
    manage_stock(instance,'product','delete')
    
@receiver(post_delete, sender=Returned_Suit)
def stock_deleted(sender, instance, *args, **kwargs): 
    manage_stock(instance,'suit','delete')
    
@receiver(post_delete, sender=Returned_Top)
def stock_deleted(sender, instance, *args, **kwargs): 
    manage_stock(instance,'top','delete')