from django.contrib import admin
from .models import *

admin.site.register(CustomClient)
admin.site.register(Toppings)
admin.site.register(Pizza)
admin.site.register(Orders)
admin.site.register(ItemOrder)
admin.site.register(DeliveryAdress)
