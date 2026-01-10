from django.db import models
from django.conf import settings
from products.models import Product
from decimal import Decimal

User = settings.AUTH_USER_MODEL

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def total(self):
        return sum((item.subtotal() for item in self.items.all()), Decimal("0.00"))

    def __str__(self):
        return f"Cart {self.user}"
   
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def subtotal(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.product} x {self.quantity}"