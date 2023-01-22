import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages

from workers.forms import Certificates_Workers_Form_Control, Certificates_Form_Control, Certificates_Parts_Form_Control, \
    Certificates_Workers_All_Form_Control, Certificates_Parts_Form_Control
from workers.mixin.rights_mixin import ViewsPermissionsMixin
from workers.models import Сertificates, Сertificate_Users, User, Сertificate_Parts
from workers.utils import DataMixin


class Certificate_Workers(DataMixin, ListView):
    model = Сertificate_Users
    template_name = 'workers/certificates_workers.html'
    login_url = 'login'
    redirect_field_name = ''
    context_object_name = 'certificate_workers'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Сертификаты.')
        # Вспомогальные запросы
        query_subdivision = self.request.GET.get('subdivision') if self.request.GET.get(
            'subdivision') else self.request.user.subdivision
        query_department = self.request.GET.get('department') if self.request.GET.get(
            'department') else self.request.user.department
        query_employee = self.request.GET.get('employee') if self.request.GET.get('employee') else 'employee'
        # Список таблицы сертификатов
        certif_parts = Сertificate_Parts.objects.filter(state=True).select_related("certificates").all()
        table = dict()
        for certificate in Сertificates.objects.filter(state=True):
            table[certificate] = [x for x in certif_parts if x.certificates == certificate]
        context['certificate_table'] = table
        # формирование таблицы пользователей
        workers = User.objects.filter(employee=query_employee, subdivision=query_subdivision,
                                      department=query_department).order_by('-chief__rights')

        cetificates = Сertificate_Users.objects.filter(user__employee=query_employee,
                                                       user__subdivision=query_subdivision,
                                                       user__department=query_department,
                                                       certificate__state=True).order_by('-date_delivery')
        # Создаем список все сотрудников с пустыми сертификатами
        list_cetificates_users = list()
        for worker in workers:
            user_cetificate = dict()
            user_cetificate['workers'] = worker
            for certif_part in certif_parts:
                user_cetificate[certif_part] = None
            list_cetificates_users.append(user_cetificate)
        # Заполняем все сертификаты. С пустой формы.
        for list_cetificate_user in list_cetificates_users:
            for cetificate in cetificates:
                # Опеределяем сертификат пользователя
                if list_cetificate_user['workers'] == cetificate.user:
                    # Просроченные сертификаты
                    old_cetificate = datetime.datetime.now().date() - cetificate.date_delivery
                    if int(old_cetificate.days) - cetificate.certificate.validity * 30 < 0:
                        # Добавить проверку последнего сертификата
                        if list_cetificate_user[cetificate.certificate] == None:
                            del list_cetificate_user[cetificate.certificate]
                            list_cetificate_user[cetificate.certificate] = cetificate
                        else:
                            # Выбираем последний сертификат по дате.
                            if cetificate.date_delivery > list_cetificate_user[cetificate.certificate].date_delivery:
                                del list_cetificate_user[cetificate.certificate]
                                list_cetificate_user[cetificate.certificate] = cetificate
                        # Обнуляем если сменилась должность
                        if cetificate.certificate.change_chief:
                            if list_cetificate_user['workers'].chief != cetificate.chief:
                                del list_cetificate_user[cetificate.certificate]
                                user_cetificate[cetificate.certificate] = None

        context = dict(list(context.items()) + list(project_menus.items()))
        context['list_cetificates'] = list_cetificates_users
        return context


class Certificate_Workers_Add(DataMixin, CreateView):
    model = Сertificate_Users
    template_name = 'workers/certificates_workers_add.html'
    form_class = Certificates_Workers_Form_Control
    user_add = ''

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Добавить сертификаты.')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context

    def get_success_url(self):
        messages.success(self.request, "Данные сохранены успешно")
        return reverse('workers_certificate_add', kwargs={'workers_slug': self.kwargs['workers_slug']})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.chief = self.request.user.chief
        self.object.save()
        return super().form_valid(form)


