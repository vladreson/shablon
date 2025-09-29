from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import Product, Category
from .forms import ProductForm
from .services import get_all_products, get_products_by_category


def home(request):
    # Показываем только опубликованные продукты
    products = Product.objects.filter(publication_status='published')[:5]
    return render(request, 'catalog/home.html', {'products': products})


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    @method_decorator(cache_page(60 * 15))  # Кеширование на 15 минут
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Используем сервисную функцию с низкоуровневым кешированием
        return get_all_products()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все товары'
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все категории'
        return context


class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    fields = ['name', 'slug', 'description']
    template_name = 'catalog/category_form.html'
    success_url = reverse_lazy('catalog:category_list')

    def test_func(self):
        # Разрешаем только модераторам или суперпользователям
        return (self.request.user.has_perm('catalog.can_unpublish_product') or
                self.request.user.is_superuser)

    def form_valid(self, form):
        messages.success(self.request, 'Категория успешно создана!')
        return super().form_valid(form)


class CategoryProductsView(ListView):
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        return get_products_by_category(category_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['category_slug']
        try:
            category = Category.objects.get(slug=category_slug)
            context['title'] = f'Товары категории: {category.name}'
            context['category'] = category
        except Category.DoesNotExist:
            context['title'] = 'Категория не найдена'
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        # Устанавливаем владельца продукта
        form.instance.owner = self.request.user
        messages.success(self.request, 'Товар успешно создан!')
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def test_func(self):
        product = self.get_object()
        # Владелец или модератор может редактировать
        return (product.owner == self.request.user or
                self.request.user.has_perm('catalog.can_unpublish_product'))

    def form_valid(self, form):
        messages.success(self.request, 'Товар успешно обновлен!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        product = self.get_object()
        # Владелец или модератор может удалять
        return (product.owner == self.request.user or
                self.request.user.has_perm('catalog.delete_product'))

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Товар успешно удален!')
        return super().delete(request, *args, **kwargs)