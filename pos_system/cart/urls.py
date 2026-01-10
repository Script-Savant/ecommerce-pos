from django.urls import path
from .views import add_to_cart, cart_detail, update_cart_item, remove_cart_item

urlpatterns = [
    path("", cart_detail, name="cart_detail"),
    path("add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("update/<int:item_id>/", update_cart_item, name="update_cart_item"),
    path("remove/<int:item_id>/", remove_cart_item, name="remove_cart_item"),
]