from email import message
from multiprocessing import context
from unicodedata import category
from django.shortcuts import render,redirect, get_object_or_404
from django.views import View
from pytz import timezone
from requests import request
from .models import Item,Order,OrderItem,ShippingAddress
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm,CheckoutForm,AddProductForm
from django.views.generic import ListView,DetailView
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from django_daraja.mpesa.core import MpesaClient
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from .serializers import MpesaCheckoutSerializer
from bootstrap_modal_forms.generic import BSModalCreateView

# from .util import MpesaGateWay



# Create your views here.

#homepage
def index(request):
    
    context = {
        "items":Item.objects.all()
    }
    return render(request,'index.html',context)
 

#includes all products
class shopView(ListView):
    paginate_by=10
    model = Item
   
    template_name = "shop.html"

#individual products details
class productDetailsView(LoginRequiredMixin ,DetailView):
    model= Item
    template_name = "product-details.html"
    # images = Item.objects.get()



class shop_cart(LoginRequiredMixin,View):
    model=Order
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            context={
                "order":order
            }
            return render(self.request,"shop-cart.html",context)
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have an active order")
            return redirect("commerce:index")


class checkoutview(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        form = CheckoutForm()
        context = {
        "form": form
        }
        return render(self.request, "checkout.html",context)

    def post(self,*args,**kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=request.user,ordered=False)
            if form.is_valid():
                firstname = form.cleaned_data.get("firstname")
                lastname = form.cleaned_data.get("lastname")
                county = form.cleaned_data.get("county")
                town = form.cleaned_data.get("town")
                street_address = form.cleaned_data.get("street_address")
                apartment_address = form.cleaned_data.get("apartment_address")
                zip = form.cleaned_data.get("zip")
                phone = form.cleaned_data.get("phone")
                email = form.cleaned_data.get("email")
                # save_info = form.cleaned_data.get("save_info")
                payment_option = form.cleaned_data.get("payment_option")
                order_notes = form.cleaned_data.get("order_notes")
                
                shippingaddress = ShippingAddress(
                    user = request.user,
                    firstname=firstname,
                    lastname= lastname,
                    county=county,
                    town=town,
                    street_address= street_address,
                    apartment_address=apartment_address,
                    zip=zip,
                    phone=phone,
                    email=email,
                    order_notes= order_notes
                )
                shippingaddress.save()
                order.shipping_address = shippingaddress
                order.save()

                return redirect("commerce:checkout")

            messages.warning(self.request,"Failed Checkout")
            return redirect("commerce:checkout")

        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have an active order")
            return redirect("commerce:checkout")

class PaymentView(View):
    def get(self,*args,**kwargs):
        return render(self.request,"payment.html")

class stringArtsView(ListView):
    model=Item
    queryset  = Item.objects.filter(category='String Art')
    context = {

    }
    template_name="string_arts.html"


class crotchetsView(ListView):
    model = Item
    queryset=Item.objects.filter(category='Crotchet Products') | Item.objects.filter(category='Crotchet Bag')
    

    template_name ="crotchets.html"


class yarnAccessoriesView(ListView):
    model=Item
    queryset  = Item.objects.filter(category='Yarn & Accessories')
    context = {

    }
    template_name="yarnaccessories.html"

@login_required
def orders(request):
    context = {

    }

    return render(request,"orders.html")


#userRegistration page
def signuppage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form =CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registered Successfully. Login to continue")
            return redirect("commerce:loginpage")

    context = {
        "form":form
    }
    return render(request,"auth/signup.html",context)

#userloginpage
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username,
                            password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in as' + ' ' + username)
            return redirect("commerce:index")
            # if user.is_admin:
            #     return redirect('dashboard')
            # if user.is_customer:
            #     return redirect('home')
        else:
            messages.error(request, 'Invalid Username and/or Password')

    context = {}
    return render(request, 'auth/login.html', context)

def logoutUser(request):
    current_user = request.user
    logout(request)
    messages.info(
        request, 'You have logged out.')  
    # if current_user.is_admin:
    return redirect('"commerce:index')
    

#adding an item to cart

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item,slug=slug)
    order_item ,created= OrderItem.objects.get_or_create(item=item,user=request.user,ordered=False)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            if order_item.quantity >=1:
                order_item.quantity +=1
                order_item.save()
            else:
                order_item.quantity =1
                order_item.save()
            messages.success(request,"Item updated Successfully")


        else:
            messages.success(request,"Item added Successfully")
            order.items.add(order_item)
            order_item.quantity +=1

            order_item.save()
    else:
        ordered_date = datetime.now()
        order = Order.objects.create(
            user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
    
    return redirect("commerce:shop-cart")

#removing an item from the cart

@login_required
def remove_from_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        print("order",order)
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item,user=request.user,ordered=False)[0]
            order_item.quantity =0
            order.items.remove(order_item)
            order_item.save()
            messages.success(request,"Item removed Successfully")

        else:
            #add a message saying the order does not contain the item
            messages.warning(request, 'The Item Is not in your order')
            return redirect("commerce:shop-cart")
    else:
        #add a message saying the user does not have an order
        messages.warning(request, 'You have no order')
        return redirect("commerce:shop-cart")
    return redirect("commerce:shop-cart")


