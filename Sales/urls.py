from rest_framework import routers
from knox import views as KnoxView
from django.urls import path
from .import views
router = routers.DefaultRouter()


app_name="sales"

urlpatterns = [
    
    # path('<int:branchId>/<str:action>',views.branchView,name="branchView"), 
      
]
urlpatterns += router.urls