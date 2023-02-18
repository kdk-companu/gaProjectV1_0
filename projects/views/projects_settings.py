import os

from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from projects.forms import Organization_Direction_Control, Organization_Control, Type_Document_Control
from projects.models import Organization_Direction, Organization, Type_Document
from workers.utils import DataMixin


class Organization_Direction_View(DataMixin, ListView):
    '''Направление деятельности организации. Просмотр.'''
    model = Organization_Direction
    template_name = 'projects/settings_organization_direction_view.html'

    def get(self, *args, **kwargs):
        if self.request.user.has_perm('workers.delete_subdivision'):
            query = self.request.GET.get('remove')
            if query != None:
                try:
                    remove = Organization_Direction.objects.get(slug=query)
                    remove.delete()
                except:
                    pass
        organizations_directions = Organization_Direction.objects.all()  # Запрос
        context = {'organizations_directions': organizations_directions, }
        project_menus = self.get_user_context(title='Направление дейтельности организации')
        context = dict(list(context.items()) + list(project_menus.items()))
        return render(self.request, self.template_name, context)


class Organization_Direction_Add(DataMixin, CreateView):
    '''Направление деятельности организации. Добавить.'''
    model = Organization_Direction
    template_name = 'projects/settings_organization_direction_control.html'
    form_class = Organization_Direction_Control
    success_url = reverse_lazy('organization_direction')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Направление дейтельности организации.')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Organization_Direction_Update(DataMixin, UpdateView):
    '''Направление деятельности организации. Изменить.'''
    model = Organization_Direction
    template_name = 'projects/settings_organization_direction_control.html'
    form_class = Organization_Direction_Control
    success_url = reverse_lazy('organization_direction')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Направление дейтельности организации.')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context

    def get_object(self, queryset=None):
        instance = Organization_Direction.objects.get(slug=self.kwargs.get('organization_direction_slug', ''))
        return instance


class Organization_View(DataMixin, ListView):
    model = Organization
    template_name = 'projects/organization_view.html'
    context_object_name = 'organizations'

    def get(self, *args, **kwargs):
        if self.request.user.has_perm('workers.delete_subdivision'):
            query = self.request.GET.get('remove')
            if query != None:
                try:
                    remove = Organization.objects.get(slug=query)
                    remove.delete()
                except:
                    pass
        organizations = Organization.objects.all()  # Запрос
        context = {'organizations': organizations, }
        project_menus = self.get_user_context(title='Организации')
        context = dict(list(context.items()) + list(project_menus.items()))
        return render(self.request, self.template_name, context)


class Organization_Add(DataMixin, CreateView):
    model = Organization
    template_name = 'projects/organization_control.html'
    form_class = Organization_Control

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Добавить организацию')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context

    def get_success_url(self):
        organization = Organization.objects.latest('id')
        folder = "media/projects/" + str(organization.pk)
        os.mkdir(folder)
        return reverse('organization')


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
    template_name = 'projects/organization_control.html'
    form_class = Organization_Control
    success_url = reverse_lazy('type_document')

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


class Type_Document_View(DataMixin, ListView):
    '''Типы докуменов разрабатываемых документов. Просмотр'''
    model = Type_Document
    template_name = 'projects/settings_type_document_view.html'
    context_object_name = 'type_documents'

    def get(self, *args, **kwargs):
        if self.request.user.has_perm('workers.delete_subdivision'):
            query = self.request.GET.get('remove')
            if query != None:
                try:
                    remove = Type_Document.objects.get(slug=query)
                    remove.delete()
                except:
                    pass
        type_documents = Type_Document.objects.all()  # Запрос
        context = {'type_documents': type_documents, }
        project_menus = self.get_user_context(title='Тип документов для разработки')
        context = dict(list(context.items()) + list(project_menus.items()))
        return render(self.request, self.template_name, context)


class Type_Document_Add(DataMixin, CreateView):
    model = Type_Document
    template_name = 'projects/settings_type_document_control.html'
    form_class = Type_Document_Control
    success_url = reverse_lazy('type_document')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Довить документ')
        context = dict(list(context.items()) + list(project_menus.items()))
        return context


class Type_Document_Edit(DataMixin, UpdateView):
    model = Type_Document
    template_name = 'projects/settings_type_document_control.html'
    form_class = Type_Document_Control
    success_url = reverse_lazy('type_document')

    def get_object(self, queryset=None):
        instance = Type_Document.objects.get(slug=self.kwargs.get('type_document_slug', ''))
        return instance

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Type_Document_Edit, self).get_context_data(**kwargs)
        project_menus = self.get_user_context(title='Довить документ')
        context = dict(list(context.items()) + list(project_menus.items()))
        context['type_document_slug'] = Type_Document.objects.get(slug=self.kwargs.get('type_document_slug'))
        return context
