from django.db.models.signals import pre_save, post_save, post_delete,m2m_changed
from django.dispatch import receiver
from Branch.models import (Branch, Branch_Foot_Wear, Branch_Product, Branch_Suit,
                           Branch_Tops, Foot_Wear_Size, Product_Size, Suit_Size, Tops_Size)
from Product.models import  Foot_Wear, Product, Suit, Top

# products signals
@receiver(pre_save, sender=Product)
def update_Product_image(sender, instance, *args, **kwargs):
    if instance.pk:
        product = Product.objects.get(pk=instance.pk)
        if product.image != instance.image:
            product.image.delete(False)
            
    
@receiver(post_delete, sender=Product)
def delete_product_image(sender, instance, using, *args, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
     
        
@receiver(pre_save, sender=Suit)
def update_suit_image(sender, instance, *args, **kwargs):
    if instance.pk:
        product = Suit.objects.get(pk=instance.pk)
        if product.image != instance.image:
            product.image.delete(False)
               
@receiver(post_delete, sender=Suit)
def delete_suit_image(sender, instance, using, *args, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
  
        
@receiver(pre_save, sender=Top)
def update_top_image(sender, instance, *args, **kwargs):
    if instance.pk:
        product = Top.objects.get(pk=instance.pk)
        if product.image != instance.image:
            product.image.delete(False)
              
@receiver(post_delete, sender=Top)
def delete_top_image(sender, instance, using, *args, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
       
@receiver(pre_save, sender=Foot_Wear)
def update_foot_wear_image(sender, instance, *args, **kwargs):
    if instance.pk:
        product = Foot_Wear.objects.get(pk=instance.pk)
        if product.image != instance.image:
            product.image.delete(False)
              
@receiver(post_delete, sender=Foot_Wear)
def delete_foot_wear_image(sender, instance, using, *args, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
        
        
def handle_branch_product(instance,key):
    mapper = {'product':[Branch_Product,Product_Size],
              'suit':[Branch_Suit,Suit_Size],
              'top':[Branch_Tops,Tops_Size],
              'foot_wear':[Branch_Foot_Wear,Foot_Wear_Size],
    
              }
    
    branches = Branch.objects.all()
    for branch in branches:  
        branch_product,created = mapper[key][0].objects.get_or_create(branch = branch,
                                                                      product = instance)
        
        if instance.sizes.exists():                                                          
            for size in instance.sizes.all():
                product_size,created_ = mapper[key][1].objects.get_or_create(branch_instance = branch_product,
                                                                             size = size)
                # if key == 'product':
                #     product_size,created_ = mapper[key][1].objects.get_or_create(branch_instance = branch_product,
                #                                                             size = size)
                # elif key == 'suit':
                #     product_size,created_ = mapper[key][1].objects.get_or_create(branch_instance = branch_product,
                #                                                             size = size)
                # elif key == "top":
                #     product_size,created_ = mapper[key][1].objects.get_or_create(branch_instance = branch_product,
                #                                                             size = size)
        
                 
@receiver(post_save, sender=Product)
def product_saved(sender, instance,*args,**kwargs):
    handle_branch_product(instance,'product')

@receiver(m2m_changed, sender=Product.sizes.through)
def product_sizes_changes(sender, instance,action,reverse,model,pk_set,**kwargs):
    if action == "post_add":
        handle_branch_product(instance,'product')
        
                
@receiver(post_save, sender=Suit)
def suit_saved(sender, instance,*args,**kwargs):
    handle_branch_product(instance,'suit')

@receiver(m2m_changed, sender=Suit.sizes.through)
def suit_sizes_changes(sender, instance,action,reverse,model,pk_set,**kwargs):
    if action == "post_add":
        handle_branch_product(instance,'suit')
          
                
@receiver(post_save, sender=Top)
def top_saved(sender, instance,*args,**kwargs):
    handle_branch_product(instance,'top')

@receiver(m2m_changed, sender=Top.sizes.through)
def top_sizes_changes(sender, instance,action,reverse,model,pk_set,**kwargs):
    if action == "post_add":
        handle_branch_product(instance,'top')
        
                    
@receiver(post_save, sender=Foot_Wear)
def foot_wear_saved(sender, instance,*args,**kwargs):
    handle_branch_product(instance,'foot_wear')

@receiver(m2m_changed, sender=Foot_Wear.sizes.through)
def foot_wear_sizes_changes(sender, instance,action,reverse,model,pk_set,**kwargs):
    if action == "post_add":
        handle_branch_product(instance,'foot_wear')
        