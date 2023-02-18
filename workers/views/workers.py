import os
import shutil
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import PasswordChangeView

from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import Group
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from workers.forms import Workers_Form_Add, Workers_Form_Upload_Images, Workers_Form_PasswordChange, \
    Workers_Form_UpdatePassword, Workers_Form_Update, Workers_Form_Update_Basic, Workers_Form_Update_Closed, \
    Workers_Form_Upload_Passport, Workers_Form_Upload_Signature, Workers_Form_Upload_Snils, Workers_Form_Upload_Inn, \
    Workers_Form_Upload_Archive, Workers_Form_Edit_Сontacts_User, Workers_Form_Edit_Сontacts_User_Basic_Information
from workers.mixin.rights_mixin import ViewsPermissionsMixin

from workers.models import User, User_Basic_Information, User_Closed_Information, Subdivision

from django.contrib import messages

from workers.utils import DataMixin
from django.template.defaultfilters import slugify
from transliterate import translit


class Workers(LoginRequiredMixin, ViewsPermissionsMixin, DataMixin, ListView):
    '''Вывод всех пользователей'''
    model = User
    template_name = 'workers/workers.html'
    login_url = 'login'
    redirect_field_name = ''
    context_object_name = 'workers'
    permission_required = 'workers.workers_view'

    def get_queryset(self):
        '''Возможные запросы'''
        subdivision = self.request.user.subdivision.slug if self.request.user.subdivision else ''
        query_subdivision = self.request.GET.get('subdivision') if self.request.GET.get(
            'subdivision') else subdivision
        department = self.request.user.department.slug if self.request.user.department else ''
        query_department = self.request.GET.get('department') if self.request.GET.get(
            'department') else department

        query_employee = self.request.GET.get('status') if self.request.GET.get('status') else 'employee'

        if query_subdivision == "":
            # Не выбрано упрваление показать всех пользователей.
            return User.objects.filter(employee=query_employee).select_related('user_basic_information').select_related(
                'user_closed_information').order_by('-chief__rights')
        elif department == "":
            return User.objects.filter(employee=query_employee, subdivision__slug=query_subdivision).select_related(
                'user_basic_information').select_related('user_closed_information').order_by('-chief__rights')
        else:
            return User.objects.filter(employee=query_employee, subdivision__slug=query_subdivision,
                                       department__slug=query_department).select_related(
                'user_basic_information').select_related('user_closed_information').order_by('-chief__rights')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Сотрудники.')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Workers_Add(LoginRequiredMixin, ViewsPermissionsMixin, DataMixin, CreateView):
    """Добавление нового сотрудника"""
    model = User
    template_name = 'workers/workers_add.html'
    success_url = reverse_lazy('workers')
    form_class = Workers_Form_Add
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.workers_add_superiors'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Добавление пользователя')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context

    def form_valid(self, form):
        form.save().subdivision = self.request.user.subdivision
        form.save().department = self.request.user.department
        self.object = form.save()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        super()
        # Получение последнего пользователя
        upadate_user = User.objects.latest('id')
        upadate_group = Group.objects.get(name=upadate_user.chief.name)  # Получаем id группы новой
        upadate_user.groups.clear()  # Очистка старых групп
        upadate_user.groups.add(upadate_group)  # Присвоение новой группы
        # Создание папок для нового пользователя
        folder_user = "media/user/" + str(upadate_user.pk)
        folder_user_images = "media/user/" + str(upadate_user.pk) + "/images/"
        folder_save_files = "media/user/" + str(upadate_user.pk) + "/files/"
        os.mkdir(folder_user)
        os.mkdir(folder_user_images)
        os.mkdir(folder_save_files)

        return str(self.success_url)  # success_url may be lazy


