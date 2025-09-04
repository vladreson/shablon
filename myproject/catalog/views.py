# catalog/views.py
from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})

def home(request):
    products = Product.objects.all()[:5]  # Первые 5 товаров
    return render(request, 'catalog/home.html', {'products': products})