from datetime import datetime
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from Branch.models import Branch, Branch_Foot_Wear, Branch_Product, Branch_Suit, Branch_Tops, Foot_Wear_Size, Product_Size, Suit_Size, Tops_Size
from Credit_Sales.models import Credit_Sale
from Product.models import Foot_Wear, Product, Product_Type, Size, Suit, Top
from Product.serializer import FootWearSerializer, ProductSerializer, SuitSerializer, TopSerializer
from Sales.forms import salesForm
from Sales.models import Items, Sales
from User.Forms import CustomerForm
from User.models import Customer

# Create your views here.
@login_required(login_url="user:loginView")
def salesView(request):
    
    json_data = {'products':[]}
    pgroup = ''
    if request.method == "POST":
        mapper = {'product':[Product,ProductSerializer],
              'suits':[Suit,SuitSerializer],
              'top':[Top,TopSerializer],
              'foot_wear':[Foot_Wear,FootWearSerializer],
    
              }
        products=[]
        found = False
        data = request.POST
        # product_type = Product_Type.objects.filter(name__icontains =data)
        
        # for item in product_type:   
        #     product = Product.objects.filter(branches=request.user.branch,
        #                                      product_type = item.id)
        pgroup = data['pgroup']
        # pgroup = data['pgroup']
        products= mapper[pgroup][0].objects.filter(
                                                    product_type__name__iexact = data['product_type'],
                                                    age_group = data['age_group'],
                                                    gender = data['gender'],
                                                    brand__iexact = data['brand'],
                                                    type__iexact = data['type'],
                                                    color__iexact = data['color'],
                                                    )
        
       
        jsonData = mapper[pgroup][1](products,many=True).data
        if products:
            found = True
            json_data['products'] =  jsonData
            # products.append(product)
        return render(request,"sales/sales.html",
                          {'products':products,'json_data':json_data,
                           'initial':False,"found":found,'pgroup':pgroup,
                           "customerForm":CustomerForm, "saleForm":salesForm})
        
    return render(request,"sales/sales.html",{'initial':True,'found':False,
                                              'json_data':json_data,'pgroup':pgroup,
                                              "customerForm":CustomerForm, "saleForm":salesForm})

@login_required(login_url="user:loginView")
def saleView(request,purchaseId,type):
    sale = None
    customer = None
    not_found = False
    try:
        if type == 'credit':
            sale = Credit_Sale.objects.get(purchase_id= purchaseId)
            customer = sale.customer
        else:
            sale = Sales.objects.get(purchase_id= purchaseId)
            customer = sale.customer
    except (Credit_Sale.DoesNotExist,Sales.DoesNotExist):
        not_found = True
  
    
    
    return render(request,"sales/sale.html",{"sale":sale,
                                             "customer":customer,'not_found':not_found})

@login_required(login_url="user:loginView")
def salesProductView(request,productTypeId,pgroup,brand='default'):
    json_data = {'products':[]}
    mapper = {'product':[Product,ProductSerializer,Branch_Product,Product_Size],
              'suits':[Suit,SuitSerializer,Branch_Suit,Suit_Size],
              'top':[Top,TopSerializer,Branch_Tops,Tops_Size],
              'foot_wear':[Foot_Wear,FootWearSerializer,Branch_Foot_Wear,Foot_Wear_Size],
    
              }
    products = []
    sizes = []
    initial = True
    brands = []
    productType = None
    
    if productTypeId != 0 and brand != 'default':
        initial = False
        if brand == 'None':
            brand = None
        products = mapper[pgroup][0].objects.filter(product_type = productTypeId,brand = brand)
        
        
        for product in products:
            filtered_sizes = []
            branch_product = mapper[pgroup][2].objects.get(branch=request.user.branch,
                                                           product = product)
            for size in product.sizes.all():
                qty =  mapper[pgroup][3].objects.get(branch_instance=branch_product,
                                                     size = size).current_qty
                if qty >= 0:
                    filtered_sizes.append(size)
            sizes.append(filtered_sizes)
        
        jsonData = mapper[pgroup][1](products,many=True).data
        json_data['products'] =  jsonData
    
    if productTypeId != 0:
        brands = mapper[pgroup][0].objects.filter(product_type = productTypeId).values('brand').distinct()
        productType = Product_Type.objects.get(pk=productTypeId)
    return render(request,"sales/product.html",{"products":zip(products,sizes),"customerForm":CustomerForm,
                                                'json_data':json_data,'pgroup':pgroup,
                                                'productType':productTypeId,'brands':brands,
                                                'productTypeName':productType,
                                                "saleForm":salesForm,'initial':initial})

@login_required(login_url="user:loginView")
def processSalesView(request):
    
   if request.method == "POST":
       customer_instance = None
       credit_or_sales = None
       sale_type = None
       data = json.loads(request.body.decode("utf-8"))
       orderlist = data['orders']
       
       mapper = {'product':[Product],
              'suits':[Suit],
              'top':[Top],
              'foot_wear':[Foot_Wear],
              }
       
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
       
       if data['payment_method'] == "credit":
           credit_or_sales = Credit_Sale.objects.create(branch=request.user.branch,
                                               total_amount=float(data['total_amount']),
                                               expected_amount=float(data['expected_amount']),
                                               remark = data['remark'],
                                               customer = customer_instance,
                                               purchase_id = data['purchase_id'])
       else:
           credit_or_sales = Sales.objects.create(branch=request.user.branch,
                                               total_amount=data['total_amount'],
                                               expected_amount=data['expected_amount'],
                                               remark = data['remark'],
                                               channel ="store",
                                               customer = customer_instance,
                                               payment_method = data['payment_method'],
                                               purchase_id = data['purchase_id'])
           sale_type = credit_or_sales.payment_method
       
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
            
            credit_or_sales.items.add(Item)
         
           
       return JsonResponse({"purchase_id":credit_or_sales.purchase_id,
                            "type":sale_type})
       
