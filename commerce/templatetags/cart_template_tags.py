from atexit import register
from django import template
from commerce.models import Order
register = template.Library()




@register.simple_tag
def cart_item_count(user):
    if user.is_authenticated(user):
        qs = Order.objects.filter(user=user,ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0