class Certificate_Workers_Add_All(DataMixin, CreateView):
    model = Сertificate_Users
    template_name = 'workers/certificates_workers_add_all.html'
    form_class = Certificates_Workers_All_Form_Control
    user_add = ''

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Certificate_Workers_Add_All, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Добавить сертификаты.')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context

    def get_form_kwargs(self):
        kwargs = super(Certificate_Workers_Add_All, self).get_form_kwargs()
        kwargs['initial']['user_current'] = self.request.user
        return kwargs

    def get_success_url(self):
        messages.success(self.request, "Данные сохранены успешно")
        return reverse('workers_certificate_add_all')


class Сertificates_View(LoginRequiredMixin, ViewsPermissionsMixin, DataMixin, ListView):
    '''Сертификаты. Визуализация.'''
    model = Сertificates
    template_name = 'workers/certificates.html'
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.certificates_view'

    def get(self, *args, **kwargs):
        if self.request.user.has_perm('workers.certificates_delete'):
            query = self.request.GET.get('remove')
            if query != None:
                try:
                    remove = Сertificates.objects.get(slug=query)
                    remove.delete()
                except:
                    pass

        certificates = Сertificates.objects.all()  # Запрос
        context = {'certificates': certificates, }

        project_menus = self.get_user_context(title='Сертификаты')
        context = dict(list(context.items()) + list(project_menus.items()))

        return render(self.request, self.template_name, context)


class Сertificates_Update(LoginRequiredMixin, ViewsPermissionsMixin, DataMixin, UpdateView):
    '''Сертификаты. Изменение '''
    model = Сertificates
    template_name = 'workers/certificates_control.html'
    form_class = Certificates_Form_Control
    success_url = reverse_lazy('certificates')
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.certificates_change'

    # Управление по slug
    def get_object(self, queryset=None):
        instance = Сertificates.objects.get(slug=self.kwargs.get('сertificates_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Редактирование сертификатов')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Сertificates_Add(LoginRequiredMixin, ViewsPermissionsMixin, DataMixin, CreateView):
    '''Сертификаты. Добавление. '''
    model = Сertificates
    template_name = 'workers/certificates_control.html'
    success_url = reverse_lazy('certificates')
    form_class = Certificates_Form_Control
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.certificates_add'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Добавление сертификатов')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Сertificates_Parts_View(LoginRequiredMixin, ViewsPermissionsMixin, DataMixin, ListView):
    '''Части сертификатов. Визуализация.'''
    model = Сertificate_Parts
    template_name = 'workers/certificates_parts.html'
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.certificate_parts_view'

    def get(self, *args, **kwargs):
        if self.request.user.has_perm('workers.certificate_parts_delete'):
            query = self.request.GET.get('remove')
            if query != None:
                try:
                    remove = Сertificate_Parts.objects.get(slug=query)
                    remove.delete()
                except:
                    pass

        certificates_parts = Сertificate_Parts.objects.all()  # Запрос
        context = {'certificates_parts': certificates_parts, }

        project_menus = self.get_user_context(title='Части сертификатов')
        context = dict(list(context.items()) + list(project_menus.items()))

        return render(self.request, self.template_name, context)


class Сertificates_Parts_Update(LoginRequiredMixin, ViewsPermissionsMixin, DataMixin, UpdateView):
    '''Части сертификатов. Изменение '''
    model = Сertificate_Parts
    template_name = 'workers/certificates_parts_control.html'
    form_class = Certificates_Parts_Form_Control
    success_url = reverse_lazy('certificates')
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.certificate_parts_change'

    # Управление по slug
    def get_object(self, queryset=None):
        instance = Сertificate_Parts.objects.get(slug=self.kwargs.get('сertificates_parts_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Редактирование частей сертификатов')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Сertificates_Parts_Add(LoginRequiredMixin, ViewsPermissionsMixin, DataMixin, CreateView):
    '''Части сертификатов. Добавление. '''
    model = Сertificate_Parts
    template_name = 'workers/certificates_parts_control.html'
    success_url = reverse_lazy('certificates_parts')
    form_class = Certificates_Parts_Form_Control
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.certificate_parts_add'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Добавление частей сертификатов')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context
