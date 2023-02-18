import datetime
import os

from django.contrib import messages
from django.db.models import QuerySet, Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template.defaultfilters import addslashes
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from projects.forms import Project_Control, Organizations_Objects_Control, Development_Task_Control, \
    Position_Objects_Control, Cabinet_Control, Development_Task_Filter, Development_Task_Edit_Date, \
    Development_Task_Edit_Develop, Development_Task_Edit_Status, Position_Objects_Filter, Position_Objects_Edit_Checker, \
    Position_Objects_Upload_Protocol
from projects.models import Project, Organizations_Objects, Development_Task, Position_Objects, Сabinet
from workers.utils import DataMixin


class Organizations_Objects_View(DataMixin, ListView):
    '''Название объекта. Просмотр'''
    model = Organizations_Objects
    template_name = 'projects/objects_view.html'
    context_object_name = 'organizations_objects'

    def get(self, *args, **kwargs):
        if self.request.user.has_perm('workers.delete_subdivision'):
            query = self.request.GET.get('remove')
            if query != None:
                try:
                    remove = Organizations_Objects.objects.get(slug=query)
                    remove.delete()
                except:
                    pass
        organizations_objects = Organizations_Objects.objects.all()  # Запрос
        context = {'organizations_objects': organizations_objects, }
        project_menus = self.get_user_context(title='Тип документов для разработки')
        context = dict(list(context.items()) + list(project_menus.items()))
        return render(self.request, self.template_name, context)


class Organizations_Objects_Add(DataMixin, CreateView):
    """Название объекта. Создать"""
    model = Organizations_Objects
    template_name = 'projects/project_control.html'
    form_class = Organizations_Objects_Control

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Довить документ')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context

    def get_success_url(self):
        """Добавление папок"""
        organizations_objects = Organizations_Objects.objects.latest('id')
        folder = 'media/projects/{0}/{1}/'.format(str(organizations_objects.organization.pk),
                                                  str(organizations_objects.pk))
        os.mkdir(folder)
        return reverse('organizations_objects')