@login_required(login_url="user:loginView")     
def salesAnalysisView(request,date,branchID):
    
    selected_branch = request.user.branch
    
    if branchID != 0 and request.user.is_admin:
        selected_branch = branchID
    
    if date == "default":
        date = datetime.today().strftime('%Y-%m-%d')
    
    products_data = []
    online_sales = []
    store = Items.objects.filter(items__date=date,items__channel='store',items__branch=selected_branch)
    transfer_total = Items.objects.filter(items__date=date,
                                       items__payment_method='transfer',
                                       items__branch=selected_branch).aggregate(total=Sum("total_price"))
    cash_total = Items.objects.filter(items__date=date,
                                items__branch=selected_branch,
                                       items__payment_method='cash').aggregate(total=Sum("total_price"))
    credit =  Items.objects.filter(credit_sale_Items__date =date,credit_sale_Items__branch=selected_branch)
   
    
    
    day_data ={
        "store_sales":{
            # "transferData":transfer,
            # "cashData":cash,
            "sales": store,
            "summary":store.values('product','suit','foot_wear','top','p_group').annotate(
                        total_amount=Sum("total_price"),total_qty =Sum("qty")),
            "transfer":transfer_total,
            "cash": cash_total,
            "total_amount":store.aggregate(total=Sum("total_price"))
        },
        "credit_sales":{
            "sales": credit,
            "summary": credit.values('product','suit','foot_wear','top','p_group').annotate(
                        total_amount=Sum("total_price"),total_qty =Sum("qty")),
            "total_amount":credit.aggregate(total=Sum("total_price")),
        }
    }
    
    if request.user.is_admin:
        online_sales = Items.objects.filter(items__date=date,items__channel='web',items__paid=True)
        online = {
            "sales": online_sales,
            "summary": online_sales.values('suit','foot_wear','top','p_group').annotate(
                        total_amount=Sum("total_price"),total_qty =Sum("qty")),
            "total_amount":online_sales.aggregate(total=Sum("total_price"),logistics=Sum('items__logistics')),
        }
        
        branches = Branch.objects.all()
    
        day_data["online_sales"] = online
        day_data["branches"] = branches
    
    for sale_type in [store,credit,online_sales]:
        for item in sale_type:
            id = item.get_product().id 
            add = True
            
            for product_data in products_data:
                if product_data['p_group'] == item.p_group and product_data['id'] == id:
                    add = False
                    break
            if add:   
                data = {'id':id,
                        'p_group': item.p_group,
                        'category':item.get_product().product_type.category.name,
                        'name': item.get_product().product_type.name,
                        'brand': item.get_product().brand,
                        'color': item.get_product().color,
                        'get_details': item.get_product().get_details(),
                        }
                products_data.append(data)
    day_data['products_data'] = products_data
           
    return render(request,"sales/daysales.html",day_data)



@login_required(login_url="user:loginView")
def rangeSalesView(request,start_date,end_date,branchID):

    selected_branch = request.user.branch.id
    
    if branchID != 0 and request.user.is_admin:
        selected_branch = branchID
    
    branch_instance = Branch.objects.get(pk=selected_branch)
    
    products_data = []
    online_sales = []
    store = Items.objects.filter(items__date__range=[start_date,end_date],
                                 items__channel='store',items__branch=selected_branch)
    credit =  Items.objects.filter(credit_sale_Items__date__range=[start_date,end_date],
                                   credit_sale_Items__branch=selected_branch)
    
    data ={
        "store_sales":{
            "summary":store.values('items__date','suit','foot_wear','top','p_group').annotate(
                        total_amount=Sum("total_price"),total_qty =Sum("qty")),
            "total_amount":store.aggregate(total=Sum("total_price"))
        },
        "credit_sales":{
            "summary": credit.values('credit_sale_Items__date', 'suit','foot_wear','top','p_group').annotate(
                        total_amount=Sum("total_price"),total_qty =Sum("qty")),
            "total_amount":credit.aggregate(total=Sum("total_price")),
        }
    }
    
    if request.user.is_admin:
        online_sales = Items.objects.filter(items__date__range=[start_date,end_date],
                                  items__branch=selected_branch, items__channel='web', items__paid=True)
    
        online = {
            "summary": online_sales.values('items__date', 'suit','foot_wear','top','p_group').annotate(
                        total_amount=Sum("total_price"),total_qty =Sum("qty")),
            "total_amount":online_sales.aggregate(total=Sum("total_price"),logistics=Sum("items__logistics")),
        }
    
        data["online_sales"] = online
    
    data["branch"] = branch_instance
    data['title'] = f'Range Sales: {start_date} -- {end_date}'
    
    for sale_type in [store,credit,online_sales]:
        for item in sale_type:
            id = item.get_product().id 
            add = True
            
            for product_data in products_data:
                if product_data['p_group'] == item.p_group and product_data['id'] == id:
                    add = False
                    break
            if add:   
                data_ = {'id':id,
                        'p_group': item.p_group,
                        'category':item.get_product().product_type.category.name,
                        'name': item.get_product().product_type.name,
                        'brand': item.get_product().brand,
                        'color': item.get_product().color,
                        'get_details': item.get_product().get_details(),
                        }
                products_data.append(data_)
    data['products_data'] = products_data
   
    return render(request,"sales/rangesales.html",data)      

