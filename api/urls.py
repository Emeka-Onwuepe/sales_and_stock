from rest_framework import routers
from django.urls import path
from knox import views as KnoxView

from api.views import (Get_All, Get_Branch,processSalesView,
                       LoginUser,creditPaymentView,addProductView,
                       addStockView,PublishView)
router = routers.DefaultRouter()

app_name = 'api'

urlpatterns = [
    path('getall', Get_All.as_view(), name="get_all"),
    path('getbranch', Get_Branch.as_view(), name="get_branch"),
    path('logout', KnoxView.LogoutView.as_view(), name="knox_logout"),
    path('process',processSalesView.as_view(),name="processSalesView"),
    path('login', LoginUser.as_view(), name="login"),
    path('creditpayment',creditPaymentView.as_view(),name='creditPayment'),
    path('addproduct',addProductView.as_view(),name='addProductView'),
    path('addstock',addStockView.as_view(),name='addstockView'),
    path('publish',PublishView.as_view(),name='PublishView')
    
           
]

urlpatterns += router.urls