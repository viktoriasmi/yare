"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import FeedbackForm, MenuItemForm
from django.contrib.auth.forms import UserCreationForm

from django.db import models
from .models import MenuItem
from .models import Review
from .forms import ReviewForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Наши контакты',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Описание приложения',
            'year':datetime.now().year,
        }
    )

def links (request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Ссылки',
            'message':'Ссылки на сайты',
            'year':datetime.now().year,
        }
    )

def feedback (request):
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': 'Мужчина', '2': 'Женщина'}
    howmuch = {'1': 'Сегодня', '2': 'Вчера', '3': 'На текущей неделе', '4': 'Более недели назад', '5': 'Более месяца назад'}
    rating = {'1': 'Ужасно', '2': 'Плохо', '3': 'Нормально', '4': 'Хорошо', '5': 'Отлично'}

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['gender'] = gender[form.cleaned_data['gender']]
            data['howmuch'] = howmuch[form.cleaned_data['howmuch']]
            data['rating'] = rating[form.cleaned_data['rating']]
            data['email'] = form.cleaned_data['email']
            if (form.cleaned_data['notice'] == True):
                data['notice'] ='Да'
            else:
                data['notice'] ='Нет'
            data['message'] = form.cleaned_data['message']
            form = None
    else:
        form = FeedbackForm()
    return render(
        request,
        'app/feedback.html',
        {
            
            'title':'Отзывы',
            'form':form,
            'data':data
        }
    )

def registration(request):
    """Renders the registration page."""
    
    
    if request.method == "POST": # после отправки формы
        regform = UserCreationForm (request.POST)
        if regform.is_valid(): #валидация полей формы
            reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы
            reg_f.is_staff = False # запрещен вход в административный раздел
            reg_f.is_active = True # активный пользователь
            reg_f.is_superuser = False # не является суперпользователем
            reg_f.date_joined = datetime.now() # дата регистрации
            reg_f.last_login = datetime.now() # дата последней авторизации
            reg_f.save() # сохраняем изменения после добавления данных
            return redirect('home') # переадресация на главную страницу после регистрации
    else:

        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/registration.html',

        {

            'regform': regform, # передача формы в шаблон веб-страницы

            'year':datetime.now().year,

        }

    )
    
def menu(request):
    """Renders the menu page."""
    menuitems = MenuItem.objects.all()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/menu.html',
        {
            'title': 'Меню',
            'menuitems': menuitems,
        }
    )

def menuit(request, parametr):
    """Renders the menuit page."""
    assert isinstance(request, HttpRequest)
    menuit_1 = MenuItem.objects.get(id=parametr)
    reviews = Review.objects.filter(menu_item=parametr)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_f = form.save(commit=False)
            review_f.author = request.user
            review_f.rating = form.cleaned_data['rating']
            review_f.menu_item = menuit_1
            review_f.save()
            
            return redirect('menuit', parametr=menuit_1.id)
    else:
        form = ReviewForm()

    return render(
        request,
        'app/menuit.html',
        {
            'menuit_1': menuit_1,
            
            'reviews': reviews,
            'form': form,
        }
        )
      
def newmenuit(request):
    """Renders the newmenuit page"""
    assert isinstance(request, HttpRequest)
    
    if request.method == "POST":
        menuitemform = MenuItemForm(request.POST, request.FILES)
        if menuitemform.is_valid():
            menuitem_f = menuitemform.save(commit=False)
            menuitem_f.author = request.user
            menuitem_f.save()
            
            return redirect('menu')
    else:
         menuitemform = MenuItemForm()
         
    return render(
        request,
        'app/newmenuit.html',
        {
            'menuitemform': menuitemform,
            'title': 'Добавить новое блюдо в меню',
            
        }
        )

def videopage(request):
    """Renders the video page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopage.html',
        {
            'title':'Страница с видео',
            'message':'Полезные видео',
        }
    )