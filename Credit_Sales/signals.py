from django.db.models.signals import pre_delete,m2m_changed,post_save,pre_save
from django.dispatch import receiver
from Branch.models import (Branch_Foot_Wear, Branch_Product, Branch_Suit, Branch_Tops, Foot_Wear_Size, 
                           Product_Size, Suit_Size, Tops_Size)
from Credit_Sales.models import Credit_Sale, Payment
from Sales.models import Items


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

@receiver(pre_save, sender=Credit_Sale)
def add_credit_sale(sender, instance, *args, **kwargs):
    print('about to add credit sales')
    if not instance.pk:
        instance.balance = instance.total_amount * -1
    if instance.total_payment  >= instance.total_amount:
        instance.fully_paid = True
    else:
        instance.fully_paid = False
        
@receiver(m2m_changed, sender= Credit_Sale.items.through)
def credit_sale_multipleSIzes_changes(sender, instance,action,reverse,model,pk_set,**kwargs):
    print('credit sales m2m fired')
    if action == "post_add":
        for item_id in pk_set:
            item = Items.objects.get(pk=item_id)
            manage_stock(item,instance.branch,action='add')
    elif action == 'pre_remove':
        for item_id in pk_set:
            item = Items.objects.get(pk=item_id)
            manage_stock(item,instance.branch,action='remove')
            
        
@receiver(pre_delete, sender=Credit_Sale)
def delete_sale(sender, instance, *args, **kwargs):
    for item in instance.items.all():
        manage_stock(item,instance.branch,action='delete')
        

# Payment signals 
@receiver(pre_save, sender=Payment)
def add_payment(sender, instance, *args, **kwargs):
    credit_sale = Credit_Sale.objects.get(pk=instance.credit_sale_id)
    if instance.pk:
        old_instance = Payment.objects.get(pk=instance.pk)
        diff = instance.amount - old_instance.amount
        credit_sale.total_payment += diff
        credit_sale.balance += diff
        credit_sale.save()
    else:
        credit_sale.total_payment += instance.amount
        credit_sale.balance += instance.amount
        credit_sale.save()
 
@receiver(pre_delete, sender=Payment)   
def delete_payment(sender, instance, *args, **kwargs):
    credit_sale = Credit_Sale.objects.get(pk=instance.credit_sale_id)
    credit_sale.total_payment -= instance.amount
    credit_sale.balance -= instance.amount
    credit_sale.save(False)