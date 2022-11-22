from django.db import models
from commerce.models import Order
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.


class Delivery(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    orders = models.ForeignKey(Order,on_delete=models.DO_NOTHING)
    shipped = models.BooleanField(default=False)
    route = models.BooleanField(default=False)
    arrived = models.BooleanField(default=False)




    def __str__(self):
        return '{} Delivery on {}'.format(self.user.username,{})
