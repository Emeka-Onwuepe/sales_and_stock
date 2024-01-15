from rest_framework import routers
from knox import views as KnoxView
from django.urls import path
from .import views
router = routers.DefaultRouter()


app_name="badproduct"

urlpatterns = [  
    path('<int:badProductId>/<str:action>/<str:pgroup>',views.badProductView,name="badProductView"),  

]
urlpatterns += router.urls