from django.urls import path, include
from .views import *

urlpatterns = [

    path('chceckout-confirm', chceckoutConfirm, name="chceckout-confirm"),
    path('order/<order_id>', orderStatus),
    path('order-status/<order_id>', orderStatusData),
    path('payu-notification', payuNotification, name="payuNotification"),

]
