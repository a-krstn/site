from django.contrib import admin
from .models import *

class SportsmanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'time_create', 'photo', 'is_published', 'slug')   # список отображаемых полей в админке
    list_display_links = ('id', 'name')     # список полей в виде ссылки для перехода к конкретной записи
    search_fields = ('name', 'content')     # поля, по которым можно будет производить поиск записей
    list_editable = ('is_published',)       # атрибут, в котором поля можно редактировать прямо в списке статей
    list_filter = ('is_published', 'time_create')   # поля, по которым можно фильтровать список статей
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Sportsman, SportsmanAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')  # список отображаемых полей в админке
    list_display_links = ('id', 'title')  # список полей в виде ссылки для перехода к конкретной записи
    search_fields = ('name',)   # поля, по которым можно будет производить поиск записей
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Category, CategoryAdmin)