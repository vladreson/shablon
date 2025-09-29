from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    PUBLISH_STATUS = [
        ('published', 'Опубликовано'),
        ('moderation', 'На модерации'),
        ('rejected', 'Отклонено'),
    ]

    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    # Новые поля
    publication_status = models.CharField(
        max_length=20,
        choices=PUBLISH_STATUS,
        default='moderation',
        verbose_name='Статус публикации'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Владелец'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
            ("can_change_description", "Может изменять описание продукта"),
        ]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name