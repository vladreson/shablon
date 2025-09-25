from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Create moderator groups with permissions'

    def handle(self, *args, **options):
        try:
            from catalog.models import Product

            # Создаем группу модераторов
            moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

            if created:
                self.stdout.write('Создана группа "Модератор продуктов"')
            else:
                self.stdout.write('Группа "Модератор продуктов" уже существует')

            # Получаем разрешения для модели Product
            content_type = ContentType.objects.get_for_model(Product)

            # Добавляем необходимые разрешения
            permissions_codenames = [
                'add_product',
                'change_product',
                'delete_product',
                'view_product',
                'can_unpublish_product',
                'can_change_description',
            ]

            added_permissions = 0
            for codename in permissions_codenames:
                try:
                    permission = Permission.objects.get(codename=codename, content_type=content_type)
                    moderator_group.permissions.add(permission)
                    self.stdout.write(f'Добавлено разрешение: {codename}')
                    added_permissions += 1
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Разрешение не найдено: {codename}'))

            self.stdout.write(
                self.style.SUCCESS(
                    f'Группы и разрешения настроены успешно! Добавлено {added_permissions} разрешений.'
                )
            )

        except ImportError as e:
            self.stdout.write(self.style.ERROR(f'Ошибка импорта: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))