class Organizations_Objects_Edit(DataMixin, UpdateView):
    """Название объекта. Обновить"""
    model = Organizations_Objects
    template_name = 'projects/project_control.html'
    form_class = Organizations_Objects_Control
    success_url = reverse_lazy('organizations_objects')

    def get_object(self, queryset=None):
        instance = Organizations_Objects.objects.get(slug=self.kwargs.get('organizations_objects_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Organizations_Objects_Edit, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Довить документ')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['organizations_objects_slug'] = Organizations_Objects.objects.get(
            slug=self.kwargs.get('organizations_objects_slug'))
        return context


class Projects_View(DataMixin, ListView):
    '''Проект на разработку. Просмотр'''
    model = Project
    template_name = 'projects/project_view.html'
    context_object_name = 'projects'

    def get(self, *args, **kwargs):
        if self.request.user.has_perm('workers.delete_subdivision'):
            query = self.request.GET.get('remove')
            if query != None:
                try:
                    remove = Project.objects.get(slug=query)
                    remove.delete()
                except:
                    pass
        projects = Project.objects.all()  # Запрос
        context = {'projects': projects, }
        project_menus = self.get_user_context(title='Тип документов для разработки')
        context = dict(list(context.items()) + list(project_menus.items()))
        return render(self.request, self.template_name, context)


class Projects_Add(DataMixin, CreateView):
    model = Project
    template_name = 'projects/project_control.html'
    form_class = Project_Control
    success_url = reverse_lazy('projects')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Довить документ')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Projects_Edit(DataMixin, UpdateView):
    model = Project
    template_name = 'projects/project_control.html'
    form_class = Project_Control
    success_url = reverse_lazy('projects')

    def get_object(self, queryset=None):
        instance = Project.objects.get(slug=self.kwargs.get('project_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Projects_Edit, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Довить документ')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['project_slug'] = Project.objects.get(slug=self.kwargs.get('project_slug'))
        return context


class Development_Task_View(DataMixin, ListView):
    """Задание на разработку. Просмотр"""
    model = Development_Task
    template_name = 'projects/development_task_view.html'
    context_object_name = 'development_tasks'

    def get_queryset(self):
        if self.request.GET:
            filters = Q()  # создаем первый объект Q, что бы складывать с ним другие
            """Отметка на дату"""
            if self.request.GET.get('year') and str(self.request.GET.get('year')) != 'allTime':
                year = int(datetime.datetime.now().year)
                try:
                    year = int(self.request.GET.get('year'))
                except Exception as e:
                    pass
                filters &= Q(**{f'{"date_issue__year"}': year})
            """Отметка проекта"""
            if self.request.GET.get('status') and str(self.request.GET.get('status')) != 'all':
                if self.request.GET.get('status') == 'done':
                    filters &= Q(**{f'{"status"}': "Done"})
                else:
                    filters &= ~Q(**{f'{"status"}': "Done"})
            """Отметка на Управление """
            if self.request.GET.get('subdivision') and str(self.request.GET.get('subdivision')) != 'own':
                filters &= Q(**{f'{"subdivision__slug"}': addslashes(str(self.request.GET.get('subdivision')))})
            else:
                if self.request.user.subdivision:
                    filters &= Q(**{f'{"subdivision__slug"}': self.request.user.subdivision.slug})
            """Отметка на отдел"""
            if self.request.GET.get('department') and str(self.request.GET.get('department')) != 'own':
                filters &= Q(**{f'{"department__slug"}': addslashes(str(self.request.GET.get('department')))})
            else:
                if self.request.user.department:
                    filters &= Q(**{f'{"department__slug"}': self.request.user.department.slug})
            if len(filters) > 0:
                return Development_Task.objects.filter(filters)

        # Если фильтра нет то выводим стандартный вывод информации
        if self.request.user.subdivision and self.request.user.department:
            return Development_Task.objects.filter(Q(subdivision=self.request.user.subdivision),
                                                   Q(department=self.request.user.department)
                                                   ).order_by('-date_issue')
        if self.request.user.subdivision and not self.request.user.department:
            return Development_Task.objects.filter(Q(subdivision=self.request.user.subdivision),
                                                   ~Q(status='Done')).order_by('-date_issue')

        return Development_Task.objects.all().order_by('-date_issue')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Задание на разработку')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['form_filter'] = Development_Task_Filter(self.request.GET, initial={'user': self.request.user})
        return context


class Development_Task_Add(DataMixin, CreateView):
    '''Задание на разработку. Просмотр'''
    model = Development_Task
    template_name = 'projects/development_task_add.html'
    form_class = Development_Task_Control
    success_url = reverse_lazy('development_task')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Добавить задание на разработку')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context

    def form_valid(self, form):
        # Объект берется из задания
        form.save().organizations_objects = form.save().project.organizations_objects
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class Development_Task_Edit(DataMixin, UpdateView):
    """Задание на разработку. Редактировать задание"""
    model = Development_Task
    template_name = 'projects/development_task_edit.html'
    form_class = Development_Task_Control

    def get_object(self, queryset=None):
        instance = Development_Task.objects.get(slug=self.kwargs.get('development_task_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Development_Task_Edit, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Редактировать задание на разработку')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['slug'] = self.kwargs.get('development_task_slug', '')
        return context

    def get_success_url(self):
        return reverse('development_task_detailed',
                       kwargs={'development_task_slug': self.kwargs['development_task_slug']})


class Development_Task_Edit_Date(DataMixin, UpdateView):
    """Задание на разработку. Редактировать задание"""
    model = Development_Task
    template_name = 'projects/development_task_edit_date.html'
    form_class = Development_Task_Edit_Date

    def get_object(self, queryset=None):
        instance = Development_Task.objects.get(slug=self.kwargs.get('development_task_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Development_Task_Edit_Date, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Редактировать задание на разработку')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['slug'] = self.kwargs.get('development_task_slug', '')
        return context

    def get_success_url(self):
        return reverse('development_task_detailed',
                       kwargs={'development_task_slug': self.kwargs['development_task_slug']})


class Development_Task_Edit_Status(DataMixin, UpdateView):
    """Задание на разработку. Редактировать задание"""
    model = Development_Task
    template_name = 'projects/development_task_edit_status.html'
    form_class = Development_Task_Edit_Status

    def get_object(self, queryset=None):
        instance = Development_Task.objects.get(slug=self.kwargs.get('development_task_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Development_Task_Edit_Status, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Редактировать задание на разработку')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['slug'] = self.kwargs.get('development_task_slug', '')
        return context

    def get_success_url(self):
        return reverse('development_task_detailed',
                       kwargs={'development_task_slug': self.kwargs['development_task_slug']})


class Development_Task_Edit_Develop(DataMixin, UpdateView):
    """Задание на разработку. Редактировать задание"""
    model = Development_Task
    template_name = 'projects/development_task_edit_develop.html'
    form_class = Development_Task_Edit_Develop

    def get_object(self, queryset=None):
        instance = Development_Task.objects.get(slug=self.kwargs.get('development_task_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Development_Task_Edit_Develop, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Редактировать задание на разработку')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['slug'] = self.kwargs.get('development_task_slug', '')
        return context

    def get_success_url(self):
        return reverse('development_task_detailed',
                       kwargs={'development_task_slug': self.kwargs['development_task_slug']})


class Development_Task_DetailView(DataMixin, DetailView):
    '''Задание на разработку. Детальный просмот проекта'''
    model = Development_Task
    template_name = 'projects/development_task_detailview.html'
    context_object_name = 'development_task'

    def get_object(self, queryset=None):
        instance = Development_Task.objects.get(slug=self.kwargs.get('development_task_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Development_Task_DetailView, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Задание на разработку')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Development_Task_Delete(DataMixin, DeleteView):
    model = Development_Task
    template_name = 'projects/development_task_delete.html'
    success_url = reverse_lazy('development_task')

    def get_object(self, queryset=None):
        instance = Development_Task.objects.get(slug=self.kwargs.get('development_task_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Development_Task_Delete, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Удаление задания на разработку')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Position_Objects_View(DataMixin, ListView):
    """Позиция на объекте"""
    model = Position_Objects
    template_name = 'projects/objects_position_view.html'
    context_object_name = 'position_objects'

    def get_queryset(self):
        """Возможные запросы. Требуется подумать и добавить фильтры по отдела и управлениям"""
        return Position_Objects.objects.filter(development_task__subdivision=self.request.user.subdivision,
                                               development_task__department=self.request.user.department).order_by(
            '-date_issue')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Позиция на объекте')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['form_filter'] = Position_Objects_Filter(self.request.GET, initial={'user': self.request.user})
        return context


class Position_Objects_Add(DataMixin, CreateView):
    """Позиция на объекте. Просмотр"""
    model = Position_Objects
    template_name = 'projects/objects_position_control.html'
    form_class = Position_Objects_Control
    success_url = reverse_lazy('position_objects')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Довить новую позицию')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context

    def form_valid(self, form):
        # Объект берется из задания
        form.save().organizations_objects = form.save().development_task.organizations_objects
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        position_objects = Position_Objects.objects.latest('id')

        folder = 'media/projects/{0}/{1}/{2}'.format(
            str(position_objects.organizations_objects.organization.pk),
            str(position_objects.organizations_objects.pk),
            str(position_objects.pk),
        )
        os.mkdir(folder)
        return reverse('position_objects')


class Position_Objects_Edit(DataMixin, UpdateView):
    """Задание на разработку. Просмотр"""
    model = Position_Objects
    template_name = 'projects/objects_position_control.html'
    form_class = Position_Objects_Control
    success_url = reverse_lazy('position_objects')

    def get_object(self, queryset=None):
        instance = Position_Objects.objects.get(slug=self.kwargs.get('position_objects_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Position_Objects_Edit, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Довить документ')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['position_objects_slug'] = Position_Objects.objects.get(slug=self.kwargs.get('position_objects_slug'))
        return context


class Position_Objects_DetailView(DataMixin, DetailView):
    """Задание на разработку. Детальный просмот проекта"""
    model = Position_Objects
    template_name = 'projects/objects_position_detailview.html'
    context_object_name = 'position_objects'

    def get_object(self, queryset=None):
        instance = Position_Objects.objects.get(slug=self.kwargs.get('position_objects_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Position_Objects_DetailView, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Позиция объекта')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Position_Objects_Delete(DataMixin, DeleteView):
    model = Position_Objects
    template_name = 'projects/objects_position_delete.html'
    success_url = reverse_lazy('position_objects')

    def get_object(self, queryset=None):
        instance = Position_Objects.objects.get(slug=self.kwargs.get('position_objects_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Position_Objects_Delete, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Удаление позиции на объекте')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Position_Objects_Edit_Checker(DataMixin, UpdateView):
    """Задание на разработку. Назначение проверяющих."""
    model = Position_Objects
    template_name = 'projects/objects_position_edit_checker.html'
    form_class = Position_Objects_Edit_Checker

    def get_object(self, queryset=None):
        instance = Position_Objects.objects.get(slug=self.kwargs.get('position_objects_slug', ''))
        return instance

    def get_success_url(self):
        messages.success(self.request, "Проверяющие назначены")

        return reverse('position_objects_edit_checker',
                       kwargs={'position_objects_slug': self.kwargs['position_objects_slug']})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Position_Objects_Edit_Checker, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Довить документ')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['position_objects_slug'] = Position_Objects.objects.get(slug=self.kwargs.get('position_objects_slug'))
        return context


class Position_Objects_Upload_Protocol(DataMixin, UpdateView):
    model = Position_Objects
    template_name = 'projects/objects_position_edit_protocol.html'
    form_class = Position_Objects_Upload_Protocol

    def get_object(self, queryset=None):
        instance = Position_Objects.objects.get(slug=self.kwargs.get('position_objects_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Position_Objects_Upload_Protocol, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Добавить протокол проверки')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['position_objects'] = Position_Objects.objects.get(slug=self.kwargs.get('position_objects_slug'))
        return context

    def get_success_url(self):
        messages.success(self.request, "Протокол успешно добавлен")
        return reverse('position_objects_upload_protokol',
                       kwargs={'position_objects_slug': self.kwargs['position_objects_slug']})


class Сabinet_View(DataMixin, ListView):
    '''Задание на разработку. Просмотр'''
    model = Сabinet
    template_name = 'projects/cabinet_view.html'
    context_object_name = 'cabinets'

    def get(self, *args, **kwargs):
        if self.request.user.has_perm('workers.delete_subdivision'):
            query = self.request.GET.get('remove')
            if query != None:
                try:
                    remove = Сabinet.objects.get(slug=query)
                    remove.delete()
                except:
                    pass
        cabinets = Сabinet.objects.all()  # Запрос
        context = {'cabinets': cabinets, }
        project_menus = self.get_user_context(title='Шкафы на позициях')
        context = dict(list(context.items()) + list(project_menus.items()))
        return render(self.request, self.template_name, context)


class Сabinet_Add(DataMixin, CreateView):
    """Задание на разработку. Просмотр"""
    model = Сabinet
    template_name = 'projects/cabinet_control.html'
    form_class = Cabinet_Control
    success_url = reverse_lazy('cabinet')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Добавиь шкаф')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Сabinet_Edit(DataMixin, UpdateView):
    '''Задание на разработку. Просмотр'''
    model = Сabinet
    template_name = 'projects/cabinet_control.html'

    form_class = Cabinet_Control
    success_url = reverse_lazy('cabinet')

    def get_object(self, queryset=None):
        instance = Сabinet.objects.get(slug=self.kwargs.get('cabinet_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Position_Objects_Edit, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Довить документ')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['cabinet_slug'] = Сabinet.objects.get(slug=self.kwargs.get('cabinet_slug'))
        return context
