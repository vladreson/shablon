# catalog/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import DeleteView, CreateView, UpdateView

from .models import Product
from django.contrib.auth.mixins import LoginRequiredMixin

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})

def home(request):
    products = Product.objects.all()[:5]  # Первые 5 товаров
    return render(request, 'catalog/home.html', {'products': products})

class ProductCreateView(LoginRequiredMixin, CreateView):
    # ...
    login_url = '/users/login/'

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    # ...
    login_url = '/users/login/'

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    # ...
    login_url = '/users/login/'

# ProductListView и ProductDetailView остаются доступными без авторизации