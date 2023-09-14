from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

from .forms import *
from .models import *
from .utils import *

# request - ссылка на спецкласс HttpRequest, содержит всю инфу о запросе
# def index(request):
#     posts = Sportsman.objects.all()
#     # cats = Category.objects.all()
#     data = {
#         'title': 'Главная страница',
#         'cat_selected': 0,
#         'menu': menu,
#         'posts': posts,
#         #'cats': cats,
#     }
#     # t = render_to_string('sportsman/index.html')
#     # return HttpResponse(t)
#     # функция render делает то же самое, что и предыдущие строчки
#     return render(request, 'sportsman/index.html', context=data)



class SportsmanHome(DataMixin, ListView):
    model = Sportsman                           # атрибут ссылается на модель данных (форм-ся object_list со всеми данными из БД)
    template_name = 'sportsman/index.html'      # явное указание на нужный шаблон
    context_object_name = 'posts'               # имя переменной в шаблоне, которой передаем все записи из БД (хотя в шаблоне можно юзать object_list)

    def get_context_data(self, *, object_list=None, **kwargs):
        '''метод для передачи динамических и статических данных'''
        context = super().get_context_data(**kwargs)    # обращение к базовому классу с вызовом этого же метода с передачей возможных именованных параметров из словаря kwargs
        # context['title'] = 'Главная страница'   # передача статических данных
        # context['cat_selected'] = 0             # передача статических данных
        # context['menu'] = menu
        c_def = self.get_user_context(title='Главная страница')
        return {**context, **c_def}

    def get_queryset(self):
        '''метод позволяет фильтровать записи по флагу (здесь – опубликованные статьи)'''
        return Sportsman.objects.filter(is_published=True).select_related('cat')

# def show_category(request, cat_slug):
#     posts = Sportsman.objects.filter(cat__slug=cat_slug)
#     if len(posts) == 0:
#         raise Http404()
#     # cats = Category.objects.all()
#
#     data = {
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_slug,
#         'menu': menu,
#         'posts': posts,
#         #'cats': cats,
#     }
#     return render(request, 'sportsman/index.html', context=data)

class SportsmanCategory(DataMixin, ListView):
    model = Sportsman
    template_name = 'sportsman/index.html'
    context_object_name = 'posts'
    allow_empty = False     # генерация исключения 404, если указан несуществующий слаг, иначе - пустая страница

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)    # формирование базовых ключей
        # context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        # context['cat_selected'] = context['posts'][0].cat_id
        # context['menu'] = menu
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.title),
                                      cat_selected=c.pk)
        return {**context, **c_def}

    def get_queryset(self):
        return Sportsman.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

def about(request):
    data = {
        'title': 'О сайте',
        'menu': menu,
    }
    return render(request, 'sportsman/about.html', context=data)

# def addpage(request):
#     if request.method == 'POST':
#         print(dir(request))
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():     # проверка на корректность заполнения полей
#             # print(form.cleaned_data)
#             # try:
#             #     # Sportsman.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, 'Ошибка добавления поста')
#             form.save()     #берет на себя проверку корректности записи данных, блок try except не нужен
#             return redirect('home')
#     else:                       # ветка else: форма показывается первый раз, поля пустые
#         form = AddPostForm()
#
#     data = {
#         'title': 'Добавление статьи',
#         'menu': menu,
#         'form': form,
#     }
#
#     return render(request, 'sportsman/add_page.html', context = data)

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'sportsman/add_page.html'
    success_url = reverse_lazy('home')
    # login_url = reverse_lazy('home')    # перенаправления для незарегистрированного пользователя при использовании LoginRequiredMixin

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Добавление статьи'
        # context['menu'] = menu
        c_def = self.get_user_context(title='Добавление статьи')
        return {**context, **c_def}

# def contact(request):
#     data = {
#         'title': 'Обратная связь',
#         'menu': menu
#     }
#     return render(request, 'sportsman/contact.html', context=data)


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'sportsman/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return {**context, **c_def}

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


# def login(request):
#     data = {
#         'title': 'Войти',
#         'menu': menu
#     }
#     return render(request, 'sportsman/login.html', context=data)

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'sportsman/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return {**context, **c_def}

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)         # стандартная функция logout() фреймворка для выхода пользователя
    return redirect('home')

# def show_post(request, post_slug):
#     # post = Sportsman.objects.get(slug=post_id)
#     post = get_object_or_404(Sportsman, slug=post_slug)
#     data = {
#         'menu': menu,
#         'post': post,
#         'name': post.name,
#         'cat_selected': 1,
#     }
#     return render(request, 'sportsman/post.html', context=data)

class ShowPost(DataMixin, DetailView):
    model = Sportsman
    template_name = 'sportsman/post.html'
    slug_url_kwarg = 'post_slug'    # прописывается из-за того, что url поста post/<post_slug>, а не просто <post_slug>
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = context['post']
        # context['menu'] = menu
        c_def = self.get_user_context(title=context['post'])
        return {**context, **c_def}


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'sportsman/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return {**context, **c_def}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')