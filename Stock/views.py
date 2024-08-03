from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Branch.models import Branch, Foot_Wear_Size, Product_Size, Suit_Size, Tops_Size
from Product.models import Foot_Wear, Product, Product_Type, Suit, Top
from Stock.forms import FootWearStockForm, ProductStockForm, SuitStockForm, TopsStockForm

from Stock.models import Foot_Wear_Stock, Product_Stock, Suit_Stock, Tops_Stock

from django.db.models import Q

# Create your views here.

@login_required(login_url="user:loginView")
def stockView(request,stockId,branchId,action,pgroup):
    mapper = {'product':[Product_Stock,ProductStockForm,Product_Size,Product],
              'suits':[Suit_Stock,SuitStockForm,Suit_Size,Suit],
              'top':[Tops_Stock,TopsStockForm,Tops_Size,Top],
              'foot_wear':[Foot_Wear_Stock,FootWearStockForm,Foot_Wear_Size,Foot_Wear],
    
              }
    branch = Branch.objects.get(pk=branchId)
    form = mapper[pgroup][1]({'branch':branch.id,
                              'qty':0,
                              'product':"",
                              'size_instance':""})
    
    branch_stock = []
    productType = Product_Type.objects.all()
    stocks = mapper[pgroup][0].objects.all()[:10]

     
    if stockId != 0:   
        stock_instance = mapper[pgroup][0].objects.get(id=stockId)
        form = mapper[pgroup][1](instance=stock_instance)
        
    
    if request.method == "POST" and action == "get":
        data = request.POST
        pgroup = data['pgroup']
        # print('inside get stock')
        # stocks = mapper[pgroup][0].objects.filter(
        #                                      Q(branch_instance__product__product_type__id = int(data['product_type'])) &
        #                                       Q(branch_instance__branch = branch.id) &
        #                                       Q(branch_instance__product__age_group = data['age_group']) &
        #                                       Q(branch_instance__product__gender = data['gender']) &
        #                                       Q(branch_instance__product__brand__iexact = data['brand']) &
        #                                       Q(branch_instance__product__type__iexact = data['type']) &
        #                                       Q(branch_instance__product__color__iexact = data['color']) 
        #                                       )
        branch_stock = mapper[pgroup][2].objects.filter(
                                                        # branch_instance__branch = branch
                                                         Q(branch_instance__product__product_type__id = int(data['product_type'])) &
                                                         Q(branch_instance__branch = branch.id) &
                                                         Q(branch_instance__product__age_group = data['age_group']) &
                                                         Q(branch_instance__product__gender = data['gender']) &
                                                         Q(branch_instance__product__brand__iexact = data['brand']) &
                                                         Q(branch_instance__product__type__iexact = data['type']) &
                                                         Q(branch_instance__product__color__iexact = data['color']) 
                                                        )
        
        # print(branch_stock)
        
    if request.method == "POST" and action == "add":
        form = mapper[pgroup][1](data= request.POST,files=request.FILES)
        # form.data['branch'] = branch
        data = request.POST
        # pgroup = data['pgroup']
        if form.is_valid():
            form.save()
            # product.sizes.all()
            product  = mapper[pgroup][3].objects.get(pk=data['product'])
            branch_stock = mapper[pgroup][2].objects.filter(
                                                        # branch_instance__branch = branch
                                                         Q(branch_instance__product__product_type__id = product.product_type.id) &
                                                         Q(branch_instance__branch = branch.id) &
                                                         Q(branch_instance__product__age_group = product.age_group) &
                                                         Q(branch_instance__product__gender = product.gender) &
                                                         Q(branch_instance__product__brand__iexact = product.brand) &
                                                         Q(branch_instance__product__type__iexact = product.type) &
                                                         Q(branch_instance__product__color__iexact = product.color) 
                                                        )

            # return HttpResponseRedirect(reverse('stock:stockView',
            # kwargs={"action":"view","stockId":0,'pgroup':pgroup,'branchId':branchId}))
        else:
            return render(request,"stock/stock.html",
                  {"form":form,"stockId":0,"action":"add",
                   'branchId':branchId,'pgroup':pgroup})  
            
    if action == "edit" and request.method == "POST":
            
        form = mapper[pgroup][1](data= request.POST,files=request.FILES,instance=stock_instance)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('stock:stockView',
                        kwargs={"action":"view","stockId":0,'pgroup':pgroup,'branchId':branchId}))
        else:
            return render(request,"stock/stock.html",
                  {"form":form,'branchId':branchId,
                   "stockId":stock_instance.id,
                   "action":"edit",'pgroup':pgroup})
    elif action == "edit" and request.method == "GET":
        return render(request,"stock/stock.html",
                  {"stock_instance":stock_instance,
                   "stockId":stock_instance.id,
                   'branchId':branchId,
                   "action":"edit",
                   'form':form,
                    'pgroup':pgroup})
    
    if action == "delete":
        stock_instance.delete()
        return HttpResponseRedirect(reverse('stock:stockView',
            kwargs={"action":"view","stockId":0,'pgroup':pgroup,'branchId':branchId}))
    # branch_stock = None
     
    # branch_stock = mapper[pgroup][2].objects.filter(branch_instance__branch = branch)

    return render(request,"stock/stock.html",
                  {"stockId":0, 
                   'stocks':stocks,
                   "action":"add",
                   'branch_stock':branch_stock,
                   'branchId':branchId,
                   'branch':branch,
                    'form':form,
                   'pgroup':pgroup,
                   'productType':productType})
    

