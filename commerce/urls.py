from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static

from .views import index, productDetailsView,shop_cart,remove_from_cart,shopView,orders,add_to_cart,signuppage,loginpage,logoutUser,crotchetsView,remove_single_item_from_cart,checkoutview,PaymentView,stringArtsView,yarnAccessoriesView,adminDash,admin_allproductsView,admin_crotchetbagsView,admin_crotchetproductsView,admin_stringsView,admin_yarnView,delete_product,AddProductView,crotchetBagsView,crotchetProductsView
app_name = 'commerce'
urlpatterns = [ 
    
    path("",index,name="index"),
    path("shop",shopView.as_view(),name="shop"),
    path("shop-cart",shop_cart.as_view(),name="shop-cart"),
    path("product-details/<slug>/",productDetailsView.as_view(),name="product-details"),
    path("add-to-cart/<slug>/",add_to_cart,name="add-to-cart"),
    path("remove-from-cart/<slug>/",remove_from_cart,name="remove-from-cart"),
    path("remove_single_item_from_cart/<slug>/",remove_single_item_from_cart,name="remove_single_item_from_cart"),
    path("string-arts",stringArtsView.as_view(),name="string-arts"),
    path("crotchets",crotchetsView.as_view(),name="crotchets"),
    path("crotchetBags",crotchetBagsView.as_view(),name="crotchetbags"),
    path("crotchetProducts",crotchetProductsView.as_view(),name="crotchetproducts"),
    path("yarnaccessories",yarnAccessoriesView.as_view(),name="yarnaccessories"),
    path("checkout",checkoutview.as_view(),name="checkout"),
    path("orders",orders,name="orders"),
    path("signuppage",signuppage,name="signuppage"),
    path("loginpage",loginpage,name="loginpage"),
    path('logout/', logoutUser, name='logout'),
    # path('daraja/stk-push', stk_push_callback, name='mpesa_stk_push_callback'),
    # path('mpesa/', mpesaPayment, name='mpesa'),
    path('payment/<payment_option>/',PaymentView.as_view(),name="payment"),
    path('adminDash/',adminDash,name="admin-dashboard"),
    path('adminproducts/',admin_allproductsView.as_view(),name="admin_allproducts"),
    path('admincrotchetbags/',admin_crotchetbagsView.as_view(),name="admin_crotchetbags"),
    path('admincrotchetproducts/',admin_crotchetproductsView.as_view(),name="admin_crotchetproducts"),
    path('adminstringarts/',admin_stringsView.as_view(),name="admin_stringarts"),
    path('adminyarn/',admin_yarnView.as_view(),name="admin_yarn"),
    path("delete_product/<slug>/",delete_product,name="delete_product"),
    path("addProduct/",AddProductView.as_view(),name="add_product"),


] 

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)