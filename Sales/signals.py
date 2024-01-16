from django.db.models.signals import pre_delete,m2m_changed,post_save
from django.dispatch import receiver
from Branch.models import (Branch_Foot_Wear, Branch_Product, Branch_Suit, Branch_Tops, Foot_Wear_Size, 
                           Product_Size, Suit_Size, Tops_Size)
from Sales.models import Items, Sales


def manage_stock(instance,branch,action='add'):
    mapper = {'product':[Branch_Product,Product_Size],
              'suit':[Branch_Suit,Suit_Size],
              'top':[Branch_Tops,Tops_Size],
              'foot_wear':[Branch_Foot_Wear,Foot_Wear_Size],
              
              }
    
    model = instance.p_group
    
    if model == 'product':
        branch_product,created = mapper[model][0].objects.get_or_create(branch = branch,
                                                                    product = instance.product)
        # product_size,created_ = mapper[model][1].objects.get_or_create(branch_instance = branch_product,
        #                                                                 size = instance.size_instance) 
    elif model == 'suit':
        branch_product,created = mapper[model][0].objects.get_or_create(branch = branch,
                                                                    product = instance.suit)
        # product_size,created_ = mapper[model][1].objects.get_or_create(branch_instance = branch_product,
        #                                                                 size = instance.size_instance)
    elif model == "top":
        branch_product,created = mapper[model][0].objects.get_or_create(branch = branch,
                                                                    product = instance.top)
        # product_size,created_ = mapper[model][1].objects.get_or_create(branch_instance = branch_product,
        #                                                                 size = instance.size_instance)
    elif model == "foot_wear":
        branch_product,created = mapper[model][0].objects.get_or_create(branch = branch,
                                                                    product = instance.foot_wear)
        # product_size,created_ = mapper[model][1].objects.get_or_create(branch_instance = branch_product,
        #                                                                 size = instance.size_instance)
        
    product_size,created_ = mapper[model][1].objects.get_or_create(branch_instance = branch_product,
                                                                        size = instance.size_instance)
        
    if action == 'delete' or action == 'remove' :
        product_size.current_qty += instance.qty
        product_size.save()
        return
 
    product_size.current_qty -= instance.qty
    product_size.save()


@receiver(m2m_changed, sender= Sales.items.through)
def sales_multipleSIzes_changes(sender, instance,action,reverse,model,pk_set,**kwargs):
    if action == "post_add" and instance.paid and instance.channel == "store":
        for item_id in pk_set:
            item = Items.objects.get(pk=item_id)
            manage_stock(item,instance.branch,action='add')
    elif action == 'pre_remove' and instance.paid:
        for item_id in pk_set:
            item = Items.objects.get(pk=item_id)
            manage_stock(item,instance.branch,action='remove')
            
@receiver(post_save, sender=Sales)
def mark_as_paid(sender, instance, *args, **kwargs): 
    if instance.paid and instance.channel == "web":
        for item in instance.items.all():
            manage_stock(item,instance.branch,action='add')
        
@receiver(pre_delete, sender=Sales)
def delete_sale(sender, instance, *args, **kwargs):
    for item in instance.items.all():
        manage_stock(item,instance.branch,action='delete')