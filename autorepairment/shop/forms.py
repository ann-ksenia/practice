from django import forms
from django.contrib.auth.models import User
from .models import Order, Feedback
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



class ContactForm(forms.Form):
    topic = forms.CharField(label="Тема",
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    content = forms.CharField(label="Содержание",
                               widget=forms.TextInput(attrs={"class": "form-control", "rows": 5, "cols": 10}))


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="ФИО",widget=forms.TextInput(attrs={"class": "form-control", "rows": 5, "cols": 10}))
    password = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={"class": "form-control", "rows": 5, "cols": 10}))

class UserRegisterForm(UserCreationForm):
    last_name = forms.CharField(label='Номер телефона', min_length=11, max_length=12, help_text='Обязательное поле. Только буквы цифры, начиная с 8.',
                             widget = forms.TextInput(attrs={"class": "form-control", "rows": 5, "cols":10}))
    password1 = forms.CharField(label='Пароль', help_text='Пароль не должен быть слишком похож на другую вашу личную информацию.  Ваш пароль должен содержать как минимум 8 символов. Пароль не может состоять только из цифр.',
                                widget = forms.PasswordInput(attrs={"class": "form-control", "rows": 5, "cols":10}))
    password2 = forms.CharField(label='Подтверждение пароля', widget = forms.PasswordInput(attrs={"class": "form-control", "rows": 5, "cols":10}))
    username = forms.CharField(label = "Логин",help_text='Имя пользователя.', widget = forms.TextInput(attrs={"class": "form-control", "rows": 5, "cols":10}))
    first_name = forms.CharField(label = "ФИО",help_text='Введите ФИО полностью.', widget = forms.TextInput(attrs={"class": "form-control", "rows": 5, "cols":10}))

    class Meta:
        model = User
        fields = ('username', 'last_name', 'password1', 'password2', 'first_name')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['problem']
        widgets= {
            'problem': forms.Textarea(attrs={"class": "form-control", "rows": 5, "cols":10})
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['content']
        widgets= {
            'content': forms.Textarea(attrs={"class": "form-control", "rows": 5, "cols":10})
        }