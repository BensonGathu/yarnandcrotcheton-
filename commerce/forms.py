from dataclasses import field
from http.client import PAYMENT_REQUIRED
from itertools import count
from pyexpat import model
from tkinter import Widget
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField



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