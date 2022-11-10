from django.contrib import admin
from  .models import Item,Order,OrderItem,ShippingAddress,PaymentTransaction
# Register your models here.

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(PaymentTransaction)
