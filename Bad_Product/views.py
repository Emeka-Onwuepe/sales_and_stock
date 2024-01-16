from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Bad_Product.forms import BadFootWearForm, BadProductForm, BadSuitForm, BadTopForm
from Bad_Product.models import Bad_Foot_Wear, Bad_Product, Bad_Suit, Bad_Top

# Create your views here.

@login_required(login_url="user:loginView")
def badProductView(request,badProductId,action,pgroup):
    
    mapper = {'product':[Bad_Product,BadProductForm],
              'suits':[Bad_Suit,BadSuitForm],
              'top':[Bad_Top,BadTopForm],
              'foot_wear':[Bad_Foot_Wear,BadFootWearForm],
              }
    bad_products = mapper[pgroup][0].objects.all()[:10]
    form = mapper[pgroup][1]()
    if badProductId != 0:
        bad_instance = mapper[pgroup][0].objects.get(id=badProductId)
        

    if request.method == "POST" and action == "add":
        data= request.POST
        form = mapper[pgroup][1](data= request.POST)
        if form.is_valid():
            form.save()
        
        
        return HttpResponseRedirect(reverse('badproduct:badProductView',
            kwargs={"action":"view","badProductId":0,'pgroup':pgroup}))
        
    if action == "edit":
        form = mapper[pgroup][1](instance=bad_instance)
        if request.method == "POST":
            form = mapper[pgroup][1](data= request.POST,instance=bad_instance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('badproduct:badProductView',
                        kwargs={"action":"view","badProductId":0,'pgroup':pgroup}))
            else:
                return render(request,"bad_product/badproduct.html",
                  {"form":form,"action":"edit",'pgroup':pgroup,
                   "badProductId":badProductId})
        else:
            return render(request,"bad_product/badproduct.html",
                  {"action":"edit",'pgroup':pgroup,"form":form,
                   "badProductId":badProductId})
    
    if action == "delete":
        bad_instance.delete()
        return HttpResponseRedirect(reverse('badproduct:badProductView',
            kwargs={"action":"view","badProductId":0,'pgroup':pgroup}))
        
        
                 
    return render(request,"bad_product/badproduct.html",
                  {'pgroup':pgroup,
                   "badProductId":badProductId,
                   "action":"add","form":form,
                   'bad_products':bad_products})
    
    