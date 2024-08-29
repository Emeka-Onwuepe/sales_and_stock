import json
import requests
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from Branch.models import Branch, Branch_Foot_Wear, Branch_Product, Branch_Suit, Branch_Tops, Foot_Wear_Size, Product_Size, Suit_Size, Tops_Size
from Logistics.models import Location
from Product.models import Category, Foot_Wear, Product, Product_Type, Size, Suit, Top
from Sales.models import Items, Sales
from User.models import Customer
from sales_and_stock.variables import official_email,rootUrl,admin_staff

from django.db.models.functions import Lower

# mapper = {'product':[Product],
#               'suits':[Suit],
#               'top':[Top],
#               'foot_wear':[Foot_Wear],
#               }
mapper = {'product':[Product,Branch_Product,Product_Size],
              'suits':[Suit,Branch_Suit,Suit_Size],
              'top':[Top,Branch_Tops,Tops_Size],
              'foot_wear':[Foot_Wear,Branch_Foot_Wear,Foot_Wear_Size],
    
              }
# Create your views here.
def homeView(request):
    products_list = []   
    sizes = []
    for pgroup in mapper.values():
        products = pgroup[0].objects.filter(publish=True)[:10]
        if products:
            products_list.append(products)
            
            for product in products:
                filtered_sizes = []
                branch_product = pgroup[1].objects.get(branch__name='Main',
                                                            product = product)
                for size in product.sizes.all():
                    qty =  pgroup[2].objects.get(branch_instance=branch_product,
                                                        size = size).current_qty
                    if qty >= 0:
                        filtered_sizes.append(size)
                sizes.append(filtered_sizes)
        
    return render(request,'frontview/home.html',{"products_list":zip(products_list,sizes)})

def cartView(request): 
    locations = Location.objects.all()
    return render(request,'frontview/cart.html',{"public_key":settings.PAYSTACT_PUBLIC_KEY,
                                                 "locations":locations})

def categoryView(request,cat,brand,p_type):
    brand = brand.replace('_',' ').replace('%20',' ').replace('-',' ').strip()
    p_type = p_type.replace('_',' ').replace('%20',' ').replace('-',' ').strip()
    cat = cat.replace('_',' ').replace('%20',' ').replace('-',' ').strip()
    sizes = []
    
    if brand == 'None':
        brand = None   
    
    category = get_object_or_404(Category,name__iexact=cat)
    product_type = Product_Type.objects.filter(category=category)[0]
    pgroup = product_type.p_group
    
    if brand == 'default' and p_type == 'default':
        p_type = mapper[pgroup][0].objects.filter(publish=True,product_type__category=category)[0]
        p_type = Product_Type.objects.get(id=p_type.product_type.id)
        
        brand = mapper[pgroup][0].objects.filter(publish=True,product_type__category=category,product_type = p_type.id)[0]
        brand = brand.brand
    elif brand != 'default' and p_type != 'default':
        p_type = Product_Type.objects.get(name=p_type,category = category)
       
    elif  p_type != 'default':
        p_type = Product_Type.objects.get(name=p_type,category = category)
        
        brand = mapper[pgroup][0].objects.filter(publish=True,product_type__category=category,product_type = p_type.id)[0]
        brand = brand.brand
    elif brand != 'default':
        p_type = mapper[pgroup][0].objects.filter(publish=True,product_type__category=category)[0]
        p_type = Product_Type.objects.get(id=p_type.product_type.id)
 
    products = mapper[pgroup][0].objects.filter(publish=True,product_type__category=category,brand=brand,product_type=p_type.id)
    for product in products:
            filtered_sizes = []
            branch_product = mapper[pgroup][1].objects.get(branch__name='Main',
                                                            product = product)
            for size in product.sizes.all():
                qty =  mapper[pgroup][2].objects.get(branch_instance=branch_product,
                                                        size = size).current_qty
                if qty <=0:
                    filtered_sizes.append(size)
            sizes.append(filtered_sizes)
    
    if not products:
        # try a randon brand
        brand = mapper[pgroup][0].objects.filter(publish=True,product_type__category=category,product_type = p_type.id)[0]
        brand = brand.brand
        products = mapper[pgroup][0].objects.filter(publish=True,product_type__category=category,brand=brand,product_type=p_type.id)
        
   
    brands = mapper[pgroup][0].objects.filter(publish=True,product_type__category=category,product_type=p_type.id).annotate(lower = Lower('brand')).values_list('lower',flat=True)
    distincts = mapper[pgroup][0].objects.filter(publish=True,product_type__category=category).values_list('product_type').distinct()
    product_types = Product_Type.objects.filter(id__in = distincts)
   
    brands = set(brands)
    
    
    # unsorted_product_types = Product_Type.objects.filter(category=category.id,
    #                                                         product_type__publish = True)
    # sorted_product_types = []
    # for product_type in unsorted_product_types:
    #     if product_type not in sorted_product_types:
    #         sorted_product_types.append(product_type) 
            
    return render(request,'frontview/category.html',{"category":category,
                                                     "products":zip(products,sizes),
                                                     'brands' :brands,
                                                     'product_types':product_types,
                                                      'p_type':p_type.name,
                                                      'brand_': brand})
    
    
