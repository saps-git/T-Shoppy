from rest_framework import routers
from django.urls import path, include

from . import views

router = routers.DefaultRouter()
router.register(r'', views.ProductViewSet) #r'' = registering the home path, i.e api/product/ in the router

urlpatterns = [
    path('', include(router.urls))
]