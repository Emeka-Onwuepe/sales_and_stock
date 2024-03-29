from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Branch.models import Branch, Product_Size
from Product.forms import  CategoryForm, FootWearForm, ProductForm, ProductTypeForm,  SizeForm, SuitForm, TopForm
from Product.models import Category, Foot_Wear, Product, Product_Type, Size, Suit, Top

# Create your views here.
@login_required(login_url="user:loginView")
def categoryView(request,categoryId,action):
    
    # categories = Category.objects.all()
    
    if categoryId != 0:   
        category_instance = Category.objects.get(id=categoryId)
    
    if request.method == "POST" and action == "add":
        form = CategoryForm(data= request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('product:categoryView',
            kwargs={"action":"view","categoryId":0}))
        else:
            return render(request,"product/category.html",
                  {"form":form,"categoryId":0})  
            
    if action == "edit":
        if request.method == "POST":
            form = CategoryForm(data= request.POST,files=request.FILES,instance=category_instance)
         
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('product:categoryView',
                        kwargs={"action":"view","categoryId":0}))
            else:
                return render(request,"product/category.html",
                  {"form":form,"categoryId":category_instance.id})
        else:
            return render(request,"product/category.html",
                  {"form":CategoryForm(instance=category_instance),
                   "categoryId":category_instance.id,"action":"edit",
                #    'categories':categories
                   })
    
    if action == "delete":
        category_instance.delete()
        return HttpResponseRedirect(reverse('product:categoryView',
            kwargs={"action":"view","categoryId":0}))
                 
    return render(request,"product/category.html",
                  {"form":CategoryForm(),"categoryId":0, 
                #    'categories':categories,
                   "action":"add"})
    

@login_required(login_url="user:loginView")
def productTypeView(request,productTypeId,action):
    
    productTypes = Product_Type.objects.all()
    
    if productTypeId != 0:   
        product_type_instance = Product_Type.objects.get(id=productTypeId)
    
    if request.method == "POST" and action == "add":
        form = ProductTypeForm(data= request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('product:productTypeView',
            kwargs={"action":"view","productTypeId":0}))
        else:
            return render(request,"product/product_type.html",
                  {"form":form,"productTypeId":0,"action":"view"})  
            
    if action == "edit":
        if request.method == "POST":
            form = ProductTypeForm(data= request.POST,instance=product_type_instance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('product:productTypeView',
                        kwargs={"action":"view","productTypeId":0}))
            else:
                return render(request,"product/product_type.html",
                  {"form":form,"productTypeId":product_type_instance.id})
        else:
            return render(request,"product/product_type.html",
                  {"form":ProductTypeForm(instance=product_type_instance),
                   "productTypeId":product_type_instance.id,"action":"edit",'productTypes':productTypes})
    
    if action == "delete":
        product_type_instance.delete()
        return HttpResponseRedirect(reverse('product:productTypeView',
            kwargs={"action":"view","productTypeId":0}))
                 
    return render(request,"product/product_type.html",
                  {"form":ProductTypeForm(),"productTypeId":0, 'productTypes':productTypes,"action":"add"})
  
    
@login_required(login_url="user:loginView")  
def sizeView(request,sizeId,action):
    
    sizes = Size.objects.all()
    form = SizeForm()
    
    if sizeId != 0:   
        size_instance = Size.objects.get(id=sizeId)
       
    
    if request.method == "POST" and action == "add":
        form = SizeForm(data= request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('product:sizeView',
            kwargs={"action":"view","sizeId":0}))
        else:
            return render(request,"product/size.html",
                  {"form":form,"sizeId":0,"action":"view"})  
            
    if action == "edit":
        if request.method == "POST":
            form = SizeForm(data= request.POST,instance=size_instance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('product:sizeView',
                        kwargs={"action":"view","sizeId":0}))
            else:
                return render(request,"product/size.html",
                  {"form":form,"sizeId":size_instance.id,"action":"edit",'sizes':sizes})
        else:
            return render(request,"product/size.html",
                  {"instance":size_instance,
                   "sizeId":size_instance.id,"action":"edit",'sizes':sizes})
    
    if action == "delete":
        size_instance.delete()
        return HttpResponseRedirect(reverse('product:sizeView',
            kwargs={"action":"view","sizeId":0}))
                 
    return render(request,"product/size.html",
                  {"form":form,"sizeId":0, 'sizes':sizes,"action":"add"})
    

@login_required(login_url="user:loginView")
def productView(request,productId,action,pgroup):
    mapper = {'product':[Product,ProductForm],
              'suits':[Suit,SuitForm],
              'top':[Top,TopForm],
              'foot_wear':[Foot_Wear,FootWearForm],
    
              }
    
    form = mapper[pgroup][1]()
    
    if productId != 0:   
        product_instance = mapper[pgroup][0].objects.get(id=productId)
        form = mapper[pgroup][1](instance=product_instance)
        
    if request.method == "POST" and action == "add":
        form = mapper[pgroup][1](data= request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            # product.sizes.all()
            return HttpResponseRedirect(reverse('product:productView',
            kwargs={"action":"view","productId":0,'pgroup':pgroup}))
        else:
            return render(request,"product/product.html",
                  {"form":form,"productId":0,"action":"add",
                   'pgroup':pgroup})  
            
    if action == "edit" and request.method == "POST":
            
        form = mapper[pgroup][1](data= request.POST,files=request.FILES,instance=product_instance)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('product:productView',
                        kwargs={"action":"view","productId":0,'pgroup':pgroup}))
        else:
            return render(request,"product/product.html",
                  {"form":form,"productId":product_instance.id,
                   "action":"edit",'pgroup':pgroup})
    elif action == "edit" and request.method == "GET":
        return render(request,"product/product.html",
                  {"product_instance":product_instance,
                   "productId":product_instance.id,"action":"edit",
                   'form':form,
                    'pgroup':pgroup})
    
    if action == "delete":
        product_instance.delete()
        return HttpResponseRedirect(reverse('product:productView',
            kwargs={"action":"view","productId":0,'pgroup':pgroup}))
                 
    products = mapper[pgroup][0].objects.all()
    return render(request,"product/product.html",
                  {"productId":0, 
                   'products':products,
                   "action":"add",
                    'form':form,
                   'pgroup':pgroup})
