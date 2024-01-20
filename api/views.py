from rest_framework import permissions,generics,status
from rest_framework.response import Response

from Credit_Sales.models import Payment,Credit_Sale
from Product.models import (Category,Product_Type,Size,
                                Product,Suit,Top,Foot_Wear)
from Product.serializer import (CategorySerializer,ProductTypeSerializer,
                                SizeSerializer,ProductSerializer,
                                SuitSerializer,TopSerializer,
                                FootWearSerializer)
from Sales.models import Items,Sales
from User.models import Customer
from User.serializer import CustomerSerializer


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