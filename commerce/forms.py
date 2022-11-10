from dataclasses import field
from http.client import PAYMENT_REQUIRED
from itertools import count
from pyexpat import model
from sre_constants import CATEGORY
from tkinter import Widget
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from bootstrap_modal_forms.forms import BSModalModelForm
import phonenumbers



from commerce.models import CATEGORY_CHOICES, Item
# from django_countries.widgets import CountrySelectWidget
# from django_countries.fields import CountryField



class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":'form-control my-2', 'placeholder':'Enter username','type':'text'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Enter email','type':'email'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Enter password','type':'password'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Confirm password','type':'password'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']



PAYMENT_CHOICES = (
    ("S","Stripe"),
    ("P","PayPal"),
    ("M","M-Pesa")
)

class CheckoutForm(forms.Form):
    firstname = forms.CharField(widget=forms.TextInput(attrs={"class":'form-control my-2', 'placeholder':'First Name','type':'text'}))
    lastname = forms.CharField(widget=forms.TextInput(attrs={"class":'form-control my-2', 'placeholder':'Last Name','type':'text'}))
    # country = CountryField(blank_label='(select country)').formfield(Widget=CountrySelectWidget(attrs={"class":'custom-select d-block w-100'}))
    county = forms.CharField(widget=forms.TextInput(attrs={"class":'form-control my-2', 'placeholder':'County','type':'text'}))
    town = forms.CharField(widget=forms.TextInput(attrs={"class":'form-control my-2', 'placeholder':'Town','type':'text'}))
    street_address = forms.CharField(widget=forms.TextInput(attrs={"class":'form-control my-2', 'placeholder':'Address','type':'text'}))
    apartment_address = forms.CharField(widget=forms.TextInput(attrs={"class":'form-control my-2', 'placeholder':'Apartment','type':'text'}),required=False)
    zip = forms.CharField(widget=forms.TextInput(attrs={"class":'form-control my-2', 'placeholder':'Postal Code / Zip','type':'text'}))
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={"class":'form-control my-2', 'placeholder':'PhoneNumber','type':'text'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":'form-control my-2', 'placeholder':'Email','type':'text'}),required=False)
    save_info = forms.BooleanField(widget=forms.CheckboxInput(),required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(),choices=PAYMENT_CHOICES)
    order_notes = forms.CharField(widget=forms.TextInput(attrs={"class":'form-control my-2', 'placeholder':' Note about your order, e.g, special note for delivery','type':'text'}),required=False)



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
class AddProductForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"class":'form-control my-2', 'placeholder':'Product name','type':'text'}))
    desc = forms.CharField(widget=forms.Textarea(attrs={"class":'form-control my-2', 'placeholder':'Product Description','type':'text','rows':3,'cols':45}))
    price = forms.FloatField(widget=forms.NumberInput(attrs={"class":'form-control my-2', 'placeholder':'price','type':'text'}))
    discounted_price = forms.FloatField(widget=forms.NumberInput(attrs={"class":'form-control my-2', 'placeholder':'discounted price','type':'text','rows':4,"cols":"4"}))
    category = forms.ChoiceField(label='select category', choices=CATEGORY_CHOICES, widget=forms.Select(attrs={"class": "form-control"}))
    label = forms.ChoiceField(label='select label', choices=LABEL_CHOICES, widget=forms.Select(attrs={"class": "form-control"}))
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={"class": "form-control"}))
    image1 = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control"}),required=False)
    image2 = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control"}),required=False)
    image3 = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control"}),required=False)
    image4 = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control"}),required=False)
   

    class Meta:
        model = Item
        fields = ['title','desc','price','discounted_price','category','image','image1','image2','image3','image4','label']


class PaymentForm(forms.Form):
    phonenumber = forms.IntegerField(widget=forms.NumberInput(attrs={"class":'form-control my-2', 'placeholder':'Enter Number to pay','type':'text'}))
    amount = forms.FloatField(widget=forms.NumberInput(attrs={"class":'form-control my-2', 'placeholder':'price','type':'text'}))