"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from.models import Review
from .models import MenuItem

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))

class FeedbackForm(forms.Form):
    name = forms.CharField(label='Ваше имя', min_length=2, max_length=255)
    gender = forms.ChoiceField(label='Ваш пол',
                                   choices=[('1','Мужской'), ('2', 'Женский')],
                                   widget=forms.RadioSelect, initial=1)
    howmuch = forms.ChoiceField(label='Вы были у нас',
                                    choices=[('1', 'Сегодня'), ('2', 'Вчера'), ('3', 'На текущей неделе'), ('4', 'Более недели назад'), ('5', 'Более месяца назад')],
                                    initial=1)
    rating = forms.ChoiceField(label='Как бы вы оценили нашу доставку',
                               choices=[('1', 'Ужасно'), ('2', 'Плохо'), ('3', 'Нормально'), ('4', 'Хорошо'), ('5', 'Отлично')],
                                    initial=1)
    email = forms.EmailField(label='Ваш e-mail', min_length=7)
    notice = forms.BooleanField(label='Хотите получать новости от нашего сайта?', required=False)
    message = forms.CharField(label='Ваш отзыв', widget=forms.Textarea(attrs={'rows': 10, 'cols': 100, 'maxlength': 255}))
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text', 'rating')
        labels = {'text': "Отзыв"}
        
class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = {'name', 'ingredients', 'category', 'price', 'calories', 'image'}
        labels = {'name': "Название", 'ingredients': "Ингредиенты", 'category': "Категория", 'price': "Цена", 'calories': "Калории", 'image': "Изображение"}
       