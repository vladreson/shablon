# create_fixtures.py
import os
import django
import sys

# Добавляем путь к проекту
sys.path.append('C:/Users/VLADRESON/PycharmProjects/myproject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

import json
from django.core import serializers
from catalog.models import Category, Product

# Создаем фикстуры для категорий
categories = Category.objects.all()
category_data = serializers.serialize('json', categories, indent=2)

# Создаем фикстуры для продуктов
products = Product.objects.all()
product_data = serializers.serialize('json', products, indent=2)

# Сохраняем с правильной кодировкой UTF-8
with open('catalog/fixtures/category_data.json', 'w', encoding='utf-8') as f:
    f.write(category_data)

with open('catalog/fixtures/product_data.json', 'w', encoding='utf-8') as f:
    f.write(product_data)

print("Фикстуры успешно созданы!")