def processPaymentView(request):
       if request.method == "POST":
           customer_instance = None
           sales = None
           sale_type = None
           data = json.loads(request.body.decode("utf-8"))
           
           if data['action'] == "payment":

               headers = {
                    "Authorization": f'Bearer {settings.PAYSTACT_SECRET_KEY}',
                        'Content-Type': 'application/json',
                }
               url = f'https://api.paystack.co/transaction/verify/{data["purchase_id"]}'
                
               response = requests.get(url,headers=headers)
                
               if response.status_code == 200:
                #    response_data = response.json()
                   sales = Sales.objects.get(purchase_id=data["purchase_id"])
                   sales.paid = True
                   sales.save()
                #    email_body = (f"There is a new online sale with ID:{sales.purchase_id}. Please, view " +
                #         f"sales details on {rootUrl}/sales/sale/{sales.purchase_id}/{sales.payment_method} ")
                #    send_mail('A new order',email_body,official_email,[admin_staff])
                   return JsonResponse({"message":'success'})
                        
           if data['action'] == "create":
               
                orderlist = data['orders']
                
                try:
                    customer_instance = Customer.objects.get(phone_number = data['phone_number'])
                    customer_instance.phone_number = data["phone_number"]
                    customer_instance.email = data["email"]
                    customer_instance.name = data["name"]
                    customer_instance.address = data["address"]
                    customer_instance.save()
                except Customer.DoesNotExist:
                        customerData = {"phone_number":data["phone_number"], "email":data["email"],
                                "name":data["name"],"address":data["address"]}
                        customer_instance = Customer.objects.create(**customerData)
                
                branch = Branch.objects.get(branch__is_super_admin = True)
                sales = Sales.objects.create(branch=branch,
                                                    total_amount=data['total_amount'],
                                                    expected_amount=data['expected_amount'],
                                                    logistics=data['logistics'],
                                                    destination=data['address'],
                                                    remark = data['remark'],
                                                    channel ="web",
                                                    customer = customer_instance,
                                                    payment_method = data['payment_method'],
                                                    purchase_id = data['purchase_id'],
                                                    paid=False)
                
                for item in orderlist:
            
                    pgroup = item['pgroup']
                    product = mapper[pgroup][0].objects.get(pk=int(item['id']))
                    size= None
                    
                    if item['id'] != item['Id']:
                        _,sizeId= item['Id'].split("_")
                        size = Size.objects.get(pk=int(sizeId))
                        
                        
                    if pgroup == 'suits':
                        pgroup = 'suit'
                        Item =  Items.objects.create(suit=product,product_type=item['product_type'],
                                                    p_group = pgroup,size_instance=size,
                                                    qty=item['qty'],
                                                    unit_price=item['price'],total_price=item['productTotal'],
                                                    mini_price=item['mini'],expected_price=item['expected'])
                    elif pgroup == 'top':
                        Item =  Items.objects.create(top=product,product_type=item['product_type'],
                                                    p_group = pgroup,size_instance=size,
                                                    qty=item['qty'],
                                                    unit_price=item['price'],total_price=item['productTotal'],
                                                    mini_price=item['mini'],expected_price=item['expected'])
                    elif pgroup == 'product':
                        Item =  Items.objects.create(product=product,product_type=item['product_type'],
                                                    p_group = pgroup,size_instance=size,
                                                    qty=item['qty'],
                                                    unit_price=item['price'],total_price=item['productTotal'],
                                                    mini_price=item['mini'],expected_price=item['expected'])
                    elif pgroup == 'foot_wear':
                        Item =  Items.objects.create(foot_wear=product,product_type=item['product_type'],
                                                    p_group = pgroup,size_instance=size,
                                                    qty=item['qty'],
                                                    unit_price=item['price'],total_price=item['productTotal'],
                                                    mini_price=item['mini'],expected_price=item['expected'])
                    
                    # credit_or_sales.items.add(Item)
                    sales.items.add(Item)
                    
                    
                return JsonResponse({"purchase_id":sales.purchase_id,
                                    "type":sale_type})


def customerOrderHistoryView(request):
    if request.method == "POST":
        phone_number = request.POST["phone_number"]
        sales=[]
        if phone_number:
            sales = Sales.objects.filter(customer__phone_number = phone_number)
        return render(request,"frontview/orderhistory.html",{"orders":sales,"public_key":settings.PAYSTACT_PUBLIC_KEY})      
    return HttpResponseRedirect(reverse('frontview:cartView'))
        
def saleView(request,purchaseId):
    sale = get_object_or_404(Sales,purchase_id= purchaseId)
    return render(request,"frontview/saledetails.html",{"sale":sale,"customer":sale.customer})       