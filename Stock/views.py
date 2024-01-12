from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Branch.models import Branch, Branch_Product
from Product.models import Product, Size
from Stock.forms import ProductStockEditForm, ProductStockForm, SuitStockEditForm, SuitStockForm, TopsStockEditForm, TopsStockForm

from Stock.models import Product_Stock, Stock, Suit_Stock, Tops_Stock

# Create your views here.

# @login_required(login_url="user:loginView")
# def stockView(request,stockId,branchId,action,pgroup):
    
#     branch = Branch.objects.get(pk=branchId)
    
#     stock_list = []
    
#     for branch_product in branch.branch_product_branch.all():
           
#         dic = {}    
#         if branch_product.is_multiple_sized:
#             for multiple_size in branch_product.multiple_size_set.all():
#                 dic["product"] = branch_product.product
#                 dic['size'] = multiple_size.size
#                 stocks = Stock.objects.filter(product= branch_product.product.id,
#                                               branch = branch_product.branchId,
#                                               size_instance = multiple_size.size.id)[0:1]
#                 if stocks:         
#                     dic['stock'] = stocks
#                     stock_list.append(dic)
#                 dic = {}
#         else:
#             dic["product"] =branch_product.product
#             dic['size'] = None
#             stocks = Stock.objects.filter(product= branch_product.product.id,
#                                               branch = branch_product.branchId)[0:1]
#             if stocks:
#                 dic['stock'] = stocks
#                 stock_list.append(dic)  
            
#             dic = {}
            
    
#     if stockId != 0:   
#         stock_instance = Stock.objects.get(id=stockId)
    
#     if request.method == "POST" and action == "add":
#         data= request.POST
#         product_size = data['product'].split("-")
#         if len(product_size)>1:
#             productId,sizeId = product_size
#             product = Product.objects.get(pk=int(productId))
#             size = Size.objects.get(pk = int(sizeId))
#             Stock.objects.create(product=product,branch=branch,
#                                  size_instance=size,qty=int(data['qty']))
#         else:
#             product = Product.objects.get(pk=int(data['product']))
#             Stock.objects.create(product=product,branch=branch,qty=int(data['qty']))
        
#         return HttpResponseRedirect(reverse('stock:stockView',
#             kwargs={"action":"view","stockId":0,'branchId':branchId}))
       
            
#     if action == "edit":
#         if request.method == "POST":
#             form = ProductStockEditForm(data= request.POST,instance=stock_instance)
#             if form.is_valid():
#                 form.save()
#                 return HttpResponseRedirect(reverse('stock:stockView',
#                         kwargs={"action":"view","stockId":0,'branchId':branchId}))
#             else:
#                 return render(request,"stock/stock.html",
#                   {"form":form,"stockId":stock_instance.id,
#                    "action":"edit",'branch':branch,"instance":stock_instance,
#                    "stock_list":stock_list})
#         else:
#             return render(request,"stock/stock.html",
#                   {"form":ProductStockEditForm(instance=stock_instance),
#                    "stockId":stock_instance.id,"action":"edit",
#                    "instance":stock_instance,'branch':branch,
#                    "stock_list":stock_list})
    
#     if action == "delete":
#         stock_instance.delete()
#         return HttpResponseRedirect(reverse('stock:stockView',
#             kwargs={"action":"view","stockId":0,'branchId':branchId}))
                 
#     return render(request,"stock/stock.html",
#                   {"stockId":0,"action":"add",'branch':branch,
#                    "stock_list":stock_list})
    
    
    

@login_required(login_url="user:loginView")
def stockView(request,stockId,branchId,action,pgroup):
    mapper = {'product':[Product_Stock,ProductStockForm,ProductStockEditForm],
              'suits':[Suit_Stock,SuitStockForm,SuitStockEditForm],
              'top':[Tops_Stock,TopsStockForm,TopsStockEditForm],
              'foot_wears':[Product_Stock,ProductStockForm,ProductStockEditForm],
    
              }
    branch = Branch.objects.get(pk=branchId)
    form = mapper[pgroup][1]({'branch':branch.id,
                              'qty':0,
                              'product':"",
                              'size_instance':""})
    if stockId != 0:   
        stock_instance = mapper[pgroup][0].objects.get(id=stockId)
        form = mapper[pgroup][1](instance=stock_instance)
        
    if request.method == "POST" and action == "add":
        form = mapper[pgroup][1](data= request.POST,files=request.FILES)
        # form.data['branch'] = branch
        if form.is_valid():
            form.save()
            # product.sizes.all()
            return HttpResponseRedirect(reverse('stock:stockView',
            kwargs={"action":"view","stockId":0,'pgroup':pgroup,'branchId':branchId}))
        else:
            return render(request,"stock/stock.html",
                  {"form":form,"stockId":0,"action":"add",
                   'pgroup':pgroup})  
            
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
    print(branch.Branch_Suit_branch.suit_size)
    stocks = mapper[pgroup][0].objects.all()
    return render(request,"stock/stock.html",
                  {"stockId":0, 
                   'stocks':stocks,
                   "action":"add",
                   'branchId':branchId,
                   'branch':branch,
                    'form':form,
                   'pgroup':pgroup})
