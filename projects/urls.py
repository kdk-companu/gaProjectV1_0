from django.urls import path

from projects.views import Development_Task_View, Development_Task_Add, Development_Task_Detail_View, \
    Development_Task_Edit, Organization_View, Organization_Add, Organization_Detail_View, \
    Organization_Edit, Organizations_Objects_View
from projects.views import infossss1

urlpatterns = [
    path('project/development_task/', Development_Task_View.as_view(), name='development_task'),
    path('project/development_task/add/', Development_Task_Add.as_view(), name='development_task_add'),
    path('project/development_task/view/<slug:development_task_slug>/', Development_Task_Detail_View.as_view(), name='development_task_view'),
    path('project/development_task/edit/<slug:development_task_slug>/', Development_Task_Edit.as_view(), name='development_task_edit'),

    path('project/organization/', Organization_View.as_view(), name='organization'),
    path('project/organization/add/', Organization_Add.as_view(), name='organization_add'),
    path('project/organization/view/<slug:organization_slug>/', Organization_Detail_View.as_view(),
          name='organization_view'),
    path('project/organization/edit/<slug:organization_slug>/', Organization_Edit.as_view(),
         name='organization_edit'),
    path('project/organizations_objects/', Organizations_Objects_View.as_view(), name='organizations_objects'),
    path('xer/', infossss1, name='test_page'),
]