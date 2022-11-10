from atexit import register
from django import template
from commerce.models import Order, Item
register = template.Library()

@register.simple_tag

def show_related_items(category):
    items = []
    queryset=Item.objects.filter(category=str(category))
    for item in queryset:
        items.append(item)
    return items
