from multiprocessing import context
from django.shortcuts import render,redirect, get_object_or_404
from pytz import timezone
from .models import Item,Order,OrderItem
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.views.generic import ListView,DetailView
# Create your views here.


def index(request):
    context = {
        "items":Item.objects.all()
    }
    return render(request,'index.html',context)
 


class shopView(ListView):
    model = Item
    template_name = "shop.html"


class productDetailsView(DetailView):
    model= Item
    template_name = "product-details.html"

def shop_cart(request):
    context = {
        "":""
    }

    return render(request,"shop-cart.html",context)


def checkout(request):
    context = {
        "":""
    }

    return render(request,"checkout.html",context)

def string_arts(request):
    context = {

    }
    return render(request,"string_arts.html")


def crotchets(request):
    context = {

    }
    return render(request,"crotchets.html")

def signuppage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form =CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("loginpage")

    context = {
        "form":form
    }
    return render(request,"auth/signup.html",context)


def loginpage(request):
    context = {

    }
    return render(request,"auth/login.html",context)

def add_to_cart(request, slug):
    item = get_object_or_404(Item,slug=slug)
    order_item = OrderItem.objects.get_or_create(item=item,user=request.user,ordered=False)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        #check if the prder item is in the order
        if order.items.filter(item__sulg=item.slug).exists():
            order_item.quantity +=1
            order_item.save()

        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
    
    return redirect("core:product-details",slug=slug)

