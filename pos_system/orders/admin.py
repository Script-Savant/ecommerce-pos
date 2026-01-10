from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_amount", "payment_method", "is_paid", "created_at")
    list_filter = ["created_at", "is_paid", "payment_method"]
    inlines = [OrderItemInline]