from django.core.cache import cache
from .models import Product, Category


def get_all_products():
    """
    Сервисная функция для получения всех продуктов с кешированием
    """
    cache_key = 'all_products'
    products = cache.get(cache_key)

    if products is None:
        products = Product.objects.filter(
            publication_status='published'
        ).select_related('category', 'owner')
        cache.set(cache_key, products, 60 * 15)  # Кеш на 15 минут

    return products


def get_products_by_category(category_slug):
    """
    Сервисная функция для получения продуктов по категории
    """
    if hasattr(category_slug, 'slug'):
        category_slug = category_slug.slug

    cache_key = f'products_category_{category_slug}'
    products = cache.get(cache_key)

    if products is None:
        try:
            category = Category.objects.get(slug=category_slug)
            products = Product.objects.filter(
                category=category,
                publication_status='published'
            ).select_related('category', 'owner')
            cache.set(cache_key, products, 60 * 15)
        except Category.DoesNotExist:
            products = Product.objects.none()

    return products