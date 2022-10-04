from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static

from .views import index, productDetailsView,shop_cart,shopView,add_to_cart,checkout,signuppage,loginpage,string_arts,crotchets
# app_name = 'commerce'
urlpatterns = [ 
    
    path("",index,name="index"),
    path("shop",shopView.as_view(),name="shop"),
    path("shop-cart",shop_cart,name="shop-cart"),
    path("product-details/<slug>/",productDetailsView.as_view(),name="product-details"),
    path("add-to-cart/<slug>/",add_to_cart,name="add-to-cart"),
    path("string-arts",string_arts,name="string-arts"),
    path("crotchets",crotchets,name="crotchets"),
    path("checkout",checkout,name="checkout"),
    path("signuppage",signuppage,name="signuppage"),
    path("loginpage",loginpage,name="loginpage"),

] 

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)