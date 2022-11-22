from atexit import register
from django import template
from commerce.models import Order,OrderItem
register = template.Library()




@register.simple_tag
def display_order_items(orderitem,user):
    qs = OrderItem.objects.filter(item=orderitem,user=user)
    if qs.exists():
        return qs
    return None