from rest_framework import routers
from django.urls import path
from .import views
router = routers.DefaultRouter()


app_name="stock"

urlpatterns = [ 
    path('getstock',views.getStockView,name="getStockView"),
    path('stock/<int:stockId>/<int:branchId>/<str:action>/<str:pgroup>',views.stockView,name="stockView"), 

]
urlpatterns += router.urls