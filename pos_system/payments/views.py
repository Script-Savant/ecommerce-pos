import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from orders.models import Order
from .mpesa import MpesaService

def mpesa_initiate(request, order_id):
    order = Order.objects.get(id=order_id)

    mpesa = MpesaService()
    response = mpesa.initiate_stk_push(
        phone_number=order.mpesa_phone_number,
        amount = order.total_amount,
        order_id=order.id
    )

    order.merchant_request_id = response["MerchantRequestID"]
    order.checkout_request_id = response["CheckoutRequestID"]
    order.save()

    return redirect("mpesa_pending", order_id=order.id)


@csrf_exempt
def mpesa_callback(request):
    try:
        payload = json.loads(request.body)

        stk = payload["Body"]["stkCallback"]
        checkout_request_id = stk["CheckoutRequestID"]
        result_code = stk["ResultCode"]

        order = Order.objects.select_for_update().get(
            checkout_request_id=checkout_request_id
        )

        if result_code == 0 and order.status == Order.STATUS_PENDING:
            with transaction.atomic():
                for item in order.items.select_related("product"):
                    product = item.product
                    product.stock -= item.quantity
                    product.save()

                order.status = Order.STATUS_PAID
                order.is_paid = True
                order.save()

        elif result_code != 0:
            order.status = Order.STATUS_FAILED
            order.save()

    except Exception as e:
        print("M-PESA CALLBACK ERROR:", e)

    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})

def mpesa_pending(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "payments/mpesa_pending.html", {"order": order})

def payment_status(request, order_id):
    order = Order.objects.get(id=order_id)
    # print("ORDER STATUS:", order.status)

    redirect_url = None
    if order.status in [Order.STATUS_PAID, Order.STATUS_CASH]:
        redirect_url = f"/orders/success/{order.id}/"
    elif order.status == Order.STATUS_FAILED:
        redirect_url = f"/orders/failed/{order.id}/"

    return JsonResponse({
        "status": order.status,
        "redirect": redirect_url
    })
