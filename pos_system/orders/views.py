from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.contrib import messages
from .models import Order, OrderItem

@login_required
def checkout(request):
    cart = request.user.cart
    cart_items = cart.items.select_related("product")

    if not cart_items.exists():
        return redirect("cart_detail")
    
    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        phone_number = request.POST.get("phone_number")

        with transaction.atomic():
            order = Order.objects.create(
                user = request.user,
                total_amount = cart.total(),
                payment_method = payment_method,
                mpesa_phone_number = phone_number if payment_method == "mpesa" else None,
                status = Order.STATUS_PENDING
            )

            for item in cart_items:
                product = item.product

                # stock check
                if product.stock < item.quantity:
                    messages.warning(request, f"Not enough stock for {product.name}")
                    return redirect("cart")
                
                # create order item
                OrderItem.objects.create(
                    order = order,
                    product = product,
                    quantity = item.quantity,
                    price = product.price
                )

                # # Reduce stock
                # product.stock -= item.quantity
                # product.save()

            cart_items.delete()

        if  payment_method == "cash":
            return redirect("cash_payment", order_id=order.id)
        
        return redirect("mpesa_initiate", order_id=order.id)
    
    return render(request, "orders/checkout.html", {"cart": cart})

@login_required
def cash_payment(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    if order.status != Order.STATUS_PENDING:
        return redirect("order_success", order_id=order.id)
    
    with transaction.atomic():
        for item in order.items.select_related("product"):
            product = item.product
            product.stock -= item.quantity
            product.save()

        order.status = Order.STATUS_CASH
        order.is_paid = True
        order.save()

    return redirect("order_success", order_id=order.id)

@login_required
def order_success(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, "orders/order_success.html", {"order": order})

