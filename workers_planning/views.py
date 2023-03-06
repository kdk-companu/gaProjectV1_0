from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.template.defaultfilters import addslashes
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, TemplateView
from workers.models import User
from workers.utils import DataMixin
from workers_planning.forms import Information_Schedule_Filter, Information_Schedule_Control, \
    Information_Missing_Control, Workers_Missing_Control, Workers_Missing_Filter, Workers_Mission_Filter, \
    Workers_Mission_Control, Workers_Weekend_Work_Filter, Workers_Weekend_Work_Control, \
    Workers_Weekend_Work_Control_Time, Workers_Work_Planning_Filter
from workers_planning.models import Workers_Mission, Information_Schedule, Information_Missing, Workers_Missing, \
    Workers_Weekend_Work
import datetime


class Information_Schedule_View(DataMixin, ListView):
    """Информация о выходных днях и празднках"""
    model = Information_Schedule
    template_name = 'workers_planning/settings_information_schedule_view.html'
    context_object_name = 'information_schedules'

    def get(self, *args, **kwargs):
        if self.request.user.has_perm('workers.delete_subdivision'):
            query = self.request.GET.get('remove')
            if query != None:
                try:
                    remove = Information_Schedule.objects.get(pk=query)
                    remove.delete()
                except:
                    pass
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_queryset(self):
        date_start = datetime.date(datetime.datetime.now().year, 1, 1)
        date_end = datetime.date(datetime.datetime.now().year + 1, 1, 1)
        if self.request.GET:
            form = Information_Schedule_Filter(self.request.GET)
            if form.is_valid():
                try:
                    year = int(addslashes(str(self.request.GET.get('year'))))
                    date_start = datetime.date(year, 1, 1)
                    date_end = datetime.date(year + 1, 1, 1)
                except Exception as e:
                    pass

        return Information_Schedule.objects.filter(
            Q(date__lte=date_end - relativedelta(days=1)) & Q(date__gte=date_start)).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Информация о выходных днях и праздниках')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['form_filter'] = Information_Schedule_Filter(self.request.GET)
        return context


class Information_Schedule_Add(DataMixin, CreateView):
    model = Information_Schedule
    template_name = 'workers_planning/settings_information_schedule_control.html'
    form_class = Information_Schedule_Control
    success_url = reverse_lazy('information_schedule')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Добавить информацию о выходных днях и праздниках')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Information_Schedule_Edit(DataMixin, UpdateView):
    model = Information_Schedule
    template_name = 'workers_planning/settings_information_schedule_control.html'
    form_class = Information_Schedule_Control
    success_url = reverse_lazy('information_schedule')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Information_Schedule_Edit, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Редактировать информация о выходных днях и праздниках')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Information_Missing_View(DataMixin, ListView):
    """Причины отсутсвия на работе."""
    model = Information_Missing
    template_name = 'workers_planning/settings_information_missing_view.html'
    context_object_name = 'information_missings'

    def get(self, *args, **kwargs):
        if self.request.user.has_perm('workers.delete_subdivision'):
            query = self.request.GET.get('remove')
            if query != None:
                try:
                    remove = Information_Missing.objects.get(slug=query)
                    remove.delete()
                except:
                    pass
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Информация о выходных днях и праздниках')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['form_filter'] = Information_Schedule_Filter(self.request.GET)
        return context


