from ast import mod
import uuid
from distutils.command.upload import upload
from email.policy import default
from random import choices
from sre_constants import CATEGORY
from statistics import mode
from tokenize import blank_re
from turtle import title
from unicodedata import category
from unittest import result
from unittest.util import _MAX_LENGTH
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.forms import IntegerField
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
 

CATEGORY_CHOICES = (
    ("String Art","String Art"),
    ("Crotchet Products","Crotchet Products"),
    ("Crotchet Bag","Crotchet Bag"),
    ("Yarn & Accessories","Yarn & Accessories")

)
LABEL_CHOICES = (
    ("P","primary"),
    ("S","secondary"),
    ("D","danger")
)

class Item(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()
    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=100)
    image = models.ImageField(null=False,blank=False,upload_to="products")
    image1 = models.ImageField(null=True, blank=True,upload_to="products")
    image2 = models.ImageField(null=True, blank=True,upload_to="products")
    image3 = models.ImageField(null=True, blank=True,upload_to="products")
    image4 = models.ImageField(null=True, blank=True,upload_to="products")
    label = models.CharField(choices=LABEL_CHOICES,max_length=100)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/product-details/{self.slug}"

        # return reverse("product-details",kwargs={
        #     'slug':self.slug
        # })

    def get_item_to_cart_url(self):
        return f"/add-to-cart/{self.slug}"

    def get_remove_from_cart_url(self):
        return f"/remove-from-cart/{self.slug}"

    def get_delete_item_url(self):
        return f"/delete_product/{self.slug}"
    

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_item_total_price(self):
        return self.item.price * self.quantity

    def get_item_discount_price(self):
        return self.item.discount_price * self.quantity

    def get_amount_saved(self):
        return self.get_item_total_price() - self.get_item_discount_price()

    def get_final_total(self):
        if self.item.discount_price:
            return self.get_item_discount_price()
        else:
            return self.get_item_total_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey('ShippingAddress',on_delete=models.SET_NULL,null=True,blank=True)
    delivered = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username
    
    def get_order_total(self): 
        total=0
        for order_item in self.items.all():
            total += order_item.get_final_total()
            print("total")
        return total

class ShippingAddress(models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    town= models.CharField(max_length=100)
    street_address= models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    zip =models.CharField(max_length=100)
    phone  =models.IntegerField()
    email =models.EmailField()
    order_notes=models.CharField(max_length=100)
    payment_option = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username



STATUS = ((1, "Pending"), (0, "Complete"))
"""This model records all the mpesa payment transactions"""
class PaymentTransaction(models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    transaction_no = models.CharField(default=uuid.uuid4, max_length=50, unique=True)
    phone_number = IntegerField()
    checkout_request_id = models.CharField(max_length=200)
    reference = models.CharField(max_length=40, blank=True)
    description = models.TextField(null=True, blank=True)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=15, choices=STATUS, default=1)
    receipt_no = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return f"{self.transaction_no}"



class Gallery(models.Model):
    pass


class MpesaPaymentAPI(models.Model):
    pass

class CallBackURL(models.Model):
    CallbackMetadata = models.CharField(max_length=600)
    CheckoutRequestID = models.CharField(max_length=600)
    MerchantRequestID = models.CharField(max_length=600)
    ResultCode = models.CharField(max_length=600)
    ResultDesc = models.CharField(max_length=600)
    


# {
# "CallbackMetadata":"CallbackMetadata",
# "CheckoutRequestID":"CheckoutRequestID",
# "MerchantRequestID":"MerchantRequestID",
# "ResultCode":"ResultCode",
# "ResultDesc":"ResultDesc"
# }