from django.urls import path
from .views import checkout, order_success, cash_payment

urlpatterns = [
    path("checkout/", checkout, name="checkout"),
    path("success/<int:order_id>/", order_success,name="order_success"),
    path("pay/cash/<int:order_id>/", cash_payment, name="cash_payment"),

]