# accounts/models.py

from django.db import models
from django.contrib.auth.models import User

class Nomenclature(models.Model):
    abbreviation = models.CharField(max_length=100, verbose_name='Аббревиатура')
    short_name = models.CharField(max_length=100, verbose_name='Наименование краткое')
    full_name = models.CharField(max_length=255, verbose_name='Наименование полное')
    internal_code = models.CharField(max_length=100, verbose_name='Код внутренний')
    cipher = models.CharField(max_length=100, verbose_name='Шифр')
    ekps_code = models.CharField(max_length=100, verbose_name='Код ЕКПС')
    kvt_code = models.CharField(max_length=100, verbose_name='Код КВТ')
    drawing_number = models.CharField(max_length=100, verbose_name='Чертёжный номер')
    nomenclature_type = models.CharField(max_length=100, verbose_name='Вид номенклатуры')

    def __str__(self):
        return self.short_name

class LSI(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True, verbose_name='Биография')

    def __str__(self):
        return self.user.username
