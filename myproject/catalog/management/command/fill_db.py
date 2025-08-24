# catalog/management/commands/fill_db.py

from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Fill the database with test data'

    def handle(self, *args, **options):
        # 1. Удаляем все существующие данные
        Product.objects.all().delete()
        Category.objects.all().delete()

        # 2. Вызываем команду для загрузки фикстур
        # Убедитесь, что фикстуры лежат в catalog/fixtures/
        call_command('loaddata', 'category_data.json')
        call_command('loaddata', 'product_data.json')

        # Альтернативный вариант: создание данных кодом прямо здесь
        # cat1 = Category.objects.create(...)
        # Product.objects.create(category=cat1, ...)

        self.stdout.write(self.style.SUCCESS('Database successfully filled!'))