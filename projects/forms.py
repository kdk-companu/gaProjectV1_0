from django import forms
from django.core.exceptions import ValidationError

from projects.models import Development_Task, Objects_Position, Organization


class Development_Task_Control(forms.ModelForm):
    '''Урпавление.'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status_systems'].empty_label = "Новый объект"
        self.fields['customer'].empty_label = "Выберите заказчика"
        self.fields['exploitation'].empty_label = "Выберите эксплуатацию"
        self.fields['designer'].empty_label = "Выберите проектировщика"
        self.fields['organizations_objects'].empty_label = "Выберите объект"
        self.fields['objects_position'].empty_label = "Выберите позицию"
        self.fields['gip'].empty_label = "Выберите ГИПа"
        # authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all())
        # self.fields['objects_position'] = forms.ModelChoiceField(queryset=Development_Task.objects.all())
        # self.fields['objects_position'] = forms.ModelChoiceField(queryset=Objects_Position.objects.filter(pk=1))
        # self.fields['objects_position'] = forms.ModelChoiceField(queryset=Objects_Position.oobjects.filter(objects_position_pk=2))

        # self.fields['objects_position'] = forms.DateField(
        #     widget=forms.Select(
        #         attrs={'class': 'select2', 'style': 'width: 100%'}
        #     ), label="XERRRRRRRRRRRRRRRRRRRRRRRRRRRRR"
        # )

    class Meta:
        model = Development_Task
        # fields = '__all__'
        fields = ['tasks_ppo', 'name_systems', 'status_systems', 'customer', 'exploitation', 'designer',
                  'organizations_objects', 'objects_position', 'gip', 'task', 'part_equipment',
                  'date_software_development_planned', 'date_documentation_development_planned',
                  'date_factory_acceptance_planned', 'date_shipment_equipment_planned', 'source_data_folder'
                  ]

        widgets = {
            'tasks_ppo': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Задания на ППО', 'id': 'tasks_ppo'}),
            'name_systems': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Название системы', 'id': 'name_systems'}),
            'status_systems': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'customer': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'exploitation': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'designer': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'organizations_objects': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'objects_position': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'gip': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'task': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Описание задания', 'id': 'task'}),
            'part_equipment': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Состав оборудования', 'id': 'part_equipment'}),
            'source_data_folder': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Папка с исходными данными',
                       'id': 'source_data_folder'}),
        }

    date_software_development_planned = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input', 'data-target': '#dateEmployment',
                   'data-inputmask-alias': 'datetime', 'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   }, format='%d.%m.%Y'
        ), label="Срок разработки ППО",
        input_formats=('%d.%m.%Y',)
    )
    date_documentation_development_planned = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input', 'data-target': '#dateEmployment',
                   'data-inputmask-alias': 'datetime', 'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   }, format='%d.%m.%Y'
        ), label="Срок разработки документации",
        input_formats=('%d.%m.%Y',)
    )
    date_factory_acceptance_planned = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input', 'data-target': '#dateEmployment',
                   'data-inputmask-alias': 'datetime', 'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   }, format='%d.%m.%Y'
        ), label="Заводская приемка",
        input_formats=('%d.%m.%Y',)
    )
    date_shipment_equipment_planned = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input', 'data-target': '#dateEmployment',
                   'data-inputmask-alias': 'datetime', 'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   }, format='%d.%m.%Y'
        ), label="Отгрузка оборудования",
        input_formats=('%d.%m.%Y',)
    )


class Organization_Control(forms.ModelForm):
    '''Урпавление.'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Organization
        fields = ['name', 'status', 'site', 'description']

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Фирма', 'id': 'tasks_ppo'}),
            'status': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Описание фирмы', 'id': 'task'}),
            'site': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Сайт', 'id': 'name_systems'}),
        }