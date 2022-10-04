from email.policy import default
from random import choices
from sre_constants import CATEGORY
from statistics import mode
from turtle import title
from unicodedata import category
from unittest import result
from unittest.util import _MAX_LENGTH
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.template.defaultfilters import slugify


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
    label = models.CharField(choices=LABEL_CHOICES,max_length=100)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Item, self).save(*args, **kwargs)

    def __str_(self):
        return self.title

    def get_absolute_url(self):
        return f"/product-details/{self.slug}"

        # return reverse("core:product-details",kwargs={
        #     'slug':self.slug
        # })

    def get_item_to_cart_url(self):
        return f"/add-to-cart/{self.slug}"

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.ImageField(default=1)


    def __str_(self):
        return f"{self.quantity} of {self.item.title}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str_(self):
        return self.user.username

