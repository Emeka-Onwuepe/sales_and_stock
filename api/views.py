from datetime import date
from decimal import Decimal
from rest_framework import permissions,generics,status
from rest_framework.response import Response
from Branch.models import Branch

from Credit_Sales.models import Payment,Credit_Sale
from Product.models import (Category,Product_Type,Size,
                                Product,Suit,Top,Foot_Wear)
from Product.serializer import (CategorySerializer,ProductTypeSerializer,
                                SizeSerializer,ProductSerializer,
                                SuitSerializer,TopSerializer,
                                FootWearSerializer)
from Sales.models import Items,Sales
from Stock.models import Foot_Wear_Stock, Product_Stock, Suit_Stock, Tops_Stock
from User.models import Customer
from User.serializer import CustomerSerializer, Get_User_Serializer, Login_Serializer

import json
from django.http import JsonResponse
from knox.models import AuthToken
# models = [Customer,Category,Product_Type,Size,
#           Product,Suit,Top,Foot_Wear,Items,
#           Sales,Credit_Sale,Payment
#           ]

models = {'category':[Category,CategorySerializer],
          'product_type':[Product_Type,ProductTypeSerializer],
          'size':[Size,SizeSerializer],
          'product':[Product,ProductSerializer],
          'suit':[Suit,SuitSerializer],
          'top':[Top,TopSerializer],
          'foot_wear':[Foot_Wear,FootWearSerializer],
          'customer':[Customer,CustomerSerializer]
          }

# Create your views here.
class Get_All(generics.GenericAPIView):
    
    # permission_classes = [permissions.IsAuthenticated]
 

    def get(self, request , *args, **kwargs):
        # permission_classes = [permissions.IsAuthenticated]
        model = request.query_params['model']

        model_data = models[model][0].objects.all()
        data = models[model][1](model_data,many=True).data
            
        return Response({'data':data})

class Get_Branch(generics.GenericAPIView):
    
    def get(self, request , *args, **kwargs):
        # permission_classes = [permissions.IsAuthenticated]
        name = request.query_params['name']

        branch = Branch.objects.get(name=name)
        data = branch.id
            
        return Response({'id':data})
    
class LoginUser(generics.GenericAPIView):
    serializer_class = Login_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        _, token = AuthToken.objects.create(user)
        returnedUser = Get_User_Serializer(user)
        return Response({"user": returnedUser.data, "token": token})
    

class processSalesView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        # user = request.user
        data = request.data

        customer_instance = None
        credit_or_sales = None
        sale_type = None
    #    data = json.loads(request.body.decode("utf-8"))
        orderlist = data['orders']
       
        mapper = {'product':[Product],
              'suit':[Suit],
              'top':[Top],
              'foot_wear':[Foot_Wear],
              }
        branch = Branch.objects.get(pk=int(data['branch']))
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
            credit_or_sales = Credit_Sale.objects.create(branch=branch,
                                               total_amount=float(data['total_amount']),
                                               expected_amount=float(data['expected_price']),
                                               remark = data['remark'],
                                               customer = customer_instance,
                                               purchase_id = data['purchase_id'])
        else:
            credit_or_sales = Sales.objects.create(branch=branch,
                                               total_amount=data['total_amount'],
                                               expected_amount=data['expected_price'],
                                               remark = data['remark'],
                                               channel ="store",
                                               customer = customer_instance,
                                               payment_method = data['payment_method'],
                                               purchase_id = data['purchase_id'])
            sale_type = credit_or_sales.payment_method
       
        for item in orderlist:
           
            pgroup = item['p_group']
            target = f'{pgroup}_id'
            product = mapper[pgroup][0].objects.get(pk=int(item[target]))
            size = Size.objects.get(pk=int(item['size_id']))
            
            
            if pgroup == 'suit':
                Item =  Items.objects.create(suit=product,product_type=item['product_type'],
                                             p_group = pgroup,size_instance=size,
                                             qty=item['qty'],
                                            unit_price=item['unit_price'],total_price=item['total_price'],
                                            mini_price=item['mini_price'],expected_price=item['expected_price'])
            elif pgroup == 'top':
                Item =  Items.objects.create(top=product,product_type=item['product_type'],
                                             p_group = pgroup,size_instance=size,
                                             qty=item['qty'],
                                            unit_price=item['unit_price'],total_price=item['total_price'],
                                            mini_price=item['mini_price'],expected_price=item['expected_price'])
            elif pgroup == 'product':
                Item =  Items.objects.create(product=product,product_type=item['product_type'],
                                             p_group = pgroup,size_instance=size,
                                             qty=item['qty'],
                                            unit_price=item['unit_price'],total_price=item['total_price'],
                                            mini_price=item['mini_price'],expected_price=item['expected_price'])
            elif pgroup == 'foot_wear':
                Item =  Items.objects.create(foot_wear=product,product_type=item['product_type'],
                                             p_group = pgroup,size_instance=size,
                                             qty=item['qty'],
                                            unit_price=item['unit_price'],total_price=item['total_price'],
                                            mini_price=item['mini_price'],expected_price=item['expected_price'])
            
            credit_or_sales.items.add(Item)
         
           
        return Response({"purchase_id":credit_or_sales.purchase_id,
                            "type":sale_type})
        
