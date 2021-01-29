from .helpers import PayUHelper
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json
from django.contrib.auth.decorators import login_required


@login_required
def chceckoutConfirm(request):
    user = request.user
    if not(user):
        messages.info(request, "Login firstly :)")
        return redirect("/login/")
    try:
        order = Orders.objects.get(
            client=user, order_status='IN CART')
    except Exception as e:
        messages.error(
            request, "Sorry! Can not see items in cart! Try again :)")
        return redirect('dashboard/menu')

    try:
        payment_request = order.request_paymaent()
    except Exception as e:
        messages.error(request, "Sorry! Cart is empty!")
        return redirect('dashboard/menu')

    return redirect(payment_request['redirectUri'])


@login_required
def orderStatus(request, order_id):
    order = Orders.objects.get(pk=order_id)
    return render(request, 'PayU/order_view.html', {'order': order})


@login_required
def orderStatusData(request, order_id):
    order = Orders.objects.get(pk=order_id)
    if order.payment_status != 'SUCCESS' and order.payment_status != 'ERR':
        try:
            payUHelper = PayUHelper()
            details = payUHelper.orderData(order.payu_id).json()
            if details['orders'][0]['status'] == 'COMPLETED':
                order.switch_to_success()
                order.order_status = "CONFIRMED"
                order.save()
        except Exception as e:
            pass

    return JsonResponse({
        'id': order.id,
        'payment_status': order.payment_status,
    })


@login_required
@csrf_exempt
def payuNotification(request):
    try:
        data = json.loads(request.body)
        if data['order']['status'] == 'COMPLETED':
            # TODO: dodać weryfikację płatności !!!
            order = Orders.objects.get(id=data['order']['extOrderId'])
            order.switch_to_success()
        return HttpResponse('Success!')
    except Exception as e:
        resp = HttpResponse('Error: {}'.format(e))
        resp.status_code = 500
        return resp
