from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Returned_Product.forms import ReturnedFootWearForm, ReturnedProductForm, ReturnedSuitForm, ReturnedTopForm

from Returned_Product.models import Returned_Foot_Wear, Returned_Product, Returned_Suit, Returned_Top

# Create your views here.

@login_required(login_url="user:loginView")
def returnedProductView(request,returnedProductId,action,pgroup):
    
    mapper = {'product':[Returned_Product,ReturnedProductForm],
              'suits':[Returned_Suit,ReturnedSuitForm],
              'top':[Returned_Top,ReturnedTopForm],
              'foot_wear':[Returned_Foot_Wear,ReturnedFootWearForm],
              }
    returned_products = mapper[pgroup][0].objects.all()[:10]
    form = mapper[pgroup][1]()
    if returnedProductId != 0:
        returned_instance = mapper[pgroup][0].objects.get(id=returnedProductId)
        

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
                return HttpResponseRedirect(reverse('Returnedproduct:returnedProductView',
                        kwargs={"action":"view","returnedProductId":0,'pgroup':pgroup}))
            else:
                return render(request,"returned_product/returnedproduct.html",
                  {"form":form,"action":"edit",'pgroup':pgroup,
                   "returnedProductId":returnedProductId})
        else:
            return render(request,"returned_product/returnedproduct.html",
                  {"action":"edit",'pgroup':pgroup,"form":form,
                   "returnedProductId":returnedProductId})
    
    if action == "delete":
        returned_instance.delete()
        return HttpResponseRedirect(reverse('returnedproduct:returnedProductView',
            kwargs={"action":"view","returnedProductId":0,'pgroup':pgroup}))
        
        
    return render(request,"returned_product/returnedproduct.html",
                  {'pgroup':pgroup,
                   "returnedProductId":returnedProductId,
                   "action":"add","form":form,
                   'returned_products':returned_products})
    
    