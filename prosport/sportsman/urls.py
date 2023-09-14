from django.urls import path
from . import views

urlpatterns = [
    path('', views.SportsmanHome.as_view(), name='home'),   # as_view() служит для привязки класса представления к маршруту
    path('about/', views.about, name='about'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.SportsmanCategory.as_view(), name='category'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('logout/', views.logout_user, name='logout'),
]