class Workers_Views(LoginRequiredMixin, ViewsPermissionsMixin, DataMixin, DetailView):
    '''Детальная информация о сотруднике.'''
    model = User
    template_name = 'workers/workers_views.html'
    slug_url_kwarg = 'workers_slug'
    context_object_name = 'workers'
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.workers_view'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Страница сотрудника')
        context = dict(list(context.items()) + list(project_menus.items()))
        '''Запросы для предоставления информации'''
        if self.request.user.has_perm('workers.basic_views') or self.request.user.has_perm(
                'workers.basic_views_superiors'):
            context['base_information'] = User_Basic_Information.objects.get(
                user__slug=self.kwargs.get(self.slug_url_kwarg))
        if self.request.user.has_perm('workers.closed_views') or self.request.user.has_perm(
                'workers.closed_views_superiors'):
            context['closed_information'] = User_Closed_Information.objects.get(
                user__slug=self.kwargs.get(self.slug_url_kwarg))
        '''Запросы для предоставления прав доступа'''
        own = self.get_object().subdivision == self.request.user.subdivision and self.get_object().department == self.request.user.department
        supervisor_right_image = own and self.request.user.has_perm('workers.workers_change_image_superiors')
        supervisor_right_contact = own and self.request.user.has_perm('workers.workers_change_contact_superiors')
        # Пользователь
        base_righ_image = self.get_object() == self.request.user and self.request.user.has_perm(
            'workers.workers_change_image')
        base_righ_contact = self.get_object() == self.request.user and self.request.user.has_perm(
            'workers.workers_change_contact')

        context['right_edit_photo'] = supervisor_right_image or base_righ_image
        context['right_edit_contact'] = supervisor_right_contact or base_righ_contact

        return context


