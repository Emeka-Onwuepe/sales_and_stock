from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Returned_Product.forms import ReturnedFootWearForm, ReturnedProductForm, ReturnedSuitForm, ReturnedTopForm

from Returned_Product.models import Returned_Foot_Wear, Returned_Product, Returned_Suit, Returned_Top
from Product.models import Foot_Wear, Product, Product_Type, Suit, Top
from django.db.models import Q

# Create your views here.

@login_required(login_url="user:loginView")
def returnedProductView(request,returnedProductId,action,pgroup):
    
    mapper = {'product':[Returned_Product,ReturnedProductForm,Product],
              'suits':[Returned_Suit,ReturnedSuitForm,Suit],
              'top':[Returned_Top,ReturnedTopForm,Top],
              'foot_wear':[Returned_Foot_Wear,ReturnedFootWearForm,Foot_Wear],
              }
    
    
    form = mapper[pgroup][1]()
    productType = Product_Type.objects.all()
    products = []
    branchid = 0
    
    if returnedProductId != 0:
        returned_instance = mapper[pgroup][0].objects.get(id=returnedProductId)
        
    if request.method == 'POST' and action == 'get':
        data = request.POST
        pgroup = data['pgroup']
        branchid = data['branch']
        products = mapper[pgroup][2].objects.filter(
                                                        # branch_instance__branch = branch
                                                         Q(product_type__id = int(data['product_type'])) &
                                                        #  Q(branch_instance__branch = data['branch']) &
                                                         Q(age_group = data['age_group']) &
                                                         Q(gender = data['gender']) &
                                                         Q(brand__iexact = data['brand']) &
                                                         Q(type__iexact = data['type']) &
                                                         Q(color__iexact = data['color']) 
                                                        )
        
    if request.method == 'POST' and action == 'select':
        data = request.POST
        pgroup = data['pgroup']

        form = mapper[pgroup][1](data = {
                                  'qty': data['qty'],
                                  'unit_price': data['unit_price'],
                                  'total_price': data['total_price'],
                                  'date_of_purchase': data['date_of_purchase'],
                                  'date_of_return': data['date_of_return'],
                                  'product':data['product'],
                                  'branch':data['branch'],
                                  'size_instance':data['size'],
                                  })
        if form.is_valid():
            form.save()
            form = mapper[pgroup][1]()
            
        
    returned_products = mapper[pgroup][0].objects.all()[:10]
        

    if request.method == "POST" and action == "add":
        form = mapper[pgroup][1](data= request.POST)
        if form.is_valid():
            form.save()
        
        
        return HttpResponseRedirect(reverse('returnedproduct:returnedProductView',
            kwargs={"action":"view","returnedProductId":0,'pgroup':pgroup}))
        
    if action == "edit":
        form = mapper[pgroup][1](instance=returned_instance)
        if request.method == "POST":
            form = mapper[pgroup][1](data= request.POST,instance=returned_instance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('returnedproduct:returnedProductView',
                        kwargs={"action":"view","returnedProductId":0,'pgroup':pgroup}))
            else:
                return render(request,"returned_product/returnedproduct.html",
                  {"form":form,"action":"edit",'pgroup':pgroup,
                   "returnedProductId":returnedProductId})
        else:
            return render(request,"returned_product/returnedproduct.html",
                  {"action":"edit",'pgroup':pgroup,"form":form,
                   'returned_products':returned_products,
                   "returnedProductId":returnedProductId})
    
    if action == "delete":
        returned_instance.delete()
        return HttpResponseRedirect(reverse('returnedproduct:returnedProductView',
            kwargs={"action":"view","returnedProductId":0,'pgroup':pgroup}))
        
        
    return render(request,"returned_product/returnedproduct.html",
                  {'pgroup':pgroup,
                   "returnedProductId":returnedProductId,
                   "action":"add","form":form,
                   'returned_products':returned_products,
                   'productType':productType,
                   'products':products,
                   'branchid':branchid,
                   })
    
    