from django import template
from sportsman.models import *

register = template.Library()   # экземпляр класса Library, через который происходит регистрация собственных шаблонных тегов

@register.simple_tag(name='getcats')      # декоратор связывает функцию с тегом
def get_categories(filter=None):
    '''функция возвращает списки категорий и выполняется при вызове тега из шаблона'''
    if filter is None:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


@register.inclusion_tag('sportsman/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    '''возвращает фрагмент html-страницы'''
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {'cats': cats, 'cat_selected': cat_selected}