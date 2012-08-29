# -*- coding: utf-8 -*-
from django import forms
from datetime import date


class GeneralForm(forms.Form):
        char_field = forms.CharField(error_messages={'required': u"Необходимый параметр!", 'max_length': u"Длинна поля не должна превышать 100 символов!"}, max_length=100)
        integer_field = forms.IntegerField(error_messages={'required': u"Необходимый параметр!"})
        date_field = forms.DateField(error_messages={"invalid": u"Дата невалидна!", "required": u"Необходимый параметр!"})

        def clean_date_field(self):
            date_value = self.cleaned_data['date_field']
            date_arr = str(date_value).split('-')
            if date(int(date_arr[0]), int(date_arr[1]), int(date_arr[2])) > date.today():
                raise forms.ValidationError("Дата не должна быть больше текущей!")
            return date_value
