# accounts/forms.py

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Nomenclature, LSI

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, label='Имя пользователя')
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Подтвердите пароль')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Это имя пользователя уже занято.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Этот email уже занят.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают.')
        return cleaned_data

    def save(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')
        user = User.objects.create_user(username=username, email=email, password=password)
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

class NomenclatureForm(forms.ModelForm):
    class Meta:
        model = Nomenclature
        fields = ['abbreviation', 'short_name', 'full_name', 'internal_code', 'cipher', 'ekps_code', 'kvt_code', 'drawing_number', 'nomenclature_type']
        labels = {
            'abbreviation': 'Аббревиатура',
            'short_name': 'Наименование краткое',
            'full_name': 'Наименование полное',
            'internal_code': 'Код внутренний',
            'cipher': 'Шифр',
            'ekps_code': 'Код ЕКПС',
            'kvt_code': 'Код КВТ',
            'drawing_number': 'Чертёжный номер',
            'nomenclature_type': 'Вид номенклатуры',
        }

class LSIForm(forms.ModelForm):
    class Meta:
        model = LSI
        fields = ['name', 'description']
        labels = {
            'name': 'Название',
            'description': 'Описание',
        }
