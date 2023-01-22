from django.core.checks import messages
from django.http import HttpResponse

# Create your views here.
from django.urls import reverse

from django.views.generic import ListView, CreateView, DetailView, UpdateView

from projects.forms import Development_Task_Control, Organization_Control
from projects.models import Development_Task, Organization, Organizations_Objects
from workers.utils import DataMixin


class Development_Task_View(DataMixin, ListView):
    '''Показать все задания'''
    model = Development_Task
    template_name = 'projects/development_task_view.html'
    context_object_name = 'developments_tasks'

    def get_queryset(self):
        print(self.request.user.subdivision)
        print('-------lllllllllllll------')
        print(self.request.user.department)
        return Development_Task.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Задание на ППО.')

        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Development_Task_Add(DataMixin, CreateView):
    '''Урпавление. Добавление. '''
    model = Development_Task
    template_name = 'projects/development_task_add.html'
    form_class = Development_Task_Control
    success_url = '/project/development_task/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Задание на ППО.')

        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Development_Task_Detail_View(DataMixin, DetailView):
    '''Урпавление. Просмотр. '''
    model = Development_Task
    template_name = 'projects/development_task_detail_view.html'
    slug_url_kwarg = 'development_task_slug'
    context_object_name = 'development_task'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Задание на ППО.')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Development_Task_Edit(DataMixin, UpdateView):
    model = Development_Task
    template_name = 'projects/development_task_edit.html'
    form_class = Development_Task_Control

    # Управление по slug
    def get_object(self, queryset=None):
        instance = Development_Task.objects.get(slug=self.kwargs.get('development_task_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Development_Task_Edit, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Обновить задание на рарзработку')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['development_task'] = Development_Task.objects.get(slug=self.kwargs.get('development_task_slug'))
        return context

    def get_success_url(self):
        messages.success(self.request, "Данные сохранены успешно")
        return reverse('development_task_edit', kwargs={'development_task_slug': self.kwargs['development_task_slug']})


############
####
############
class Organization_View(DataMixin, ListView):
    model = Organization
    template_name = 'projects/organization_view.html'
    context_object_name = 'organizations'

    def get_queryset(self):
        return Organization.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Фирмы.')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Organization_Add(DataMixin, CreateView):
    model = Organization
    template_name = 'projects/organization_add.html'
    form_class = Organization_Control
    success_url = '/project/organization/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Фирмы')

        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Organization_Detail_View(DataMixin, DetailView):
    model = Organization
    template_name = 'projects/organization_detail_view.html'
    slug_url_kwarg = 'organization_slug'
    context_object_name = 'organization'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Фирмы.')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Organization_Edit(DataMixin, UpdateView):
    model = Organization
    template_name = 'projects/organization_edit.html'
    form_class = Organization_Control

    # Управление по slug
    def get_object(self, queryset=None):
        instance = Organization.objects.get(slug=self.kwargs.get('organization_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Organization_Edit, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Обновить информацию о фирме')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['development_task'] = Organization.objects.get(slug=self.kwargs.get('organization_slug'))
        return context


############
####
############

class Organizations_Objects_View(DataMixin, ListView):
    model = Organizations_Objects
    template_name = 'projects/organizations_objects_view.html'
    context_object_name = 'organizations_objects'

    def get_queryset(self):
        return Organizations_Objects.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Название объекта')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Organizations_Objects_Add(DataMixin, CreateView):
    model = Organization
    template_name = 'projects/organization_add.html'
    form_class = Organization_Control
    success_url = '/project/organization/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Фирмы')

        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Organizations_Objects_Detail_View(DataMixin, DetailView):
    model = Organization
    template_name = 'projects/organization_detail_view.html'
    slug_url_kwarg = 'organization_slug'
    context_object_name = 'organization'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Фирмы.')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Organizations_Objects_Edit(DataMixin, UpdateView):
    model = Organization
    template_name = 'projects/organization_edit.html'
    form_class = Organization_Control

    # Управление по slug
    def get_object(self, queryset=None):
        instance = Organization.objects.get(slug=self.kwargs.get('organization_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Organization_Edit, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Обновить информацию о фирме')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['development_task'] = Organization.objects.get(slug=self.kwargs.get('organization_slug'))
        return context


def infossss1(request):
    return HttpResponse("XER1")


# Create your views here.
def infossss2(request):
    return HttpResponse("xer2")