class Workers_Image(LoginRequiredMixin, ViewsPermissionsMixin, DataMixin, UpdateView):
    '''Добавление авотарок на сайт'''
    model = User
    template_name = 'workers/workers_images.html'
    form_class = Workers_Form_Upload_Images
    login_url = 'login'
    permission_required = ('workers.workers_change_image', 'workers.workers_change_image_superiors')
    permission_user = 'workers.workers_change_image'
    permission_user_superiors = 'workers.workers_change_image_superiors'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        form_check = Workers_Form_Upload_Images(request.POST, request.FILES)
        if form.is_valid() and len(form_check.files.dict()):
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # Управление по slug
    def get_object(self, queryset=None):
        instance = User.objects.get(slug=self.kwargs.get('workers_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Настройки. Загрузка аватарки.')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['workers'] = User.objects.get(slug=self.kwargs.get('workers_slug'))
        return context

    def get_success_url(self):
        messages.success(self.request, "Данные сохранены успешно")
        return reverse('workers_image', kwargs={'workers_slug': self.kwargs['workers_slug']})


class Workers_Change_Password(LoginRequiredMixin, DataMixin, PasswordChangeView):
    '''Изменить только сам сотрудник'''
    template_name = 'workers/workers_password_change.html'
    form_class = Workers_Form_PasswordChange
    login_url = 'login'
    redirect_field_name = ''

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Изменения пароля')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context

    def form_valid(self, form):
        self.object = form.save()

        return HttpResponseRedirect('')


class Workers_Update_Password(LoginRequiredMixin, ViewsPermissionsMixin, DataMixin, UpdateView):
    '''Изменить только по правам'''
    model = User
    template_name = 'workers/workers_password_update.html'
    form_class = Workers_Form_UpdatePassword
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.workers_update_password_superiors'

    # Управление по slug
    def get_object(self, queryset=None):
        instance = User.objects.get(slug=self.kwargs.get('workers_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Сброс пароля')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['workers'] = User.objects.get(slug=self.kwargs.get('workers_slug'))
        return context

    def get_success_url(self):
        if 'workers_slug' in self.kwargs:
            slug = self.kwargs['workers_slug']
        return reverse('workers_update_password', kwargs={'workers_slug': slug})

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, 'Данные сохранены успешно')
        return HttpResponseRedirect(self.get_success_url())


class Workers_Change(LoginRequiredMixin, ViewsPermissionsMixin, DataMixin, UpdateView):
    model = User
    template_name = 'workers/workers_update.html'
    form_class = Workers_Form_Update
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.workers_change_superiors'

    # Управление по slug
    def get_object(self, queryset=None):
        instance = User.objects.get(slug=self.kwargs.get('workers_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Workers_Change, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Обновить пользователя')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['workers'] = User.objects.get(slug=self.kwargs.get('workers_slug'))
        return context

    def form_valid(self, form):
        # Проверка на изменение ФИО
        old_name = User.objects.get(slug=self.kwargs.get('workers_slug', ''))
        if old_name.name != form.save().name or old_name.surname != form.save().surname or old_name.patronymic != form.save().patronymic:
            slug_name = form.save().surname + " " + form.save().name + " " + form.save().patronymic
            form.save().slug = slugify(translit(slug_name, 'ru', reversed=True))
            self.kwargs['workers_slug'] = form.save().slug
            self.object = form.save()
            # Переместить папку
            try:
                shutil.move("media/user/" + old_name.slug + "/files/",
                            "media/user/" + self.kwargs['workers_slug'] + "/files/")
                shutil.move("media/user/" + old_name.slug + "/certificate/",
                            "media/user/" + self.kwargs['workers_slug'] + "/certificate/")
            except:
                pass
            # Изменение путей в базе закрытая информация
            # Изменение путей в сертификатах

        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        # Обновление ифнормации о правах
        # Получить все группы пользователя  upadate_user.groups.all()
        upadate_user = User.objects.get(slug=self.kwargs.get('workers_slug', ''))  # Получаем пользователя
        upadate_group = Group.objects.get(name=upadate_user.chief.name)  # Получаем id группы новой
        upadate_user.groups.clear()  # Очистка старых групп
        upadate_user.groups.add(upadate_group)  # Присвоение новой группы

        messages.success(self.request, "Данные сохранены успешно")
        return reverse('workers_update', kwargs={'workers_slug': self.kwargs['workers_slug']})


class Workers_Basic_Change(LoginRequiredMixin, ViewsPermissionsMixin, DataMixin, UpdateView):
    model = User_Basic_Information
    template_name = 'workers/workers_update.html'

    form_class = Workers_Form_Update_Basic
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.basic_change_superiors'

    # Управление по slug
    def get_object(self, queryset=None):
        instance = User_Basic_Information.objects.get(user__slug=self.kwargs.get('workers_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Workers_Basic_Change, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Обновить пользователя')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['workers'] = User.objects.get(slug=self.kwargs.get('workers_slug'))
        return context

    def get_success_url(self):
        messages.success(self.request, "Данные сохранены успешно")
        return reverse('workers_basic_update', kwargs={'workers_slug': self.kwargs['workers_slug']})


class Workers_Closed_Change(LoginRequiredMixin, ViewsPermissionsMixin, DataMixin, UpdateView):
    model = User_Closed_Information
    template_name = 'workers/workers_update.html'
    form_class = Workers_Form_Update_Closed
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.closed_change_superiors'

    # Управление по slug
    def get_object(self, queryset=None):
        instance = User_Closed_Information.objects.get(user__slug=self.kwargs.get('workers_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Workers_Closed_Change, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Обновить пользователя')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['workers'] = User.objects.get(slug=self.kwargs.get('workers_slug'))
        return context

    def get_success_url(self):
        messages.success(self.request, "Данные сохранены успешно")
        return reverse('workers_closed_update', kwargs={'workers_slug': self.kwargs['workers_slug']})


class Workers_Passport(LoginRequiredMixin, ViewsPermissionsMixin, DataMixin, UpdateView):
    model = User_Closed_Information
    template_name = 'workers/workers_doc_passport.html'
    form_class = Workers_Form_Upload_Passport
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.user_basic_add_passport_superiors'

    # Управление по slug
    def get_object(self, queryset=None):
        instance = User_Closed_Information.objects.get(user__slug=self.kwargs.get('workers_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Workers_Passport, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Скан паспорта')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['closed_information'] = User_Closed_Information.objects.get(user__slug=self.kwargs.get('workers_slug'))

        return context

    def get_success_url(self):
        messages.success(self.request, "Данные сохранены успешно")
        return reverse('workers_passport', kwargs={'workers_slug': self.kwargs['workers_slug']})


class Workers_Snils(LoginRequiredMixin, ViewsPermissionsMixin, DataMixin, UpdateView):
    model = User_Closed_Information
    template_name = 'workers/workers_doc_snils.html'
    form_class = Workers_Form_Upload_Snils
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.user_basic_add_snils_superiors'

    # Управление по slug
    def get_object(self, queryset=None):
        instance = User_Closed_Information.objects.get(user__slug=self.kwargs.get('workers_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Workers_Snils, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Скан СНИЛС')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['closed_information'] = User_Closed_Information.objects.get(user__slug=self.kwargs.get('workers_slug'))

        return context

    def get_success_url(self):
        messages.success(self.request, "Данные сохранены успешно")
        return reverse('workers_snils', kwargs={'workers_slug': self.kwargs['workers_slug']})


class Workers_Inn(LoginRequiredMixin, ViewsPermissionsMixin, DataMixin, UpdateView):
    model = User_Closed_Information
    template_name = 'workers/workers_doc_inn.html'
    form_class = Workers_Form_Upload_Inn
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.user_basic_add_inn_superiors'

    def get_object(self, queryset=None):
        instance = User_Closed_Information.objects.get(user__slug=self.kwargs.get('workers_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Workers_Inn, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Скан ИНН')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['closed_information'] = User_Closed_Information.objects.get(user__slug=self.kwargs.get('workers_slug'))

        return context

    def get_success_url(self):
        messages.success(self.request, "Данные сохранены успешно")
        return reverse('workers_inn', kwargs={'workers_slug': self.kwargs['workers_slug']})


class Workers_Archive(LoginRequiredMixin, ViewsPermissionsMixin, DataMixin, UpdateView):
    model = User_Closed_Information
    template_name = 'workers/workers_doc_archive.html'
    form_class = Workers_Form_Upload_Archive
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.user_basic_add_archive_superiors'

    # Управление по slug
    def get_object(self, queryset=None):
        instance = User_Closed_Information.objects.get(user__slug=self.kwargs.get('workers_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Workers_Archive, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Архив документов при трудоустройстве')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['closed_information'] = User_Closed_Information.objects.get(user__slug=self.kwargs.get('workers_slug'))
        return context

    def get_success_url(self):
        messages.success(self.request, "Данные сохранены успешно")
        return reverse('workers_archive', kwargs={'workers_slug': self.kwargs['workers_slug']})


class Workers_Signature(LoginRequiredMixin, ViewsPermissionsMixin, DataMixin, UpdateView):
    """Загрузка подписи"""
    model = User_Closed_Information
    template_name = 'workers/workers_signature.html'
    form_class = Workers_Form_Upload_Signature
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.user_basic_add_signature_superiors'

    # Управление по slug
    def get_object(self, queryset=None):
        instance = User_Closed_Information.objects.get(user__slug=self.kwargs.get('workers_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Образец подписи')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['closed_information'] = User_Closed_Information.objects.get(user__slug=self.kwargs.get('workers_slug'))
        return context

    def get_success_url(self):
        messages.success(self.request, "Данные сохранены успешно")
        return reverse('workers_signature', kwargs={'workers_slug': self.kwargs['workers_slug']})


class Workers_Edit_Сontacts(LoginRequiredMixin, ViewsPermissionsMixin, DataMixin, UpdateView):
    template_name = 'workers/workers_contacts.html'
    model = User
    form_class = Workers_Form_Edit_Сontacts_User

    model_basic_ifnormation = User_Basic_Information
    form_class_basic_information = Workers_Form_Edit_Сontacts_User_Basic_Information

    login_url = 'login'
    redirect_field_name = ''
    permission_required = ('workers.workers_change_contact', 'workers.workers_change_contact_superiors')
    permission_user = 'workers.workers_change_contact'
    permission_user_superiors = 'workers.workers_change_contact_superiors'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        # Базовая информация о сотрудниках
        basic_information_obj = getattr(self.object, 'user_basic_information', None)
        basic_information_form = self.form_class_basic_information(request.POST, prefix='basic_information',
                                                                   instance=basic_information_obj)
        if form.is_valid() and basic_information_form.is_valid():
            return self.form_valid(form, basic_information_form)
        else:
            return self.form_invalid(form, basic_information_form)

    # Управление по slug
    def get_object(self, queryset=None):
        instance = User.objects.get(slug=self.kwargs.get('workers_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Workers_Edit_Сontacts, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Обновить пользователя')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['workers'] = User.objects.get(slug=self.kwargs.get('workers_slug'))
        # Вторая форма
        if self.request.method == 'POST':
            basic_information_form = self.form_class_basic_information(self.request.POST, prefix='basic_information')
        else:
            basic_information_model = self.model_basic_ifnormation.objects.get(
                user__slug=self.kwargs.get('workers_slug', ''))
            basic_information_form = self.form_class_basic_information(instance=basic_information_model,
                                                                       prefix='basic_information')
        context['basic_informations'] = basic_information_form
        return context

    def get_success_url(self):
        messages.success(self.request, "Данные сохранены успешно")
        return reverse('contacts_edit', kwargs={'workers_slug': self.kwargs['workers_slug']})

    def form_valid(self, form, basic_information_form):
        # форма User
        obj = form.save(commit=False)
        obj.save()
        # форма User_Basic_Information
        basic_information_obj = basic_information_form.save(commit=False)
        basic_information_obj.task = obj
        basic_information_obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, basic_information_form):
        return self.render_to_response(self.get_context_data(form=form))
