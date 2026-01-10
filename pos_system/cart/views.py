from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import CartItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.user.cart

    cart_item, created = CartItem.objects.get_or_create(
        cart = cart,
        product = product
    )

    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()

    return redirect("product_list")


@login_required
def cart_detail(request):
    cart = request.user.cart
    return render(request, "cart/cart_detail.html", {"cart": cart})

@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart=request.user.cart)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()

    return redirect("cart_detail")

@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart=request.user.cart)
    item.delete()
    return redirect("cart_detail")
