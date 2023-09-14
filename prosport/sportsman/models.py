from django.db import models
from django.db.models import ForeignKey
from django.urls import reverse


class Sportsman(models.Model):
    name = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name=True)
    content = models.TextField(blank=True, verbose_name='Текст статьи')  # поле может быть пустым
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')   # текущее время в момент добавления записи, не изменяется
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')   # меняется каждый раз при изменении записи
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    cat = ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категории')

    def __str__(self):
        return self.name

    # функция reverse строит URL-адрес записи на основе имени маршрута post и словаря параметров kwargs
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    # класс для тонкой накстройки админки
    class Meta:
        verbose_name = 'Спортсмены'             # определяет название модели в админке
        verbose_name_plural = 'Спортсмены'      # определяет название во множ. числе (убирает s)
        ordering = ['-time_create', 'name']     # определяет сортировку записей

class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    # класс для тонкой накстройки админки
    class Meta:
        verbose_name = 'Категории'             # определяет название модели в админке
        verbose_name_plural = 'Категории'      # определяет название во множ. числе (убирает s)
        ordering = ['id']                      # определяет сортировку записей
