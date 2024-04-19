from django.db import models
from django.contrib import admin
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User


class MenuItem(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название блюда")
    ingredients = models.TextField(verbose_name="Ингредиенты")
    category = models.CharField(max_length=100, blank=True, null=True, verbose_name="Категория")
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Цена")
    calories = models.IntegerField(verbose_name="Калории")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    image = models.FileField(default = 'temp.jpg', verbose_name="Путь к картинке")

    # Методы класса:
    def get_absolute_url(self): # метод возвращает строку с URL-адресом записи
        return reverse("menuitem", args=[str(self.id)])
    def __str__(self):                      # метод возвращает название, используемое для представления отдельных записей в административном разделе
        return self.name
    
    # Метаданные - вложенный класс, который задает дополнительные параметры модели:
    class Meta:
        db_table = "MenuItems" # имя таблицы для модели
        ordering = ["name"] # порядок сортировки данных в модели
        verbose_name = "Меню доставки" # имя, под которым модель будет отображаться в административном разделе
        verbose_name_plural = "Меню доставки" # тоже для всех пунктов меню доставки

class Review(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name="Автор отзыва")
    menu_item = models.ForeignKey(MenuItem, on_delete = models.CASCADE, verbose_name="Позиция в меню")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.IntegerField(choices=((1, 'Очень плохо'), (2, 'Плохо'), (3, 'Удовлетворительно'), (4, 'Хорошо'), (5, 'Отлично')), default=3)

    class Meta:
        db_table='Review'
        ordering = ['rating']
        verbose_name="Отзыв к блюду"
        verbose_name_plural="Отзывы к блюдам"
        
    def __str__(self):
        return 'Комментарий к %d %s к %s' % (self.id, self.author, self.menu_item)
    

admin.site.register(MenuItem)
admin.site.register(Review)