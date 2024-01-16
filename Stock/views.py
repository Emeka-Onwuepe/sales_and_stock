from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Branch.models import Branch, Foot_Wear_Size, Product_Size, Suit_Size, Tops_Size
from Stock.forms import FootWearStockForm, ProductStockForm, SuitStockForm, TopsStockForm

from Stock.models import Foot_Wear_Stock, Product_Stock, Suit_Stock, Tops_Stock

# Create your views here.

@login_required(login_url="user:loginView")
def stockView(request,stockId,branchId,action,pgroup):
    mapper = {'product':[Product_Stock,ProductStockForm,Product_Size],
              'suits':[Suit_Stock,SuitStockForm,Suit_Size],
              'top':[Tops_Stock,TopsStockForm,Tops_Size],
              'foot_wear':[Foot_Wear_Stock,FootWearStockForm,Foot_Wear_Size],
    
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
    branch_stock = None
     
    branch_stock = mapper[pgroup][2].objects.filter(branch_instance__branch = branch)
    
    stocks = mapper[pgroup][0].objects.all()[:10]
    return render(request,"stock/stock.html",
                  {"stockId":0, 
                   'stocks':stocks,
                   "action":"add",
                   'branch_stock':branch_stock,
                   'branchId':branchId,
                   'branch':branch,
                    'form':form,
                   'pgroup':pgroup})
    

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
    if request.method == "POST":
        searched = True
        data = request.POST
        model = data['pgroup']
        stocks = mapper[model][0].objects.filter(
                                              branch_instance__product__product_type__name__iexact = data['product_type'],
                                              branch_instance__branch = data['branch'],
                                              branch_instance__product__age_group = data['age_group'],
                                              branch_instance__product__gender = data['gender'],
                                              branch_instance__product__brand__iexact = data['brand'],
                                              branch_instance__product__type__iexact = data['type'],
                                              branch_instance__product__color__iexact = data['color'],
                                              
                                              )
         
    return render(request,"stock/getstock.html",
                  {
                   'stocks':stocks,
                   'searched':searched,
                  })
    