from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product

def product_list(request):
    query = request.GET.get("q", "")

    products = Product.objects.filter(is_active=True)

    if query:
        products = products.filter(name__icontains=query)

    paginator = Paginator(products.order_by("-created_at"), 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "query": query,
    }

    return render(request, "products/product_list.html", context)