class creditPaymentView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        # user = request.user
        data = request.data
        credit_sale = Credit_Sale.objects.get(purchase_id = data['purchase_id'])
        Payment.objects.create(credit_sale=credit_sale,amount=Decimal(data['amount']))
        
        return Response({'id':data['id']})
    
class addProductView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        # user = request.user
        data = request.data
        mapper = {'product':[Product],
              'suits':[Suit],
              'top':[Top],
              'foot_wear':[Foot_Wear],
              }
        status = 'success'
        for product in data['data']:
            try:
                Category_instance,cat_created= Category.objects.get_or_create(name=product['product'])
                
                p_type,p_type_created = Product_Type.objects.get_or_create(name=product['category'],
                                                category = Category_instance,
                                                p_group = product['p_group']
                                                )
                price = 45_000
                product.pop('category')
                product.pop('p_group')
                product.pop('product')
                size = product.pop('size')
                if product.get('price'):
                    price = product.pop('price')
                
                product['product_type_id'] = p_type.id
               
                product_instance,product_instance_created = mapper[p_type.p_group][0].objects.get_or_create(**product)
               
                size_instance = Size.objects.get(size=size,gender=product['gender'],
                                        age_group = product['age_group'],
                                        product_type_id = product['product_type_id'] )
                product_instance.sizes.add(size_instance)
            except Product_Type.DoesNotExist:
                status = 'Product Type not Found'
            except Size.DoesNotExist:
                size_instance = Size.objects.create(size=size,gender=product['gender'],
                                        age_group = product['age_group'],
                                        product_type_id = product['product_type_id'],
                                        price=price)
                product_instance.sizes.add(size_instance)   
        return Response({"status":status})
        
class addStockView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        # user = request.user
        data = request.data
       
        mapper = {'product':[Product,Product_Stock],
              'suits':[Suit,Suit_Stock],
              'top':[Top,Tops_Stock],
              'foot_wear':[Foot_Wear,Foot_Wear_Stock],
              }
        status = 'success'
        for product in data['data']:
            try:
                p_type = Product_Type.objects.get(name__iexact=product['product_type_id'],
                                                category__name__iexact=product['category'])
                product.pop('category')
                size = product.pop('size')
                qty = product.pop('qty')
                product['product_type_id'] = p_type.id
                product_instance = mapper[p_type.p_group][0].objects.get(**product)
                size_instance = Size.objects.get(size=size,gender=product['gender'],
                                        age_group = product['age_group'],
                                        product_type_id = product['product_type_id'] )
                branch = Branch.objects.get(name__iexact = data['branch'])
                
                check =  mapper[p_type.p_group][1].objects.filter(branch = branch,
                                                          product = product_instance,
                                                          size_instance = size_instance,
                                                          qty = qty,
                                                          date__icontains = date.today()
                                                          )
                if check:
                    continue
                mapper[p_type.p_group][1].objects.create(branch = branch,
                                                          product = product_instance,
                                                          size_instance = size_instance,
                                                          qty = qty
                                                          )
                
            except Product_Type.DoesNotExist:
                status = 'Product Type not Found'
            except mapper[p_type.p_group][0].DoesNotExist:
                status = 'Product not Found'
            except Size.DoesNotExist:
                status = 'Size Does Not Exist' 
            except Branch.DoesNotExist:
                status = 'Branch Does Not Exist'   
        return Response({"status":status})   
        
