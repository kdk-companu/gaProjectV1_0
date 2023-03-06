from django import forms
import datetime

from django.core.exceptions import ValidationError

from projects.models import Organization_Direction, Organization, Type_Document, Project, Organizations_Objects, \
    Development_Task, Position_Object, Сabinet
from workers.models import Subdivision, Department


class Organization_Direction_Control(forms.ModelForm):
    """Направление деятельности организации."""

    class Meta:
        model = Organization_Direction
        fields = ['name', ]

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Направление деятельности организации', 'id': 'name'}),
        }


class Organization_Control(forms.ModelForm):
    """Урпавление."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Organization
        fields = '__all__'


class Type_Document_Control(forms.ModelForm):
    """Разновидность документов."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Type_Document
        fields = '__all__'


class Organizations_Objects_Control(forms.ModelForm):
    """Разновидность документов."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Organizations_Objects
        fields = '__all__'


class Project_Control(forms.ModelForm):
    """Разновидность документов."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Project
        fields = '__all__'


class Development_Task_Control(forms.ModelForm):
    """Задание на разработку"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].empty_label = "Название проекта"
        self.fields['gip'].empty_label = "ГИП"
        self.fields['designer'].empty_label = "Проектировщик"
        self.fields['subdivision'].empty_label = "Управление "
        self.fields['department'].empty_label = "Отдел"

        # self.fields['objects_position'] = forms.ModelChoiceField(queryset=Objects_Position.oobjects.filter(objects_position_pk=2))

        # self.fields['objects_position'] = forms.DateField(
        #     widget=forms.Select(
        #         attrs={'class': 'select2', 'style': 'width: 100%'}
        #     ), label="XERRRRRRRRRRRRRRRRRRRRRRRRRRRRR"
        # )

    class Meta:
        model = Development_Task
        fields = ('project', 'tasks_ppo', 'name', 'gip',
                  'designer', 'part_equipment', 'task', 'documentation_development',
                  'date_documentation_development_planned', 'date_software_development_planned',
                  'date_equipment_assembly_planned', 'date_factory_acceptance_planned',
                  'date_shipment_equipment_planned', 'source_data_folder', 'subdivision', 'department')
        widgets = {
            'project': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'tasks_ppo': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Задания на ППО', 'id': 'tasks_ppo'}),
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Название системы', 'id': 'name'}),
            'gip': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'designer': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'part_equipment': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Состав оборудования', 'id': 'part_equipment'}),
            'task': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Описание задания', 'id': 'task'}),
            'source_data_folder': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Исходные данные', 'id': 'source_data_folder'}),
            'documentation_development': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Описание задания', 'id': 'documentation_development'}),
            'subdivision': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'department': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
        }

    date_documentation_development_planned = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input', 'data-target': '#dateEmployment',
                   'data-inputmask-alias': 'datetime', 'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   }, format='%d.%m.%Y'
        ), label="Разработка документации. Планируемая.",
        input_formats=('%d.%m.%Y',)
    )
    date_software_development_planned = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input', 'data-target': '#dateEmployment',
                   'data-inputmask-alias': 'datetime', 'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   }, format='%d.%m.%Y'
        ), label="Разработка ППО. Планируемая.",
        input_formats=('%d.%m.%Y',)
    )
    date_equipment_assembly_planned = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input', 'data-target': '#dateEmployment',
                   'data-inputmask-alias': 'datetime', 'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   }, format='%d.%m.%Y'
        ), label="Сборка оборудования. Планируемая.",
        input_formats=('%d.%m.%Y',)
    )
    date_factory_acceptance_planned = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input', 'data-target': '#dateEmployment',
                   'data-inputmask-alias': 'datetime', 'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   }, format='%d.%m.%Y'
        ), label="Заводская приемка. Планируемая.",
        input_formats=('%d.%m.%Y',)
    )
    date_shipment_equipment_planned = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input', 'data-target': '#dateEmployment',
                   'data-inputmask-alias': 'datetime', 'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   }, format='%d.%m.%Y'
        ), label="Отгрузка оборудования. Планируемая.",
        input_formats=('%d.%m.%Y',)
    )


class Development_Task_Edit_Date(forms.ModelForm):
    """Задание на разработку"""
    class Meta:
        model = Development_Task
        fields = (
            'date_documentation_development_actual', 'date_software_development_actual',
            'date_equipment_assembly_actual',
            'date_factory_acceptance_actual', 'date_shipment_equipment_actual')

    date_documentation_development_actual = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input', 'data-target': '#dateEmployment',
                   'data-inputmask-alias': 'datetime', 'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   }, format='%d.%m.%Y'
        ), label="Разработка документации. Фактическая.",
        input_formats=('%d.%m.%Y',)
    )
    date_software_development_actual = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input', 'data-target': '#dateEmployment',
                   'data-inputmask-alias': 'datetime', 'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   }, format='%d.%m.%Y'
        ), label="Разработка ППО. Фактическая.",
        input_formats=('%d.%m.%Y',)
    )
    date_equipment_assembly_actual = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input', 'data-target': '#dateEmployment',
                   'data-inputmask-alias': 'datetime', 'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   }, format='%d.%m.%Y'
        ), label="Сборка оборудования. Фактическая.",
        input_formats=('%d.%m.%Y',)
    )
    date_factory_acceptance_actual = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input', 'data-target': '#dateEmployment',
                   'data-inputmask-alias': 'datetime', 'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   }, format='%d.%m.%Y'
        ), label="Заводская приемка. Фактическая.",
        input_formats=('%d.%m.%Y',)
    )
    date_shipment_equipment_actual = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input', 'data-target': '#dateEmployment',
                   'data-inputmask-alias': 'datetime', 'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   }, format='%d.%m.%Y'
        ), label="Отгрузка оборудования. Фактическая.",
        input_formats=('%d.%m.%Y',)
    )


class Development_Task_Edit_Status(forms.ModelForm):
    """Задание на разработку"""

    class Meta:
        model = Development_Task
        fields = ('status', 'current_state')
        widgets = {
            'status': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'current_state': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
        }


class Development_Task_Edit_Develop(forms.ModelForm):
    """Задание на разработку"""

    class Meta:
        model = Development_Task
        fields = ('project_archives_folder',)
        widgets = {
            'project_archives_folder': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Папка с проектом', 'id': 'project_archives_folder'}),

        }


class Development_Task_Filter(forms.Form):
    """Форма для поиска и фильтрации Development_Task_VIEW"""

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('initial')['user']  # Текущий пользователь
        super().__init__(*args, **kwargs)
        '''Сортировка по годам'''
        YEARS_CHOICES = list((str(i), str(i)) for i in range(int(datetime.datetime.now().year), 2019, -1))
        YEARS_CHOICES.insert(0, ('allTime', 'Все года'))
        self.fields['year'] = forms.ChoiceField(label='год', required=False, choices=YEARS_CHOICES,
                                                widget=forms.Select(
                                                    attrs={'class': 'select2', 'style': 'width: 100%'}))
        '''Статус выполенния'''
        STATUS_COMPLETION = (
            ('all', 'Все'),
            ('done', 'Выполнено'),
            ('not_done', 'Не выполнено')
        )
        self.fields['status'] = forms.ChoiceField(label='Отметка',
                                                  required=False,
                                                  choices=STATUS_COMPLETION,
                                                  widget=forms.Select(
                                                      attrs={'class': 'select2', 'style': 'width: 100%'}))
        '''Сортировка по управлению'''
        QUERY_SUBDIVISION = list(Subdivision.objects.values_list('slug', 'name'))
        QUERY_SUBDIVISION.insert(0, ('own', 'Свое управление'))
        self.fields['subdivision'] = forms.ChoiceField(label='Управление',
                                                       required=False,
                                                       choices=QUERY_SUBDIVISION,
                                                       widget=forms.Select(
                                                           attrs={'class': 'select2', 'style': 'width: 100%'}))
        '''Сортировка по отделу'''
        QUERY_DEPARTMENT = list(Department.objects.values_list('slug', 'name'))
        QUERY_DEPARTMENT.insert(0, ('own', 'Свой отдел'))
        self.fields['department'] = forms.ChoiceField(label='Отдел', required=False, choices=QUERY_DEPARTMENT,
                                                      widget=forms.Select(
                                                          attrs={'class': 'select2', 'style': 'width: 100%'}))


class Position_Objects_Control(forms.ModelForm):
    """Задание на разработку"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['development_task'].empty_label = "Задания на ППО"

    class Meta:
        model = Position_Object
        fields = ['development_task', 'name', 'short_names', 'description']
        widgets = {
            'development_task': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Название позиции', 'id': 'name'}),
            'short_names': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Обиходные название', 'id': 'short_names'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Описание позиции', 'id': 'description'}),
        }


