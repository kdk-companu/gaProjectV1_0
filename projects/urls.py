from django.urls import path

from projects.views import Projects_View, Projects_Add, Projects_Edit, Organizations_Objects_View, \
    Organizations_Objects_Add, Organizations_Objects_Edit, Development_Task_View, Development_Task_Add, \
    Development_Task_Edit, Position_Objects_Edit, Position_Objects_Add, Position_Objects_View, Сabinet_Edit, \
    Сabinet_Add, Сabinet_View, Development_Task_Delete, Development_Task_DetailView, Development_Task_Edit_Date, \
    Development_Task_Edit_Develop, Development_Task_Edit_Status, Position_Objects_DetailView, Position_Objects_Delete, \
    Position_Objects_Edit_Checker, Position_Objects_Upload_Protocol
from projects.views.projects_settings import Organization_Direction_View, Organization_Direction_Add, \
    Organization_Direction_Update, Organization_View, Organization_Add, Organization_Edit, Organization_Detail_View, \
    Type_Document_View, Type_Document_Add, Type_Document_Edit

urlpatterns = [
    path('project/settings/organization_direction/', Organization_Direction_View.as_view(),
         name='organization_direction'),
    path('project/settings/organization_direction/add/', Organization_Direction_Add.as_view(),
         name='organization_direction_add'),
    path('project/settings/organization_direction/edit/<slug:organization_direction_slug>',
         Organization_Direction_Update.as_view(), name='organization_direction_edit'),
    #
    path('project/settings/type_document/', Type_Document_View.as_view(), name='type_document'),
    path('project/settings/type_document/add/', Type_Document_Add.as_view(), name='type_document_add'),
    path('project/settings/type_document/edit/<slug:type_document_slug>', Type_Document_Edit.as_view(),
         name='type_document_edit'),

    path('project/organization/', Organization_View.as_view(), name='organization'),
    path('project/organization/add/', Organization_Add.as_view(), name='organization_add'),
    path('project/organization/edit/<slug:organization_slug>/', Organization_Edit.as_view(),
         name='organization_edit'),
    path('project/organization/view/<slug:organization_slug>/', Organization_Detail_View.as_view(),
         name='organization_detail_view'),

    path('organizations_objects/', Organizations_Objects_View.as_view(), name='organizations_objects'),
    path('organizations_objects/add/', Organizations_Objects_Add.as_view(), name='organizations_objects_add'),
    path('organizations_objects/edit/<slug:organizations_objects_slug>/', Organizations_Objects_Edit.as_view(),
         name='organizations_objects_edit'),

    path('projects/', Projects_View.as_view(), name='projects'),
    path('projects/add/', Projects_Add.as_view(), name='projects_add'),
    path('projects/edit/<slug:project_slug>/', Projects_Edit.as_view(), name='projects_edit'),

    path('development_task/', Development_Task_View.as_view(), name='development_task'),
    path('development_task/add/', Development_Task_Add.as_view(), name='development_task_add'),
    path('development_task/edit/<slug:development_task_slug>/', Development_Task_Edit.as_view(),
         name='development_task_edit'),
    path('development_task/delete/<slug:development_task_slug>/', Development_Task_Delete.as_view(),
         name='development_task_delete'),
    path('development_task/detailed/<slug:development_task_slug>/', Development_Task_DetailView.as_view(),
         name='development_task_detailed'),
    path('development_task/edit/date/<slug:development_task_slug>/', Development_Task_Edit_Date.as_view(),
         name='development_task_edit_date'),
    path('development_task/edit/develop/<slug:development_task_slug>/', Development_Task_Edit_Develop.as_view(),
         name='development_task_edit_develop'),
    path('development_task/edit/status/<slug:development_task_slug>/', Development_Task_Edit_Status.as_view(),
         name='development_task_edit_status'),

    path('position_objects/', Position_Objects_View.as_view(), name='position_objects'),
    path('position_objects/add/', Position_Objects_Add.as_view(), name='position_objects_add'),
    path('position_objects/edit/<slug:position_objects_slug>/', Position_Objects_Edit.as_view(),
         name='position_objects_edit'),
    path('position_objects/detailed/<slug:position_objects_slug>/', Position_Objects_DetailView.as_view(),
         name='position_objects_detailed'),
    path('position_objects/delete/<slug:position_objects_slug>/', Position_Objects_Delete.as_view(),
         name='position_objects_delete'),
    path('position_objects/edit/checker/<slug:position_objects_slug>/', Position_Objects_Edit_Checker.as_view(),
         name='position_objects_edit_checker'),
    path('position_objects/protocol/upload/<slug:position_objects_slug>/', Position_Objects_Upload_Protocol.as_view(),
         name='position_objects_upload_protokol'),

    path('cabinet/', Сabinet_View.as_view(), name='cabinet'),
    path('cabinet/add/', Сabinet_Add.as_view(), name='cabinet_add'),
    path('cabinet/edit/<slug:position_objects_slug>/', Сabinet_Edit.as_view(),
         name='cabinet_edit'),

]
