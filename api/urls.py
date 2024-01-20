from rest_framework import routers
from django.urls import path
from knox import views as KnoxView

from api.views import Get_All
router = routers.DefaultRouter()

app_name = 'api'

urlpatterns = [
    path('getall', Get_All.as_view(), name="get_all"),
    path('logout', KnoxView.LogoutView.as_view(), name="knox_logout"),
           
]

urlpatterns += router.urls