from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Bad_Product.forms import BadFootWearForm, BadProductForm, BadSuitForm, BadTopForm
from Bad_Product.models import Bad_Foot_Wear, Bad_Product, Bad_Suit, Bad_Top
from Product.models import Foot_Wear, Product, Product_Type, Suit, Top
from django.db.models import Q

# Create your views here.

@login_required(login_url="user:loginView")
def badProductView(request,badProductId,action,pgroup):
    
    mapper = {'product':[Bad_Product,BadProductForm,Product],
              'suits':[Bad_Suit,BadSuitForm,Suit],
              'top':[Bad_Top,BadTopForm,Top],
              'foot_wear':[Bad_Foot_Wear,BadFootWearForm,Foot_Wear],
              }
    # bad_products = mapper[pgroup][0].objects.all()[:10]
    form = mapper[pgroup][1]()
    productType = Product_Type.objects.all()
    products = []
    branchid = 0
    
    if badProductId != 0:
        bad_instance = mapper[pgroup][0].objects.get(id=badProductId)
        
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
                                  'product':data['product'],
                                  'branch':data['branch'],
                                  'size_instance':data['size'],
                                  })
        if form.is_valid():
            form.save()
            form = mapper[pgroup][1]()
            
        
    bad_products = mapper[pgroup][0].objects.all()[:10]    

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
                   "badProductId":badProductId,
                   'bad_products':bad_products})
    
    if action == "delete":
        bad_instance.delete()
        return HttpResponseRedirect(reverse('badproduct:badProductView',
            kwargs={"action":"view","badProductId":0,'pgroup':pgroup}))
        
        
                 
    return render(request,"bad_product/badproduct.html",
                  {'pgroup':pgroup,
                   'productType':productType,
                   "badProductId":badProductId,
                   "action":"add","form":form,
                   'products':products,
                   'branchid':branchid,
                   'bad_products':bad_products})
    
    