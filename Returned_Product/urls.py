from rest_framework import routers
from knox import views as KnoxView
from django.urls import path
from .import views
router = routers.DefaultRouter()


app_name="returnedproduct"

urlpatterns = [  
    path('<int:returnedProductId>/<str:action>/<str:pgroup>',views.returnedProductView,name="returnedProductView"),  

]
urlpatterns += router.urls