from django import forms
from django.core.exceptions import ValidationError

from workers.models import Сertificate_Users, Сertificates, Сertificate_Parts, User


class Certificates_Workers_Form_Control(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user_add = kwargs.pop('user_add', None)
        print(self.user_add)
        super(Certificates_Workers_Form_Control, self).__init__(*args, **kwargs)

    def clean_passport_file(self):
        file = self.cleaned_data.get('file1', False)
        # Проверка на повторное нажатие
        if '/' in str(file):
            raise ValidationError("Вы не выбрали файл.")
        try:
            file.size
        except:
            raise ValidationError("Пустой файл.")

        if file:
            if file.size > 5 * 1024 * 1024:
                raise ValidationError("Максимальный размер файла 5мб")
            return file
        else:
            raise ValidationError("Не удалось прочитать загруженный файл")

    class Meta:
        model = Сertificate_Users
        fields = ['certificate', 'date_delivery','file1', 'file2', 'file3']
        widgets = {
            'certificate': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'file1': forms.FileInput(
                attrs={'class': 'custom-file-input', 'id': 'customFile', 'accept': ".pdf"}
            ),
        }

    date_delivery = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input', 'data-target': '#dateEmployment',
                   'data-inputmask-alias': 'datetime', 'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   }, format='%d.%m.%Y'
        ), label="Дата получение сертификата",
        input_formats=('%d.%m.%Y',)
    )


class Certificates_Workers_All_Form_Control(forms.ModelForm):
    '''Добавить сертификаты для всех пользователей'''
    user_current = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].empty_label = "Укажите сотрудника"
        self.fields['chief'].empty_label = "Должность получения сертификата"
        self.fields['certificate'].empty_label = "Тип сертификата"
        self.user_current = kwargs['initial']['user_current']
        self.fields['user'].queryset = User.objects.filter(subdivision=self.user_current.subdivision,
                                                           department=self.user_current.department,
                                                           employee='employee').order_by('surname')

    def clean_user(self):
        user = self.cleaned_data['user']
        if self.user_current.subdivision != user.subdivision or self.user_current.department != user.department:
            raise ValidationError("У вас нет прав добавлять сертификат данному сотруднику")
        return user

    def clean_chief(self):
        chief = self.cleaned_data['chief']
        if not chief:
            raise ValidationError("Не указана должность")
        return chief

    def clean_file1(self):
        file = self.cleaned_data.get('file1', False)
        # Проверка на повторное нажатие
        if '/' in str(file):
            raise ValidationError("Вы не выбрали файл.")
        try:
            file.size
        except:
            raise ValidationError("Пустой файл.")

        if file:
            if file.size > 5 * 1024 * 1024:
                raise ValidationError("Максимальный размер файла 5мб")
            return file
        else:
            raise ValidationError("Не удалось прочитать загруженный файл")

    class Meta:
        model = Сertificate_Users
        fields = ['user', 'certificate', 'date_delivery', 'chief', 'file1', 'file2', 'file3']
        widgets = {
            'user': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'certificate': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'chief': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'file1': forms.FileInput(
                attrs={'class': 'custom-file-input', 'id': 'customFile1', 'accept': ".pdf"}
            ),
            'file2': forms.FileInput(
                attrs={'class': 'custom-file-input', 'id': 'customFile2', 'accept': ".pdf"}
            ),
            'file3': forms.FileInput(
                attrs={'class': 'custom-file-input', 'id': 'customFile3', 'accept': ".pdf"}
            ),
        }

    date_delivery = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input', 'data-target': '#dateEmployment',
                   'data-inputmask-alias': 'datetime', 'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   }, format='%d.%m.%Y'
        ), label="Дата получение сертификата",
        input_formats=('%d.%m.%Y',)
    )


class Certificates_Form_Control(forms.ModelForm):
    '''Сертификаты.'''

    class Meta:
        model = Сertificates
        # fields = '__all__'
        fields = ['name', 'abbreviation', 'how_to_take', 'answers', 'state']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Название сертификата', 'id': 'name'}),
            'abbreviation': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Сокращенное название', 'id': 'abbreviation'}),
            'how_to_take': forms.Textarea(
                attrs={'class': 'summernote', 'placeholder': 'Описание задания', 'id': 'how_to_take'}),
            'answers': forms.Textarea(
                attrs={'class': 'summernote', 'placeholder': 'Описание задания', 'id': 'answers'}),
            'state': forms.CheckboxInput(
                attrs={'id': 'state',}),

        }


class Certificates_Parts_Form_Control(forms.ModelForm):
    '''Сертификаты.'''

    class Meta:
        model = Сertificate_Parts
        fields = ['certificates', 'name', 'validity', 'change_chief', 'state']
        # widgets = {
        #     'name': forms.TextInput(
        #         attrs={'class': 'form-control', 'placeholder': 'Название сертификата', 'id': 'name'}),
        #     'abbreviation': forms.TextInput(
        #         attrs={'class': 'form-control', 'placeholder': 'Сокращенное название', 'id': 'abbreviation'}),
        #     'how_to_take': forms.TextInput(
        #         attrs={'class': 'form-control', 'placeholder': 'Как сдавать', 'id': 'how_to_take'}),
        #     'answers': forms.TextInput(
        #         attrs={'class': 'form-control', 'placeholder': 'Ответы', 'id': 'answers'}),
        #     'state': forms.TextInput(
        #         attrs={'class': 'form-control', 'placeholder': 'Актуальность', 'id': 'state'})
        # }
