from ast import Pass
from cProfile import label
from email import message
from multiprocessing import context
from turtle import title
from unicodedata import category
from django.shortcuts import render,redirect, get_object_or_404
from django.views import View
import phonenumbers
from pytz import timezone
from requests import request
from .models import Item,Order,OrderItem,ShippingAddress
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm,CheckoutForm,AddProductForm,PaymentForm
from django.views.generic import ListView,DetailView
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
# from django_daraja.mpesa.core import MpesaClient
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from .serializers import MpesaCheckoutSerializer
from bootstrap_modal_forms.generic import BSModalCreateView
from .mpesa import lipa_na_mpesa

# from .util import MpesaGateWay



# Create your views here.

#homepage
def index(request):
    items = Item.objects.all(),
    
    new_crotchets = Item.objects.filter(category='Crotchet Products').first() 
    new_bag = Item.objects.filter(category='Crotchet Bag').order_by('-id').first()
    new_art = Item.objects.filter(category='String Art').order_by('-id').first()
    new_acc = Item.objects.filter(category='Yarn & Accessories').order_by('-id').first()
    print(new_bag)
    context = {
        "items":items,
        "new_crotchets": new_crotchets,
        "new_art":new_art,
        "new_acc":new_acc,
        "new_bag":new_bag,

    }
    return render(request,'index.html',context)
 

#includes all products
class shopView(ListView):
    paginate_by=10
    model = Item
    queryset=Item.objects.all().order_by('-id')
   
    template_name = "shop.html"

#individual products details
class productDetailsView(DetailView):
    model= Item
    template_name = "product-details.html"
    # images = Item.objects.get()



class shop_cart(View):
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
    model=Order
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            form = CheckoutForm()
            context = {
            "form": form,
            "order":order
            }
            return render(self.request, "checkout.html",context)
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have an active order")
            return redirect("commerce:index")
            

    def post(self,*args,**kwargs):
        form = CheckoutForm(self.request.POST or None)
        paymentForm =  PaymentForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            context = {

            "paymentForm": paymentForm,
            "order":order
            }
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
                    user = self.request.user,
                    firstname=firstname,
                    lastname= lastname,
                    county=county,
                    town=town,
                    street_address= street_address,
                    apartment_address=apartment_address,
                    zip=zip,
                    phone=phone,
                    email=email,
                    order_notes= order_notes,
                    payment_option=payment_option,
                )
                shippingaddress.save()
                order.shipping_address = shippingaddress
                order.save()
                context = {
                "paymentForm": paymentForm,
                "order":order
                    }
                if shippingaddress.payment_option == "M":
                    print(shippingaddress.payment_option)
                    return redirect("commerce:payment",str(shippingaddress.payment_option))

                elif shippingaddress.payment_option == "P":
                    pass

                elif shippingaddress.payment_option == "S":
                    pass

                

            messages.warning(self.request,"Failed Checkout")
            return redirect("commerce:checkout")

        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have an active order")
            return redirect("commerce:checkout")

class PaymentView(View):
    model=Order
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            paymentForm = PaymentForm()
            context = {
            "paymentForm": paymentForm,
            "order":order
            }
          
            return render(self.request, "payment.html",context)
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have an active order")
            return redirect("commerce:index")
    def post(self,*args,**kwargs):
        paymentForm =  PaymentForm(self.request.POST or None, self.request.FILES)
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            
            context = {
            "paymentForm": paymentForm,
            "order":order
            }
            phonenumber = self.request.POST.get("phonenumber")
            amount = order.get_order_total()
           
            lipa_na_mpesa(amount,phonenumber)
            
           
                
                

            return render(self.request,"payment.html",context)
            print("NOT VALID")
            return redirect("commerce:checkout")
        

        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have an active order")
            return redirect()
            

class stringArtsView(ListView):
    model=Item
    queryset  = Item.objects.filter(category='String Art').order_by('-id')
    context = {

    }
    template_name="string_arts.html"


class crotchetsView(ListView):
    model = Item
    queryset=Item.objects.filter(category='Crotchet Products') | Item.objects.filter(category='Crotchet Bag').order_by('-id')
    

    template_name ="crotchets.html"

class crotchetBagsView(ListView):
    model = Item
    queryset= Item.objects.filter(category='Crotchet Bag').order_by('-id')
    

    template_name ="crotchetsbags.html"

class crotchetProductsView(ListView):
    model = Item
    queryset= Item.objects.filter(category='Crotchet Products').order_by('-id')
    

    template_name ="crotchetsProducts.html"


class yarnAccessoriesView(ListView):
    model=Item
    queryset  = Item.objects.filter(category='Yarn & Accessories').order_by('-id')
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
    return redirect('commerce:index')
    

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
    
    if item:
        item.delete()
        messages.success(request,"Item Deleted successfully")
        return redirect("commerce:admin-dashboard")
    else:
        messages.warning(request,"Item does not exist")
        return redirect("commerce:admin-dashboard")




#admin Dashboard page
def adminDash(request):
    context = {

    }
    return render(request,'adminDash/index.html',context)


#admin all products page
class admin_allproductsView(View):
    paginate_by=1
    def get(self,*args,**kwargs):
        form = AddProductForm()
        object_list = Item.objects.all().order_by('-id')
        context = {
            "form":form,
            "object_list":object_list
        }

        return render(self.request, "adminDash/admin_allproducts.html",context)

    def post(self,*args,**kwargs):
        form = AddProductForm(self.request.POST or None, self.request.FILES)
        
        
        if form.is_valid():
            title = form.cleaned_data.get("title")
            desc = form.cleaned_data.get("desc")
            price = form.cleaned_data.get("price")
            discount_price = form.cleaned_data.get("discounted_price")
            category = form.cleaned_data.get("category")
            label = form.cleaned_data.get("label")
            image = form.cleaned_data.get("image")
            image1 = form.cleaned_data.get("image1")
            image2 = form.cleaned_data.get("image2")
            image3 = form.cleaned_data.get("image3")
            image4 = form.cleaned_data.get("image4")
            
            item = Item(
                title=title,
                desc=desc,
                price=price,
                discount_price=discount_price,
                category=category,
                label=label,
                image=image,
                image1=image1,
                image2=image2,
                image3=image3,
                image4=image4
            )
           
            
            return redirect("commerce:admin_allproducts")
        return redirect("commerce:checkout")


       



    
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