class Position_Objects_Filter(forms.Form):
    """Форма для поиска и фильтрации Development_Task_VIEW"""

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('initial')['user']  # Текущий пользователь
        super().__init__(*args, **kwargs)
        '''Статус выполенния'''
        STATUS_COMPLETION = (
            ('all', 'Все'),
            ('done', 'Выполнено'),
            ('not_done', 'Не выполнено')
        )
        self.fields['status'] = forms.ChoiceField(label='Отметка',
                                                  required=False,
                                                  choices=STATUS_COMPLETION,
                                                  widget=forms.Select(
                                                      attrs={'class': 'select2', 'style': 'width: 100%'}))
        '''Сортировка по управлению'''
        QUERY_SUBDIVISION = list(Subdivision.objects.values_list('slug', 'name'))
        QUERY_SUBDIVISION.insert(0, ('own', 'Свое управление'))
        self.fields['subdivision'] = forms.ChoiceField(label='Управление',
                                                       required=False,
                                                       choices=QUERY_SUBDIVISION,
                                                       widget=forms.Select(
                                                           attrs={'class': 'select2', 'style': 'width: 100%'}))
        '''Сортировка по отделу'''
        QUERY_DEPARTMENT = list(Department.objects.values_list('slug', 'name'))
        QUERY_DEPARTMENT.insert(0, ('own', 'Свой отдел'))
        self.fields['department'] = forms.ChoiceField(label='Отдел', required=False, choices=QUERY_DEPARTMENT,
                                                      widget=forms.Select(
                                                          attrs={'class': 'select2', 'style': 'width: 100%'}))


class Position_Objects_Edit_Checker(forms.ModelForm):
    """ lll"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Position_Object
        fields = ['checker', ]
        widgets = {
            'checker': forms.SelectMultiple(
                attrs={'name': 'checker', 'id': 'checker', 'class': 'duallistbox', 'multiple': 'multiple'}),
        }


class Position_Objects_Upload_Protocol(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reviewer_protocol'].empty_label = ""

    def clean_reviewer_protocol_scan(self):
        file = self.cleaned_data.get('reviewer_protocol', False)
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
        model = Position_Object
        fields = ('reviewer_protocol',)
        widgets = {
            'reviewer_protocol': forms.FileInput(
                attrs={'class': 'custom-file-input', 'id': 'customFile', 'accept': ".pdf"}
            ),
        }


class Cabinet_Control(forms.ModelForm):
    """Задание на разработку"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position_objects'].empty_label = "Позиция на объекте"

    class Meta:
        model = Сabinet
        fields = ['position_objects','name','factory_number','description','comments' ]
        widgets = {
            'position_objects': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Название шкафа', 'id': 'name'}),
            'factory_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Заводской номер', 'id': 'factory_number'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Описание', 'id': 'description'}),
            'comments': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Замечание по шкафу', 'id': 'description'})
        }