class Information_Missing_Add(DataMixin, CreateView):
    model = Information_Missing
    template_name = 'workers_planning/settings_information_missing_control.html'
    form_class = Information_Missing_Control
    success_url = reverse_lazy('information_missing')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Добавить причины отсутсвия на работе')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Information_Missing_Edit(DataMixin, UpdateView):
    """Департамент. Изменение"""
    model = Information_Missing
    template_name = 'workers_planning/settings_information_missing_control.html'
    form_class = Information_Missing_Control
    success_url = reverse_lazy('information_missing')

    def get_object(self, queryset=None):
        instance = Information_Missing.objects.get(slug=self.kwargs.get('information_missing_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Редактирование причин отсутсвия на работе')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


def date_out(month: int, yers: int, lasting=2, schedules=None):
    """Функция выводит дни. Для отрисовки верхней шапки"""
    MONTH_SELECT = {1: 'Январь', 2: 'Февраль', 3: 'Март',
                    4: 'Апрель', 5: 'Май', 6: 'Июнь', 7: 'Июль',
                    8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'}
    date_begin = datetime.date(yers, month, 1)
    calendar = dict()
    month_start = date_begin
    for i in range(0, lasting):
        calendar_days = list()
        for d in range(0, ((month_start + relativedelta(months=1)) - month_start).days):
            day_d = month_start + datetime.timedelta(days=d)
            day_not_working = None
            if len(schedules) > 0:
                for schedule in schedules:
                    if day_d == schedule[0]:
                        day_not_working = False if schedule[1] else True
                        schedules.remove(schedule)
                        break
            if day_not_working == None:
                day_not_working = True if day_d.weekday() == 6 or day_d.weekday() == 5 else False
            calendar_days.append([day_d, day_not_working])
        calendar[MONTH_SELECT[month_start.month]] = calendar_days
        month_start += relativedelta(months=1)
    return calendar


def workers_report_card(month: int, yers: int, lasting=2, schedules=None, missions=None, workers=None):
    """Структура данных на выходе
        User
        -[[bool mission(true- командировка,False-офис),'дата',int кол-во дней, 'объект','final',Не рабочий день],]
    """
    lastings = ((datetime.date(yers, month, 1) + relativedelta(months=lasting)) - datetime.date(yers, month, 1)).days
    month_start = datetime.date(yers, month, 1)
    list_days = list()
    '''Подготовка всех дат'''
    for d in range(0, lastings):
        day_d = month_start + datetime.timedelta(days=d)
        day_not_working = None
        if len(schedules) > 0:
            for schedule in schedules:
                if day_d == schedule[0]:
                    day_not_working = False if schedule[1] else True
                    schedules.remove(schedule)
                    break
        if day_not_working == None:
            day_not_working = True if day_d.weekday() == 6 or day_d.weekday() == 5 else False
        list_days.append([False, day_d, 1, '', '', day_not_working])

    '''Заполнятеся словарь дататами для сотрудников'''
    workers_date = dict()
    for worker in workers:
        workers_date[worker] = list_days.copy()
    '''Заполнение командировок'''
    for worker in workers:
        for mission in missions:
            if worker == mission[0]:
                '''<User: Пятыгин Юрий Витальевич>, 'Заполярка', 2 - datetime.date(2023, 2, 2), datetime.date(2023, 2, 10), 'final'''
                n_date_start = mission[2] - (datetime.date(yers, month, 1))  # День начала командировки
                n_count_day = (mission[3] - mission[2]).days + 1  # Кол-во командировки
                max_date = datetime.date(yers, month, 1) + relativedelta(months=lasting + 1) - relativedelta(
                    days=1)  # Максимальная дата
                '''Ограничение на максимальную дату'''
                if mission[3] > max_date:
                    n_count_day = (max_date - mission[2]).days
                '''Собираем итоговый вид'''
                for i in range(len(workers_date[worker])):
                    if mission[2] == workers_date[worker][i][1]:
                        start_date = workers_date[worker][0:i]
                        update_date = [[True, n_date_start, n_count_day, mission[1], mission[4], False], ]
                        end_date = workers_date[worker][i + n_count_day:len(workers_date[worker])]
                workers_date[worker] = start_date + update_date + end_date
    return workers_date


class Workers_Report_Card_View(DataMixin, ListView):
    """ """
    model = Workers_Mission
    template_name = 'workers_planning/workers_report_card.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Сотрудники.')
        context = dict(list(context.items()) + list(project_menus.items()))
        """Выборка"""
        in_date_month = 2
        in_date_year = 2023
        in_month_see = 2
        in_date = datetime.date(in_date_year, in_date_month, 1)
        """Верхняя часть календаря"""
        calendar_base = Information_Schedule.objects.filter(date__gte=datetime.date(in_date_year, in_date_month, 1),
                                                            date__lte=datetime.date(in_date_year, in_date_month, 1)
                                                                      + relativedelta(months=in_month_see))
        calendar_base_out = [(d.date, d.work) for d in calendar_base]
        context['calendar'] = date_out(in_date_month, in_date_year, lasting=in_month_see,
                                       schedules=calendar_base_out.copy())
        """Заполнение пользователей"""
        workers = User.objects.all()
        # Запрос идет на 7 месяцев раньше
        query_start = datetime.date(in_date_year, in_date_month, 1)
        query_end = datetime.date(in_date_year, in_date_month, 1) + relativedelta(months=in_month_see + 1)
        calendar_user_base_range = Workers_Mission.objects.filter(date_start__gte=query_start, date_end__lte=query_end)
        '''Список командировок'''
        calendar_user_base_out = [(d.user, d.organizations_objects.short_names, d.date_start, d.date_end, d.status) for
                                  d in
                                  calendar_user_base_range]
        '''Получение последней командировки от запрощенной даты'''
        for worker in workers:
            calendar_user_base_up_range = Workers_Mission.objects.filter(date_start__lte=query_start,
                                                                         user=worker).order_by('-date_start').first()
            if calendar_user_base_up_range:
                if calendar_user_base_up_range.date_end > in_date:
                    print(calendar_user_base_up_range.date_start)
                    print(calendar_user_base_up_range.date_end)
                    calendar_user_base_out.append((calendar_user_base_up_range.user,
                                                   calendar_user_base_up_range.organizations_objects.short_names,
                                                   in_date,
                                                   calendar_user_base_up_range.date_end,
                                                   calendar_user_base_up_range.status))

        context['workers_missions'] = workers_report_card(in_date_month, in_date_year, lasting=in_month_see,
                                                          schedules=calendar_base_out.copy(),
                                                          missions=calendar_user_base_out, workers=workers)

        return context


class Workers_Missing_View(DataMixin, ListView):
    paginate_by = 25
    model = Workers_Missing
    template_name = 'workers_planning/workers_missing_view.html'
    context_object_name = 'workers_missing'

    def get_queryset(self):
        date_start = datetime.date(datetime.datetime.now().year, 1, 1)
        date_end = datetime.date(datetime.datetime.now().year + 1, 1, 1)
        filters = Q()  # создаем первый объект Q, что бы складывать с ним другие
        """Обработка GET Запросов"""
        if self.request.GET:
            """Проверка формы для запроса"""
            form = Workers_Missing_Filter(self.request.GET, initial={'user': self.request.user})
            if form.is_valid():
                if not self.request.GET.get('date_in') == '' and self.request.GET.get('date_in'):
                    get_date_in = self.request.GET.get('date_in').split('.')
                    date_start = datetime.date(int(get_date_in[2]), int(get_date_in[1]), int(get_date_in[0]))
                if not self.request.GET.get('date_out') == '' and self.request.GET.get('date_out'):
                    get_date_out = self.request.GET.get('date_out').split('.')
                    date_end = datetime.date(int(get_date_out[2]), int(get_date_out[1]), int(get_date_out[0]))
                get_workers = 'own'
                if self.request.GET.get('workers'):
                    get_workers = addslashes(self.request.GET.get('workers'))
                if not get_workers == 'own':
                    filters &= Q(**{f'{"user__slug"}': get_workers})
        """Фильтр в базу данных"""
        filters &= Q(**{f'{"date_start__gte"}': date_start})
        filters &= Q(**{f'{"date_start__lte"}': date_end})
        if self.request.user.subdivision:
            filters &= Q(**{f'{"user__subdivision"}': self.request.user.subdivision})
        if self.request.user.department:
            filters &= Q(**{f'{"user__department"}': self.request.user.department})

        return Workers_Missing.objects.filter(filters).order_by('-date_start')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Отсутсвие сотрудников')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['form_filter'] = Workers_Missing_Filter(self.request.GET, initial={'user': self.request.user})
        context['url_filter'] = ""
        if self.request.GET:
            dateIn = ''
            dateOut = ''
            workers = 'own'
            try:
                dateIn = self.request.GET['date_in']
            except Exception as e:
                pass
            try:
                dateOut = self.request.GET['date_out']
            except Exception as e:
                pass
            try:
                workers = self.request.GET['workers']
            except Exception as e:
                pass
            context['url_filter'] = "?date_in={0}&date_out={1}&workers={2}".format((dateIn), dateOut, workers)
        return context


class Workers_Missing_Add(DataMixin, CreateView):
    model = Workers_Missing
    template_name = 'workers_planning/workers_missing_control.html'
    form_class = Workers_Missing_Control
    success_url = reverse_lazy('workers_missing')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Добавить отсутсвие сотрудника')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context

    def get_form_kwargs(self):
        kwargs = super(Workers_Missing_Add, self).get_form_kwargs()
        kwargs['initial']['user_current'] = self.request.user
        return kwargs


class Workers_Missing_Edit(DataMixin, UpdateView):
    model = Workers_Missing
    template_name = 'workers_planning/workers_missing_control.html'
    form_class = Workers_Missing_Control
    success_url = reverse_lazy('workers_missing')

    def get_form_kwargs(self):
        kwargs = super(Workers_Missing_Edit, self).get_form_kwargs()
        kwargs['initial']['user_current'] = self.request.user
        return kwargs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Workers_Missing_Edit, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Редактировать отсутсвие сотрудника')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Workers_Missing_Delete(DataMixin, DeleteView):
    model = Workers_Missing
    template_name = 'workers_planning/workers_missing_delete.html'
    success_url = reverse_lazy('workers_missing')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Workers_Missing_Delete, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Удаление задания на разработку')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Workers_Mission_View(DataMixin, ListView):
    paginate_by = 25
    model = Workers_Mission
    template_name = 'workers_planning/workers_mission_view.html'
    context_object_name = 'worker_missions'

    def get_queryset(self):
        date_departure = datetime.date(datetime.datetime.now().year, 1, 1)
        date_arrival = datetime.date(datetime.datetime.now().year + 1, 1, 1)
        filters = Q()  # создаем первый объект Q, что бы складывать с ним другие
        """Обработка GET Запросов"""
        if self.request.GET:
            """Проверка формы для запроса"""
            form = Workers_Mission_Filter(self.request.GET, initial={'user': self.request.user})
            if form.is_valid():
                # Даты
                if not self.request.GET.get('date_in') == '' and self.request.GET.get('date_in'):
                    get_date_in = self.request.GET.get('date_in').split('.')
                    date_departure = datetime.date(int(get_date_in[2]), int(get_date_in[1]), int(get_date_in[0]))
                if not self.request.GET.get('date_out') == '' and self.request.GET.get('date_out'):
                    get_date_out = self.request.GET.get('date_out').split('.')
                    date_arrival = datetime.date(int(get_date_out[2]), int(get_date_out[1]), int(get_date_out[0]))
                # Пользователь
                get_workers = 'own'
                if self.request.GET.get('workers'):
                    get_workers = addslashes(self.request.GET.get('workers'))
                if not get_workers == 'own':
                    filters &= Q(**{f'{"user__slug"}': get_workers})
                #
                get_organizations_objects = 'own'
                if self.request.GET.get('organizations_objects'):
                    get_organizations_objects = addslashes(self.request.GET.get('organizations_objects'))
                if not get_organizations_objects == 'own':
                    filters &= Q(**{f'{"organizations_objects__slug"}': get_organizations_objects})

        """Фильтр в базу данных"""
        filters &= Q(**{f'{"date_departure__gte"}': date_departure})
        filters &= Q(**{f'{"date_arrival__lte"}': date_arrival})
        if self.request.user.subdivision:
            filters &= Q(**{f'{"user__subdivision"}': self.request.user.subdivision})
        if self.request.user.department:
            filters &= Q(**{f'{"user__department"}': self.request.user.department})

        # return Workers_Mission.objects.filter(filters).order_by('-date_departure')

        return Workers_Mission.objects.filter(filters).order_by('-date_departure')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Командировки сотрудников')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['form_filter'] = Workers_Mission_Filter(self.request.GET, initial={'user': self.request.user})
        context['url_filter'] = ""
        if self.request.GET:
            dateIn = ''
            dateOut = ''
            workers = 'own'
            try:
                dateIn = self.request.GET['date_in']
            except Exception as e:
                pass
            try:
                dateOut = self.request.GET['date_out']
            except Exception as e:
                pass
            try:
                workers = self.request.GET['workers']
            except Exception as e:
                pass
            context['url_filter'] = "?date_in={0}&date_out={1}&workers={2}".format((dateIn), dateOut, workers)
        return context


class Workers_Mission_Add(DataMixin, CreateView):
    model = Workers_Mission
    template_name = 'workers_planning/workers_mission_control.html'
    form_class = Workers_Mission_Control
    success_url = reverse_lazy('workers_mission')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Добавить командировку сотрудника')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context

    def get_form_kwargs(self):
        kwargs = super(Workers_Mission_Add, self).get_form_kwargs()
        kwargs['initial']['user_current'] = self.request.user
        return kwargs


class Workers_Mission_Edit(DataMixin, UpdateView):
    model = Workers_Mission
    template_name = 'workers_planning/workers_mission_control.html'
    form_class = Workers_Mission_Control
    success_url = reverse_lazy('workers_mission')

    def get_form_kwargs(self):
        kwargs = super(Workers_Mission_Edit, self).get_form_kwargs()
        kwargs['initial']['user_current'] = self.request.user
        return kwargs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Workers_Mission_Edit, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Редактировать командировки сотрудника')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Workers_Mission_Delete(DataMixin, DeleteView):
    model = Workers_Mission
    template_name = 'workers_planning/workers_mission_delete.html'
    success_url = reverse_lazy('workers_mission')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Workers_Mission_Delete, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Удаление командировки сотрудника')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Workers_Weekend_Work_View(DataMixin, ListView):
    paginate_by = 25
    model = Workers_Weekend_Work
    template_name = 'workers_planning/workers_weekend_work_view.html'
    context_object_name = 'workers_weekend_works'

    def get_queryset(self):
        date_start = datetime.date(datetime.datetime.now().year, 1, 1)
        date_end = datetime.date(datetime.datetime.now().year + 1, 1, 1)
        filters = Q()  # создаем первый объект Q, что бы складывать с ним другие
        """Обработка GET Запросов"""
        if self.request.GET:
            """Проверка формы для запроса"""
            form = Workers_Weekend_Work_Filter(self.request.GET, initial={'user': self.request.user})
            if form.is_valid():
                if not self.request.GET.get('date_in') == '' and self.request.GET.get('date_in'):
                    get_date_in = self.request.GET.get('date_in').split('.')
                    date_start = datetime.date(int(get_date_in[2]), int(get_date_in[1]), int(get_date_in[0]))
                if not self.request.GET.get('date_out') == '' and self.request.GET.get('date_out'):
                    get_date_out = self.request.GET.get('date_out').split('.')
                    date_end = datetime.date(int(get_date_out[2]), int(get_date_out[1]), int(get_date_out[0]))
                get_workers = 'own'
                if self.request.GET.get('workers'):
                    get_workers = addslashes(self.request.GET.get('workers'))
                if not get_workers == 'own':
                    filters &= Q(**{f'{"user__slug"}': get_workers})
        """Фильтр в базу данных"""
        filters &= Q(**{f'{"date__gte"}': date_start})
        filters &= Q(**{f'{"date__lte"}': date_end})
        if self.request.user.subdivision:
            filters &= Q(**{f'{"user__subdivision"}': self.request.user.subdivision})
        if self.request.user.department:
            filters &= Q(**{f'{"user__department"}': self.request.user.department})

        # return Workers_Weekend_Work.objects.filter(filters).order_by('-date_start')
        return Workers_Weekend_Work.objects.filter(filters).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Работа на выходные в офисе')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['form_filter'] = Workers_Weekend_Work_Filter(self.request.GET, initial={'user': self.request.user})
        context['url_filter'] = ""
        if self.request.GET:
            dateIn = ''
            dateOut = ''
            workers = 'own'
            try:
                dateIn = self.request.GET['date_in']
            except Exception as e:
                pass
            try:
                dateOut = self.request.GET['date_out']
            except Exception as e:
                pass
            try:
                workers = self.request.GET['workers']
            except Exception as e:
                pass
            context['url_filter'] = "?date_in={0}&date_out={1}&workers={2}".format((dateIn), dateOut, workers)
        return context


class Workers_Weekend_Work_Add(DataMixin, CreateView):
    model = Workers_Weekend_Work
    template_name = 'workers_planning/workers_weekend_work_control.html'
    form_class = Workers_Weekend_Work_Control
    success_url = reverse_lazy('workers_weekend_work')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Добавить сотрудника на работу в выходные')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context

    def get_form_kwargs(self):
        kwargs = super(Workers_Weekend_Work_Add, self).get_form_kwargs()
        kwargs['initial']['user_current'] = self.request.user
        return kwargs


class Workers_Weekend_Work_Time_Add(DataMixin, UpdateView):
    model = Workers_Weekend_Work
    template_name = 'workers_planning/workers_weekend_work_control_time.html'
    form_class = Workers_Weekend_Work_Control_Time
    success_url = reverse_lazy('workers_weekend_work')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Workers_Weekend_Work_Time_Add, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Редактировать время работы')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['workers_weekend_work'] = Workers_Weekend_Work.objects.get(pk=self.kwargs.get('pk', ''))
        return context


class Workers_Weekend_Work_Edit(DataMixin, UpdateView):
    model = Workers_Weekend_Work
    template_name = 'workers_planning/workers_weekend_work_control.html'
    form_class = Workers_Weekend_Work_Control
    success_url = reverse_lazy('workers_weekend_work')

    def get_form_kwargs(self):
        kwargs = super(Workers_Weekend_Work_Edit, self).get_form_kwargs()
        kwargs['initial']['user_current'] = self.request.user
        return kwargs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Workers_Weekend_Work_Edit, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Редактировать отсутсвие сотрудника')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Workers_Weekend_Work_Delete(DataMixin, DeleteView):
    model = Workers_Weekend_Work
    template_name = 'workers_planning/workers_weekend_work_delete.html'
    success_url = reverse_lazy('workers_weekend_work')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Workers_Weekend_Work_Delete, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Удаление работы в выходные')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


def calendar_out(month: int, yers: int, lasting=2):
    """Функция выводит дни. Для отрисовки верхней шапки
    Структура данных:
    {'Февраль':[date(Дата),count(Кол-во дней),text,color]
    """
    MONTH_SELECT = {1: 'Январь', 2: 'Февраль', 3: 'Март',
                    4: 'Апрель', 5: 'Май', 6: 'Июнь', 7: 'Июль',
                    8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'}
    date_begin = datetime.date(yers, month, 1)
    # Запрос к базе данных с праздниками
    schedule_base = Information_Schedule.objects.filter(date__gte=date_begin,
                                                        date__lte=date_begin + relativedelta(months=lasting))
    schedule_base_lists = [(d.date, d.work) for d in schedule_base]
    calendar = dict()
    for i in range(0, lasting):
        calendar_days = list()
        # Проходим по календарным дням
        for d in range(0, ((date_begin + relativedelta(months=1)) - date_begin).days):
            # print(d)
            day_d = date_begin + datetime.timedelta(days=d)
            day_not_working = '#ffffff'
            # # Устанавлививаем праздники
            if len(schedule_base_lists) > 0:
                for schedule_base in schedule_base_lists:
                    if day_d == schedule_base[0]:
                        day_not_working = '#ffffff' if schedule_base[1] else '#b0b7c6'
                        schedule_base_lists.remove(schedule_base)
                        break
            # Добавляем выходные по календарю если нет праздинков и переносов
            if day_not_working == '#ffffff':
                day_not_working = '#b0b7c6' if day_d.weekday() == 6 or day_d.weekday() == 5 else '#ffffff'
            calendar_days.append([day_d, 1, '', day_not_working])

        calendar[MONTH_SELECT[date_begin.month]] = calendar_days
        date_begin += relativedelta(months=1)
    return calendar


def workers_calendar_out(month: int, yers: int, calendar: dict, user, lasting=2):
    """Список дней для пользователя"""
    date_begin = datetime.date(yers, month, 1)
    date_final = (datetime.date(yers, month, 1) + relativedelta(months=lasting)) - relativedelta(days=1)
    workers_calendar_list = list()
    for i, j in calendar.items():
        workers_calendar_list.extend(j)
    """Зарпосы"""
    # 1 Получаем всех пользователей отдела. И заполняем датами
    workers = User.objects.filter(subdivision=user.subdivision, department=user.department,
                                  employee='employee').order_by('chief__rights')
    '''Заполнятеся словарь дататами для сотрудников'''
    workers_calendar = dict()
    for worker in workers:
        workers_calendar[worker] = workers_calendar_list.copy()
    ''' Заполняем отсутсвие сотрудников'''
    workers_missings = Workers_Missing.objects.filter(user__subdivision=user.subdivision,
                                                      user__department=user.department,
                                                      user__employee='employee',
                                                      date_start__gte=date_begin - relativedelta(months=6),
                                                      date_end__lte=date_begin + relativedelta(months=7),
                                                      )
    for workers_missing in workers_missings:
        d_in = date_begin
        d_out = date_final
        d_len = 0
        if not workers_missing.date_end < date_begin or not workers_missing.date_start < date_begin:
            if workers_missing.date_start > date_begin:
                d_in = workers_missing.date_start
            if workers_missing.date_end < date_final:
                d_out = workers_missing.date_end
            d_len = (d_out - d_in).days + 1
            '''Замена в списке'''
            for i in range(len(workers_calendar[workers_missing.user])):
                if workers_calendar[workers_missing.user][i][0] == d_in:
                    n_date_start = workers_calendar[workers_missing.user][0:i]
                    n_date_update = [[d_in, d_len, '', workers_missing.information_missing.color], ]
                    n_date_end = workers_calendar[workers_missing.user][
                                 i + d_len:len(workers_calendar[workers_missing.user])]
                    workers_calendar[workers_missing.user] = n_date_start + n_date_update + n_date_end
                    break
    ''' Заполняем Командировки'''
    workers_missions = Workers_Mission.objects.filter(user__subdivision=user.subdivision,
                                                      user__department=user.department,
                                                      user__employee='employee',
                                                      date_departure__gte=date_begin - relativedelta(months=6),
                                                      date_arrival__lte=date_begin + relativedelta(months=7),
                                                      )
    for workers_mission in workers_missions:
        d_in = date_begin
        d_out = date_final
        d_len = 0
        if not workers_mission.date_arrival < date_begin or not workers_mission.date_departure < date_begin:
            if workers_mission.date_departure > date_begin:
                d_in = workers_mission.date_departure
            if workers_mission.date_arrival < date_final:
                d_out = workers_mission.date_arrival
            d_len = (d_out - d_in).days + 1
            '''Замена в списке'''
            for i in range(len(workers_calendar[workers_mission.user])):
                if workers_calendar[workers_mission.user][i][0] == d_in:
                    n_date_start = workers_calendar[workers_mission.user][0:i]
                    color = '#E75A67' if workers_mission.status == 'final' else '#FB3648'
                    n_date_update = [[d_in, d_len, workers_mission.organizations_objects.short_names, color], ]
                    n_date_end = workers_calendar[workers_mission.user][
                                 i + d_len:len(workers_calendar[workers_mission.user])]
                    workers_calendar[workers_mission.user] = n_date_start + n_date_update + n_date_end
                    break
    ''' Заполняем Выход в выходные'''
    workers_weekend_works = Workers_Weekend_Work.objects.filter(user__subdivision=user.subdivision,
                                                                user__department=user.department,
                                                                user__employee='employee',
                                                                date__gte=date_begin - relativedelta(months=1),
                                                                date__lte=date_begin + relativedelta(months=2),
                                                                )
    for workers_weekend_work in workers_weekend_works:
        '''Замена в списке'''
        for i in range(len(workers_calendar[workers_weekend_work.user])):
            if workers_calendar[workers_weekend_work.user][i][0] == workers_weekend_work.date:
                n_date_start = workers_calendar[workers_weekend_work.user][0:i]
                color = '#76829c'
                hours_working =workers_weekend_work.hours_working if workers_weekend_work.hours_working >-1 else '?'
                n_date_update = [[workers_weekend_work.date, 1, hours_working, color], ]
                n_date_end = workers_calendar[workers_weekend_work.user][
                             i + 1:len(workers_calendar[workers_weekend_work.user])]
                workers_calendar[workers_weekend_work.user] = n_date_start + n_date_update + n_date_end
                break
    return workers_calendar


class Workers_Work_Planning_View(DataMixin, TemplateView):
    """Планирование работ отдела"""
    template_name = 'workers_planning/workers_work_planning_view.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Workers_Work_Planning_View, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Планирование работ')
        context = dict(list(context.items()) + list(project_menus.items()))

        """Выборка"""
        in_date_month = datetime.datetime.now().month
        in_date_year = datetime.datetime.now().year
        in_month_see = 2
        if self.request.GET:
            form = Workers_Work_Planning_Filter(self.request.GET)
            if form.is_valid():
                try:
                    in_date_year = int(addslashes(str(self.request.GET.get('year'))))
                except Exception as e:
                    pass
                try:
                    in_date_month = int(addslashes(str(self.request.GET.get('month'))))
                except Exception as e:
                    pass
        """Верхняя часть календаря"""
        calendar = calendar_out(in_date_month, in_date_year, lasting=in_month_see)
        context['calendar'] = calendar
        """Пользовательская часть календаря"""
        calendar_workers = workers_calendar_out(in_date_month, in_date_year, calendar, self.request.user,
                                                lasting=in_month_see)
        context['calendar_workers'] = calendar_workers
        """форма поиска"""
        context['form_filter'] = Workers_Work_Planning_Filter(self.request.GET)
        """Переходы"""
        date_begin = datetime.date(in_date_year, in_date_month, 1)
        date_up = date_begin + relativedelta(months=1)
        date_down = date_begin - relativedelta(months=1)
        context['up_month'] = "?month={0}&year={1}".format(date_up.month, date_up.year)
        context['down_month'] = "?month={0}&year={1}".format(date_down.month, date_down.year)
        """Описание цвета"""
        information_missing = Information_Missing.objects.all()
        information_missing_lists = [(i.name, i.color) for i in information_missing]
        information_missing_lists.append(['Командировка итоговая', '#E75A67'])
        information_missing_lists.append(['Командировка планируемая', '#FB3648'])
        information_missing_lists.append(['Выходной день', '#b0b7c6'])
        information_missing_lists.append(['Выход в выходной день', '#76829c'])
        context['information_missings'] = information_missing_lists

        return context
