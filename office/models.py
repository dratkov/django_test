from django.db import models
# -*- coding: utf-8 -*-


class User(models.Model):
    name = models.CharField(max_length=50, verbose_name="Имя")
    paycheck = models.IntegerField(verbose_name="Зарплата")
    date_joined = models.DateField(verbose_name="Дата поступления на работу")

    def get_app_label(self):
        return self._meta.app_label

    def get_class_name(self):
        return  self.__class__.__name__

    def get_fields(self):
        # make a list of field/values.
        return [(field, field.value_to_string(self)) for field in User._meta.fields]

    def get_verbose_name_plural(self):
        return self._meta.verbose_name_plural

    class Meta:
            verbose_name = 'Пользователь'
            verbose_name_plural = 'Пользователи'


class Room(models.Model):
    departament = models.CharField(max_length=100, verbose_name="Департамент")
    spots = models.IntegerField(verbose_name="Вместимость")

    def get_app_label(self):
        return self._meta.app_label

    def get_class_name(self):
        return  self.__class__.__name__

    def get_verbose_name_plural(self):
        return self._meta.verbose_name_plural

    class Meta:
            verbose_name = 'Комната'
            verbose_name_plural = 'Комнаты'
# Create your models here.
