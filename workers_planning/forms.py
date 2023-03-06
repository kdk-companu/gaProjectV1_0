from dateutil.relativedelta import relativedelta
from django import forms
from django.core.exceptions import ValidationError

from projects.models import Organizations_Objects
from workers.models import User
from workers_planning.models import Information_Schedule, Information_Missing, Workers_Missing, Workers_Mission, \
    Workers_Weekend_Work


class Information_Schedule_Filter(forms.Form):
    """Форма для поиска и фильтрации Информация о выходных днях и празднках"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['year'] = forms.IntegerField(label='Год', required=False, widget=forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'Год', 'id': 'year'}))

    def clean(self):
        try:
            if self.cleaned_data['year']:
                year = int(self.cleaned_data['year'])
                if year > 2030:
                    raise ValidationError('Уменьшите год.')
                if year < 2000:
                    raise ValidationError('Увеличьте год.')
        except Exception as e:
            raise ValidationError('Неправильный формат года.')


class Information_Schedule_Control(forms.ModelForm):
    class Meta:
        model = Information_Schedule
        fields = ['date', 'description', 'work', 'work_time']
        widgets = {
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Описание', 'id': 'description'}),
            'work': forms.CheckboxInput(
                attrs={'id': 'work', 'class': 'custom-control-input'}),
            'work_time': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Время работы', 'id': 'work_time'}),
        }

    date = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input', 'data-target': '#dateEmployment',
                   'data-inputmask-alias': 'datetime', 'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   }, format='%d.%m.%Y'
        ), label="Дата",
        input_formats=('%d.%m.%Y',)
    )


class Information_Missing_Control(forms.ModelForm):
    class Meta:
        model = Information_Missing
        fields = ['name', 'color']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control'}),
        }


class Workers_Missing_Control(forms.ModelForm):
    user_current = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].empty_label = "Сотрудник"
        self.fields['information_missing'].empty_label = "Причина отсутствия"
        self.user_current = kwargs['initial']['user_current']
        self.fields['user'].queryset = User.objects.filter(subdivision=self.user_current.subdivision,
                                                           department=self.user_current.department,
                                                           employee='employee').order_by('surname')

    class Meta:
        model = Workers_Missing
        fields = ['user', 'information_missing', 'date_start', 'date_end', 'comments']
        widgets = {
            'user': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'information_missing': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'comments': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Коментарии', 'id': 'comments'}),
        }

    date_start = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input',
                   'data-target': '#date_in_form',
                   'data-inputmask-alias': 'datetime',
                   'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   'inputmode': "numeric"
                   }, format='%d.%m.%Y'
        ), label="Дата от",
        input_formats=('%d.%m.%Y',)
    )
    date_end = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input',
                   'data-target': '#date_out_form',
                   'data-inputmask-alias': 'datetime',
                   'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   'inputmode': "numeric"
                   }, format='%d.%m.%Y'
        ), label="Дата до",
        input_formats=('%d.%m.%Y',)
    )
    def clean(self):

        date_start = self.cleaned_data['date_start']
        date_end = self.cleaned_data['date_end']
        workers = self.cleaned_data['user']
        if date_start > date_end:
            raise ValidationError('Дата начала отсутствия не может быть больше даты окончания отсутствия.')
        """Проверки на заполенение базы данных по Workers_Missing,Workers_Weekend_Work"""

        """ Проверка на Отсутсвие"""
        missings = Workers_Missing.objects.filter(date_start__gte=date_start - relativedelta(months=6),
                                                  date_end__lte=date_end + relativedelta(months=6), user=workers)
        for missing in missings:
            """Если даты попадают в диапазон"""
            if date_start >= missing.date_start and date_start <= missing.date_end or date_end >= missing.date_start and date_end <= missing.date_end:
                raise ValidationError(
                    '{0} уже отсутсвует с {1} по {2} по причине {3}'.format(workers, missing.date_start,
                                                                            missing.date_end,
                                                                            missing.information_missing))
            if date_start < missing.date_start and date_end > missing.date_end:
                raise ValidationError(
                    '{0} уже отсутсвует с {1} по {2} по причине {3}'.format(workers, missing.date_start,
                                                                            missing.date_end,
                                                                            missing.information_missing))
        """ Проверка на командировки"""
        missions = Workers_Mission.objects.filter(date_start__gte=date_start - relativedelta(months=6),
                                                  date_end__lte=date_end + relativedelta(months=6), user=workers)
        for mission in missions:
            """Если даты попадают в диапазон"""
            if date_start >= mission.date_departure and date_start <= mission.date_arrival or date_end >= mission.date_departure and date_start <= mission.date_arrival:
                raise ValidationError(
                    '{0} уже в командировке с {1} по {2} на объекте {3}'.format(workers, mission.date_departure,
                                                                            mission.date_arrival,
                                                                            mission.organizations_objects))
            if date_start < mission.date_departure and date_end > mission.date_arrival:
                raise ValidationError(
                    '{0} уже в командировке с {1} по {2} на объекте {3}'.format(workers, mission.date_departure,
                                                                            mission.date_arrival,
                                                                            mission.organizations_objects))
        """Максимальный срок отсутствия"""
        if (date_end - date_start).days > 120:
            raise ValidationError('Максимальный срок отсутствия 120 дней.')




class Workers_Missing_Filter(forms.Form):
    date_in = forms.DateField(required=False,
                              widget=forms.DateInput(
                                  attrs={'class': 'form-control datepicker-input',
                                         'data-target': '#date_in_form',
                                         'data-inputmask-alias': 'datetime',
                                         'data-inputmask-inputformat': 'dd.mm.yyyy',
                                         'data-mask': "00.00.0000",
                                         'inputmode': "numeric"
                                         }, format='%d.%m.%Y'
                              ), label="Дата от",
                              input_formats=('%d.%m.%Y',))
    date_out = forms.DateField(required=False,
                               widget=forms.DateInput(
                                   attrs={'class': 'form-control datepicker-input',
                                          'data-target': '#date_out_form',
                                          'data-inputmask-alias': 'datetime',
                                          'data-inputmask-inputformat': 'dd.mm.yyyy',
                                          'data-mask': "00.00.0000",
                                          'inputmode': "numeric"
                                          }, format='%d.%m.%Y'
                               ), label="Дата до",
                               input_formats=('%d.%m.%Y',))

    def __init__(self, *args, **kwargs):
        workers = kwargs.pop('initial')['user']  # Текущий пользователь
        super().__init__(*args, **kwargs)
        '''Сортировка по управлению'''
        QUERY_WORKERS = [(i.slug, i) for i in User.objects.filter(employee='employee', subdivision=workers.subdivision,
                                                                  department=workers.department).order_by(
            '-chief__rights')]
        QUERY_WORKERS.insert(0, ('own', 'Все сотрудники'))
        self.fields['workers'] = forms.ChoiceField(label='Сотрудники',
                                                   required=False,
                                                   choices=QUERY_WORKERS,
                                                   widget=forms.Select(
                                                       attrs={'class': 'select2', 'style': 'width: 100%'}))

    def clean(self):
        try:
            self.cleaned_data['date_in']
        except Exception as e:
            raise ValidationError('Неправильный формат даты.')
        try:
            self.cleaned_data['date_out']
        except Exception as e:
            raise ValidationError('Неправильный формат даты.')

        if self.cleaned_data['date_in'] and self.cleaned_data['date_out']:
            if self.cleaned_data['date_in'] > self.cleaned_data['date_out']:
                raise ValidationError('Неправильно задан диапазон дат.')
        return self.cleaned_data['date_in']


class Workers_Mission_Control(forms.ModelForm):
    user_current = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].empty_label = "Сотрудник"
        self.fields['organizations_objects'].empty_label = "Объект"
        self.user_current = kwargs['initial']['user_current']
        self.fields['user'].queryset = User.objects.filter(subdivision=self.user_current.subdivision,
                                                           department=self.user_current.department,
                                                           employee='employee').order_by('surname')
        self.fields['organizations_objects'].queryset = Organizations_Objects.objects.filter(
            development_tasks__subdivision=self.user_current.subdivision,
            development_tasks__department=self.user_current.department).order_by('-name').distinct()

    class Meta:
        model = Workers_Mission
        fields = ['user', 'organizations_objects', 'date_departure', 'date_start', 'date_end', 'date_arrival', 'status']
        widgets = {
            'user': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'organizations_objects': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'status': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
        }

    date_departure = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input',
                   'data-target': '#date_departure_form',
                   'data-inputmask-alias': 'datetime',
                   'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   'inputmode': "numeric"
                   }, format='%d.%m.%Y'
        ), label="Дата выезда",
        input_formats=('%d.%m.%Y',)
    )
    date_start = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input',
                   'data-target': '#date_start_form',
                   'data-inputmask-alias': 'datetime',
                   'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   'inputmode': "numeric"
                   }, format='%d.%m.%Y'
        ), label="Дата начала работы",
        input_formats=('%d.%m.%Y',)
    )
    date_end = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input',
                   'data-target': '#date_end_form',
                   'data-inputmask-alias': 'datetime',
                   'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   'inputmode': "numeric"
                   }, format='%d.%m.%Y'
        ), label="Дата окончание работы",
        input_formats=('%d.%m.%Y',)
    )
    date_arrival = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input',
                   'data-target': '#date_arrival_form',
                   'data-inputmask-alias': 'datetime',
                   'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   'inputmode': "numeric"
                   }, format='%d.%m.%Y'
        ), label="Дата прибытия",
        input_formats=('%d.%m.%Y',)
    )

    def clean(self):
        date_departure = self.cleaned_data['date_departure']
        date_start = self.cleaned_data['date_start']
        date_end = self.cleaned_data['date_end']
        date_arrival = self.cleaned_data['date_arrival']
        workers = self.cleaned_data['user']
        if date_departure > date_start:
            raise ValidationError('Дата выезда не может быть больше даты выхода на работу.')

        if date_end > date_arrival:
            raise ValidationError('Дата окончания работ не может быть больше даты выезда.')

        if date_departure > date_arrival:
            raise ValidationError('Дата выезда не может быть больше даты прибытия.')
        """Проверки на заполенение базы данных по Workers_Missing,Workers_Weekend_Work"""

        """ Проверка на Отсутсвие"""
        missings = Workers_Missing.objects.filter(date_start__gte=date_departure - relativedelta(months=6),
                                                  date_end__lte=date_arrival + relativedelta(months=6), user=workers)
        for missing in missings:
            """Если даты попадают в диапазон"""
            if date_departure >= missing.date_start and date_departure <= missing.date_end or date_arrival >= missing.date_start and date_arrival <= missing.date_end:
                raise ValidationError(
                    '{0} уже отсутсвует с {1} по {2} по причине {3}'.format(workers, missing.date_start,
                                                                            missing.date_end,
                                                                            missing.information_missing))
            if date_departure < missing.date_start and date_arrival > missing.date_end:
                raise ValidationError(
                    '{0} уже отсутсвует с {1} по {2} по причине {3}'.format(workers, missing.date_start,
                                                                            missing.date_end,
                                                                            missing.information_missing))
        """ Проверка на командировки"""
        missions = Workers_Mission.objects.filter(date_start__gte=date_departure - relativedelta(months=6),
                                                  date_end__lte=date_arrival + relativedelta(months=6), user=workers)
        for mission in missions:
            """Если даты попадают в диапазон"""
            if date_departure >= mission.date_departure and date_departure <= mission.date_arrival or date_arrival >= mission.date_departure and date_arrival <= mission.date_arrival:
                raise ValidationError(
                    '{0} уже в командировке с {1} по {2} на объекте {3}'.format(workers, mission.date_departure,
                                                                            mission.date_arrival,
                                                                            mission.organizations_objects))
            if date_departure < mission.date_departure and date_arrival > mission.date_arrival:
                raise ValidationError(
                    '{0} уже в командировке с {1} по {2} на объекте {3}'.format(workers, mission.date_departure,
                                                                            mission.date_arrival,
                                                                            mission.organizations_objects))
        """Максимальный срок командировки"""
        if (date_arrival - date_departure).days > 120:
            raise ValidationError('Максимальный срок отсутствия 120 дней.')


class Workers_Mission_Filter(forms.Form):
    date_in = forms.DateField(required=False,
                              widget=forms.DateInput(
                                  attrs={'class': 'form-control datepicker-input',
                                         'data-target': '#date_in_form',
                                         'data-inputmask-alias': 'datetime',
                                         'data-inputmask-inputformat': 'dd.mm.yyyy',
                                         'data-mask': "00.00.0000",
                                         'inputmode': "numeric"
                                         }, format='%d.%m.%Y'
                              ), label="Дата от",
                              input_formats=('%d.%m.%Y',))
    date_out = forms.DateField(required=False,
                               widget=forms.DateInput(
                                   attrs={'class': 'form-control datepicker-input',
                                          'data-target': '#date_out_form',
                                          'data-inputmask-alias': 'datetime',
                                          'data-inputmask-inputformat': 'dd.mm.yyyy',
                                          'data-mask': "00.00.0000",
                                          'inputmode': "numeric"
                                          }, format='%d.%m.%Y'
                               ), label="Дата до",
                               input_formats=('%d.%m.%Y',))

    def __init__(self, *args, **kwargs):
        workers = kwargs.pop('initial')['user']  # Текущий пользователь
        super().__init__(*args, **kwargs)
        '''Сортировка по управлению'''
        QUERY_WORKERS = [(i.slug, i) for i in User.objects.filter(employee='employee', subdivision=workers.subdivision,
                                                                  department=workers.department).order_by(
            '-chief__rights')]
        QUERY_WORKERS.insert(0, ('own', 'Все сотрудники'))
        self.fields['workers'] = forms.ChoiceField(label='Сотрудники',
                                                   required=False,
                                                   choices=QUERY_WORKERS,
                                                   widget=forms.Select(
                                                       attrs={'class': 'select2', 'style': 'width: 100%'}))
        QUERY_ORGANIZATIONS_OBJECTS = [(i.slug, i.name) for i in Organizations_Objects.objects.filter(
            development_tasks__subdivision=workers.subdivision,
            development_tasks__department=workers.department).order_by('-name').distinct()]
        QUERY_ORGANIZATIONS_OBJECTS.insert(0, ('own', 'Все объекты'))
        self.fields['organizations_objects'] = forms.ChoiceField(label='Объекты',
                                                                 required=False,
                                                                 choices=QUERY_ORGANIZATIONS_OBJECTS,
                                                                 widget=forms.Select(
                                                                     attrs={'class': 'select2',
                                                                            'style': 'width: 100%'}))

    def clean(self):
        try:
            self.cleaned_data['date_in']
        except Exception as e:
            raise ValidationError('Неправильный формат даты.')
        try:
            self.cleaned_data['date_out']
        except Exception as e:
            raise ValidationError('Неправильный формат даты.')

        if self.cleaned_data['date_in'] and self.cleaned_data['date_out']:
            if self.cleaned_data['date_in'] > self.cleaned_data['date_out']:
                raise ValidationError('Неправильно задан диапазон дат.')
        return self.cleaned_data['date_in']


class Workers_Weekend_Work_Control(forms.ModelForm):
    user_current = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].empty_label = "Сотрудник"
        self.user_current = kwargs['initial']['user_current']
        self.fields['user'].queryset = User.objects.filter(subdivision=self.user_current.subdivision,
                                                           department=self.user_current.department,
                                                           employee='employee').order_by('surname')

    class Meta:
        model = Workers_Weekend_Work
        fields = ['user', 'date', 'planning', 'hours_working']
        widgets = {
            'user': forms.Select(
                attrs={'class': 'select2', 'style': 'width: 100%'}),
            'planning': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Планирование работ', 'id': 'planning'}),

        }

    date = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control datepicker-input',
                   'data-target': '#date_form',
                   'data-inputmask-alias': 'datetime',
                   'data-inputmask-inputformat': 'dd.mm.yyyy',
                   'data-mask': "00.00.0000",
                   'inputmode': "numeric"
                   }, format='%d.%m.%Y'
        ), label="Дата",
        input_formats=('%d.%m.%Y',)
    )

    def clean_date(self):
        """Добавить проверку на командировку, отсутствие"""
        date = self.cleaned_data['date']
        workers = self.cleaned_data['user']
        """Проверка на командировку"""

        mission = Workers_Mission.objects.filter(date_departure__lte=date, user=workers).last()
        if mission:
            if date >= mission.date_departure and date <= mission.date_arrival:
                raise ValidationError(
                    '{0} находиться в командировке {1}.'.format(workers, mission.organizations_objects))
        """ Проверка на Отсутсвие"""
        missing = Workers_Missing.objects.filter(date_start__lte=date, user=workers).last()
        if missing:
            if date >= missing.date_start and date <= missing.date_end:
                raise ValidationError('{0} отсутствует по причине  {1}.'.format(workers, missing.information_missing))
        """ Проверка на выходной или праздник"""
        schedule = Information_Schedule.objects.filter(date=date)
        if not schedule:
            if not date.weekday() == 6 and not date.weekday() == 5:
                raise ValidationError(
                    'Вы не можете записать {0}. Данный день не выходной и не праздник.'.format(workers))
        """ Проверка на повторную запись"""
        weekend_work = Workers_Weekend_Work.objects.filter(date=date)
        if weekend_work:
            raise ValidationError('Данный сотрудник уже записан.')
        return date


class Workers_Weekend_Work_Control_Time(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Workers_Weekend_Work
        fields = ['hours_working', ]
        widgets = {
            'hours_working': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Отработанное время', 'id': 'hours_working'}),
        }


class Workers_Weekend_Work_Filter(forms.Form):
    date_in = forms.DateField(required=False,
                              widget=forms.DateInput(
                                  attrs={'class': 'form-control datepicker-input',
                                         'data-target': '#date_in_form',
                                         'data-inputmask-alias': 'datetime',
                                         'data-inputmask-inputformat': 'dd.mm.yyyy',
                                         'data-mask': "00.00.0000",
                                         'inputmode': "numeric"
                                         }, format='%d.%m.%Y'
                              ), label="Дата от",
                              input_formats=('%d.%m.%Y',))
    date_out = forms.DateField(required=False,
                               widget=forms.DateInput(
                                   attrs={'class': 'form-control datepicker-input',
                                          'data-target': '#date_out_form',
                                          'data-inputmask-alias': 'datetime',
                                          'data-inputmask-inputformat': 'dd.mm.yyyy',
                                          'data-mask': "00.00.0000",
                                          'inputmode': "numeric"
                                          }, format='%d.%m.%Y'
                               ), label="Дата до",
                               input_formats=('%d.%m.%Y',))

    def __init__(self, *args, **kwargs):
        workers = kwargs.pop('initial')['user']  # Текущий пользователь
        super().__init__(*args, **kwargs)
        '''Сортировка по управлению'''
        QUERY_WORKERS = [(i.slug, i) for i in User.objects.filter(employee='employee', subdivision=workers.subdivision,
                                                                  department=workers.department).order_by(
            '-chief__rights')]
        QUERY_WORKERS.insert(0, ('own', 'Все сотрудники'))
        self.fields['workers'] = forms.ChoiceField(label='Сотрудники',
                                                   required=False,
                                                   choices=QUERY_WORKERS,
                                                   widget=forms.Select(
                                                       attrs={'class': 'select2', 'style': 'width: 100%'}))

    def clean(self):
        try:
            self.cleaned_data['date_in']
        except Exception as e:
            raise ValidationError('Неправильный формат даты.')
        try:
            self.cleaned_data['date_out']
        except Exception as e:
            raise ValidationError('Неправильный формат даты.')

        if self.cleaned_data['date_in'] and self.cleaned_data['date_out']:
            if self.cleaned_data['date_in'] > self.cleaned_data['date_out']:
                raise ValidationError('Неправильно задан диапазон дат.')
        return self.cleaned_data['date_in']


class Workers_Work_Planning_Filter(forms.Form):
    """Форма для поиска и фильтрации"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['year'] = forms.IntegerField(label='Год', required=False, widget=forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'Год', 'id': 'year'}))
        self.fields['month'] = forms.IntegerField(label='Месяц', required=False, widget=forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'Месяц', 'id': 'month'}))

    def clean(self):
        try:
            if self.cleaned_data['year']:
                year = int(self.cleaned_data['year'])
                if year > 2030:
                    raise ValidationError('Уменьшите год.')
                if year < 2000:
                    raise ValidationError('Увеличьте год.')
        except Exception as e:
            raise ValidationError('Неправильный формат года.')
        try:
            if self.cleaned_data['month']:
                year = int(self.cleaned_data['month'])
                if year > 12:
                    raise ValidationError('Уменьшите месяц.')
                if year < 1:
                    raise ValidationError('Увеличьте месяц.')
        except Exception as e:
            raise ValidationError('Неправильный формат месяца.')
