from django import forms
from django.core.exceptions import ValidationError

from workers.models import Subdivision, Department, Chief


class Subdivision_Form_Control(forms.ModelForm):
    ''' Урпавление.'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Subdivision
        # fields = '__all__'
        fields = ['name', 'abbreviation', 'description']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Управления/Подразделения', 'id': 'name'}),
            'abbreviation': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Сокращенное название', 'id': 'abbreviation'}),
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Описание', 'id': 'description'})
        }

    # Пользовательский валидатор на subdivision. Доп проверка.
    def clean_subdivision(self):
        subdivision = self.cleaned_data['name']
        if len(subdivision) > 255:
            raise ValidationError('Длина превышает 255 символов')
        return subdivision


class Department_Form_Control(forms.ModelForm):
    '''Урпавление.'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Department
        # fields = '__all__'
        fields = ['name', 'abbreviation', 'description']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Отдел', 'id': 'name'}),
            'abbreviation': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Сокращенное название', 'id': 'abbreviation'}),
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Описание', 'id': 'description'})
        }

    def clean_subdivision(self):
        subdivision = self.cleaned_data['department']
        if len(subdivision) > 255:
            raise ValidationError('Длина превышает 255 символов')
        return subdivision


class Chief_Form_Control(forms.ModelForm):
    '''Отдел.'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Chief
        fields = ['name', 'abbreviation', 'rights']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Должность', 'id': 'name'}),
            'abbreviation': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Сокращенное название', 'id': 'abbreviation'}),
            'rights': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'По старшенству', 'id': 'rights'})
        }

    # Пользовательский валидатор на subdivision. Доп проверка.
    def clean_subdivision(self):
        subdivision = self.cleaned_data['name']
        if len(subdivision) > 255:
            raise ValidationError('Длина превышает 255 символов')
        return subdivision
