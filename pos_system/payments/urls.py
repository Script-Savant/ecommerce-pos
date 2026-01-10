from django.urls import path
from .views import mpesa_initiate, mpesa_callback, mpesa_pending, payment_status

urlpatterns = [
    path("mpesa/initiate/<int:order_id>/", mpesa_initiate, name="mpesa_initiate"),
    path("mpesa/pending/<int:order_id>/", mpesa_pending, name="mpesa_pending"),
    path("mpesa/status/<int:order_id>/", payment_status, name="mpesa_status"),
    path("mpesa/callback/", mpesa_callback, name="mpesa_callback"),
]