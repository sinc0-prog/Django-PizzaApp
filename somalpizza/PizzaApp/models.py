from django.db import models
from django.contrib.auth.models import AbstractUser
from PayU.helpers import PayUHelper


SIZE_PIZZA = ((40, '40cm'), (50, '50cm'))

ORDER_STATUS = (
    ('IN CART', 'IN CART'),
    ('CONFIRMED', 'CONFIRMED'),
    ('IN PRODUCTION', 'IN PRODUCTION'),
    ('DELIVERING', 'DELIVERING'),
    ('DELIVERED', 'DELIVERED'),
    ('CANCELLED', 'CANCELLED')
)



class CustomClient(AbstractUser):
    city = models.CharField(max_length=64, blank=True,
                            null=True, verbose_name='City')
    post_code = models.CharField(
        max_length=10, verbose_name='Post-Code', null=True, blank=True)
    street = models.CharField(
        max_length=64, verbose_name='Street', null=True, blank=True)
    number_of_builing = models.CharField(
        max_length=64, verbose_name='Number of building', null=True, blank=True)
    flat_number = models.IntegerField(
        verbose_name='Flat\'s number', null=True, blank=True)
    phone_number = models.CharField(max_length=31, null=True, blank=True)

    # Define topings


class Toppings(models.Model):
    name = models.CharField(max_length=64, verbose_name='toppings name')

    def __str__(self):
        return str(self.name)


class Pizza(models.Model):
    name = models.CharField(max_length=64, verbose_name='pizza name')
    toppings = models.ManyToManyField(Toppings, verbose_name='pizza toppings')
    size = models.IntegerField(
        choices=SIZE_PIZZA, verbose_name='size', null=True, blank=True)
    add_cheese = models.BooleanField(
        null=True, blank=True, choices=((False, 'No'), (True, 'Yes')))
    price = models.DecimalField(
        max_digits=4, decimal_places=2, verbose_name='pizza\'s price', null=True, blank=True)
    is_special = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    @property
    def count_toppings(self):
        pizzatoppings = self.toppings.all()
        quantity_toppings = pizzatoppings.count()
        return quantity_toppings

    @property
    def get_my_price(self):
        pizzatoppings = self.toppings.all()
        quantity_toppings = pizzatoppings.count()
        if self.size == '40':
            if quantity_toppings > 4:
                return 30.00
            return 25.00
        else:
            if quantity_toppings > 4:
                return 40.00
            return 35.00


# class Cart
class Orders(models.Model):
    client = models.ForeignKey(
        CustomClient, on_delete=models.SET_NULL, blank=True, null=True)
    order_time = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(choices=ORDER_STATUS, max_length=24)
    payu_id = models.CharField(max_length=64, null=True)
    payment_status = models.CharField(max_length=162, null = True)


    @property
    def get_cart_total(self):
        orderitems = self.itemorder_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.itemorder_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self): return "Order of {}, #{}, status {}".format(CustomClient,self.id,self.payment_status)

    def request_paymaent(self):
            payuHelper = PayUHelper()
            result = payuHelper.newOrder(self.id, self.client, self.itemorder_set.all(),"Order {}".format(self.id))
            result_json = result.json()
            if result_json['status']['statusCode'] == 'SUCCESS':
                self.payu_id = result_json['orderId']
                self.payment_status = 'WAITING'
                self.save()
                return result_json
            else:
                raise Exception('Nie udało się utworzyć zamównia: {}'.format(result))
   
    def switch_to_success(self):
        self.payment_status = 'SUCCESS'
        self.save()



class ItemOrder(models.Model):
    product = models.ForeignKey(
        Pizza, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Orders, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return (f"{self.product} x  {self.quantity} price: {self.get_total}")

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class DeliveryAdress(models.Model):
    customer = models.ForeignKey(
        CustomClient, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Orders, on_delete=models.SET_NULL, blank=True, null=True)
    adress = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
