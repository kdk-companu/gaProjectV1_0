from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, ListView

from workers.forms import Subdivision_Form_Control, Department_Form_Control, Chief_Form_Control
from workers.mixin.rights_mixin import ViewsPermissionsMixin
from workers.models import Subdivision, Department, Chief
from workers.utils import DataMixin


def info1(request):
    return HttpResponse("Hello word")


# Create your views here.
def info2(request):
    return HttpResponse("Hello word")


class Subdivision_Update(LoginRequiredMixin,ViewsPermissionsMixin, DataMixin, UpdateView):
    '''Урпавление. Изменение '''
    model = Subdivision
    template_name = 'workers/development_task_add.html'
    form_class = Subdivision_Form_Control
    success_url = reverse_lazy('subdivision')
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.change_subdivision'

    # Управление по slug
    def get_object(self, queryset=None):
        instance = Subdivision.objects.get(slug=self.kwargs.get('subdivision_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Редактирование Управления/Подразделения')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Subdivision_Add(LoginRequiredMixin,ViewsPermissionsMixin, DataMixin, CreateView):
    '''Урпавление. Добавление. '''
    model = Subdivision
    template_name = 'workers/settings_subdivision_control.html'
    success_url = reverse_lazy('subdivision')
    form_class = Subdivision_Form_Control
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.add_subdivision'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Добавление Управления/Подразделения')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Subdivision_View(LoginRequiredMixin,ViewsPermissionsMixin, DataMixin, ListView):
    '''Урпавление. Визуализация.'''
    model = Subdivision
    template_name = 'workers/settings_subdivision.html'
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.view_subdivision'

    def get(self, *args, **kwargs):
        if self.request.user.has_perm('workers.delete_subdivision'):
            query = self.request.GET.get('remove')
            if query != None:
                try:
                    remove = Subdivision.objects.get(slug=query)
                    remove.delete()
                except:
                    pass

        subdivisions = Subdivision.objects.all()  # Запрос
        context = {'subdivisions': subdivisions, }

        project_menus = self.get_user_context(title='Управления/Подразделения')
        context = dict(list(context.items()) + list(project_menus.items()))

        return render(self.request, self.template_name, context)


class Department_Update(LoginRequiredMixin,ViewsPermissionsMixin, DataMixin, UpdateView):
    '''Департамент. Изменение'''
    model = Department
    template_name = 'workers/settings_department_control.html'
    form_class = Department_Form_Control
    success_url = reverse_lazy('department')
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.change_department'

    # Управление по slug
    def get_object(self, queryset=None):
        instance = Department.objects.get(slug=self.kwargs.get('department_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Редактирование отдела')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Department_Add(LoginRequiredMixin,ViewsPermissionsMixin, DataMixin, CreateView):
    '''Департамент. Добавление'''
    model = Department
    template_name = 'workers/settings_department_control.html'
    success_url = reverse_lazy('department')
    form_class = Department_Form_Control
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.add_department'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Добавление отдела')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Department_View(LoginRequiredMixin,ViewsPermissionsMixin, DataMixin, ListView):
    '''Департамент. Добавление'''
    model = Department
    template_name = 'workers/settings_department.html'
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.view_department'

    def get(self, *args, **kwargs):
        if self.request.user.has_perm('workers.delete_department'):
            query = self.request.GET.get('remove')
            if query != None:
                try:
                    remove = Department.objects.get(slug=query)
                    remove.delete()
                except:
                    pass
        departments = Department.objects.all()  # Запрос
        context = {'departments': departments, }

        project_menus = self.get_user_context(title='Отдел')
        context = dict(list(context.items()) + list(project_menus.items()))

        return render(self.request, self.template_name, context)


class Chief_Update(LoginRequiredMixin,ViewsPermissionsMixin, DataMixin, UpdateView):
    '''Отдел. Изменение'''
    model = Chief
    template_name = 'workers/settings_chief_control.html'
    form_class = Chief_Form_Control
    login_url = 'login'
    redirect_field_name = ''
    success_url = reverse_lazy('chief')
    permission_required = 'workers.change_chief'

    # Управление по slug
    def get_object(self, queryset=None):
        instance = Chief.objects.get(slug=self.kwargs.get('chief_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Редактирование должности')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Chief_Add(LoginRequiredMixin,ViewsPermissionsMixin, DataMixin, CreateView):
    '''Отдел. Добавление'''
    model = Chief
    template_name = 'workers/settings_chief_control.html'
    success_url = reverse_lazy('chief')
    form_class = Chief_Form_Control
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.add_chief'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Добавление должности')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Chief_View(LoginRequiredMixin,ViewsPermissionsMixin, DataMixin, ListView):
    '''Отдел. Изменение'''
    model = Chief
    template_name = 'workers/settings_chief.html'
    login_url = 'login'
    redirect_field_name = ''
    permission_required = 'workers.view_chief'

    def get(self, *args, **kwargs):
        if self.request.user.has_perm('workers.delete_chief'):
            query = self.request.GET.get('remove')
            if query != None:
                try:
                    print(query)
                    remove = Chief.objects.get(slug=query)
                    remove.delete()
                except:
                    pass

        chiefs = Chief.objects.all().order_by('-rights')# Запрос
        print(chiefs)
        context = {'chiefs': chiefs, }

        project_menus = self.get_user_context(title='Должность')
        context = dict(list(context.items()) + list(project_menus.items()))

        return render(self.request, self.template_name, context)