@login_required
def remove_single_item_from_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        print("order",order)
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item,user=request.user,ordered=False)[0]
            if  order_item.quantity >1:
                order_item.quantity -=1
                order_item.save()
            else:
                order.items.remove(order_item)   
            messages.success(request,"Item updated Successfully")

        else:
            #add a message saying the order does not contain the item
            messages.warning(request, 'The Item Is not in your order')
            return redirect("commerce:shop-cart")
    else:
        #add a message saying the user does not have an order
        messages.warning(request, 'You have no order')
        return redirect("commerce:shop-cart")
    return redirect("commerce:shop-cart")


#delete an item from the database
def delete_product(request,slug):
    item = get_object_or_404(Item,slug=slug)
    print(item)
    if item:
        item.delete()
        messages.success(request,"Item Deleted successfully")
        return redirect("commerce:admin-dashboard")
    else:
        messages.warning(request,"Item does not exist")
        return redirect("commerce:admin-dashboard")

# def payment(request):
#     url = "https://sandbox.safaricom.co.ke/oauth/v1/generate"
#     querystring = {"grant_type":"client_credentials"}
#     payload = ""
#     headers = {
#     "Authorization": "Basic SWZPREdqdkdYM0FjWkFTcTdSa1RWZ2FTSklNY001RGQ6WUp4ZVcxMTZaV0dGNFIzaA=="
#     }
#     response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
#     print(response.text)



def mpesaPayment(request):
    cl = MpesaClient()
    print(cl)
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = '0703446950'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://darajambili.herokuapp.com/express-payment'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)    

def stk_push_callback(request):
        data = request.body
        # You can do whatever you want with the notification received from MPESA here. 


#admin Dashboard page
def adminDash(request):
    context = {

    }
    return render(request,'adminDash/index.html',context)


#admin all products page
class admin_allproductsView(View):
    def get(self,*args,**kwargs):
        form = AddProductForm()
        object_list = Item.objects.all()
        context = {
            "form":form,
            "object_list":object_list
        }

        return render(self.request, "adminDash/admin_allproducts.html",context)

    def post(self,*args,**kwargs):
        form = CheckoutForm(self.request.POST or None)
        pass
        model=Item
        context = {

        }
        template_name=  'adminDash/admin_allproducts.html'



    
#admin crotchetbags page
class admin_crotchetbagsView(ListView):
    model=Item
    context = {

    }
    template_name =  'adminDash/admin_crotchetbags.html'


#admin crotchetproducts page
class admin_crotchetproductsView(ListView):
    model=Item
    context = {

    }
    template_name = 'adminDash/admin_crotchetproducts.html'


#admin string arts page
class admin_stringsView(ListView):
    model=Item
    context = {

    }
    template_name = 'adminDash/admin_strings.html'

#admin yarn and accessories page
class admin_yarnView(ListView):
    model=Item
    context = {

    }
    template_name = 'adminDash/admin_yarn.html'



class AddProductView(BSModalCreateView):
    template_name = 'examples/create_book.html'
    form_class = AddProductForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')