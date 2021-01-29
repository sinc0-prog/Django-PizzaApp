from .models import *
from django.contrib.auth import *

def item_in_cart(request):
    item_in_cart = 0
    try:
        item_cart = Orders.objects.get(client = request.user, order_status = 'IN CART')
        item_in_cart = item_cart.get_cart_items  
    except Exception: pass
    return {"item_in_cart": item_in_cart }