@login_required(login_url="user:loginView")
def getStockView(request):
    
    mapper = {'product':[Product_Size],
              'suits':[Suit_Size],
              'top':[Tops_Size],
              'foot_wear':[Foot_Wear_Size],
              }
    
    #  'branch': [''], 'pgroup': ['suits'], 'gender': [''], 'age_group': [''], 'product_type': ['sss'], 'brand': ['sss'], 'type': ['ssss'], 'color': ['sss']
    stocks = None
    searched = False
    all = False
    data = []
    if request.method == "POST":
        searched = True
        data = request.POST
        model = data['pgroup']
        if data['branch'] != '0':
            
            
            stocks = mapper[model][0].objects.filter(
                                             Q(branch_instance__product__product_type__id = int(data['product_type'])) &
                                              Q(branch_instance__branch = data['branch']) &
                                              Q(branch_instance__product__age_group = data['age_group']) &
                                              Q(branch_instance__product__gender = data['gender']) &
                                              Q(branch_instance__product__brand__iexact = data['brand']) &
                                              Q(branch_instance__product__type__iexact = data['type']) &
                                              Q(branch_instance__product__color__iexact = data['color']) 
                                              )
        else:
            stocks = mapper[model][0].objects.filter(
                                              Q(branch_instance__product__product_type__id = int(data['product_type'])) &
                                              Q(branch_instance__product__age_group = data['age_group']) &
                                              Q(branch_instance__product__gender = data['gender']) &
                                              Q(branch_instance__product__brand__iexact = data['brand']) &
                                              Q(branch_instance__product__type__iexact = data['type']) &
                                              Q(branch_instance__product__color__iexact = data['color'])
                                              ).select_related('branch_instance')
        
            
            data_ = {}
            for stock in stocks:
                key = f'{stock.branch_instance.product_id}_{stock.size_id}'
                if data_.get(key):
                    data_[key][1] = data_[key][1] + stock.current_qty
                    data_[key][2] = data_[key][2] + stock.returned_qty
                    data_[key][3] = data_[key][3] + stock.bad_qty
                else:
                    data_[key] = [stock,stock.current_qty,stock.returned_qty,stock.bad_qty]

            all = True
            stocks = []
            data = data_.values()
    productType = Product_Type.objects.all()
    # print(productType)
            # print(list(data)[0][0].branch_instance.product.get_details())
    return render(request,"stock/getstock.html",
                  {
                   'stocks':stocks,
                   'searched':searched,
                   'all':all,
                   'all_':data,
                   'productType':productType
                  })
    