from django.urls import path

from workers_planning.views import Workers_Report_Card_View, Information_Schedule_View, Information_Schedule_Add, \
    Information_Schedule_Edit, Information_Missing_View, Information_Missing_Add, Information_Missing_Edit, \
    Workers_Missing_View, Workers_Missing_Edit, Workers_Missing_Add, Workers_Missing_Delete, Workers_Mission_View, \
    Workers_Mission_Add, Workers_Mission_Edit, Workers_Mission_Delete, Workers_Weekend_Work_View, \
    Workers_Weekend_Work_Delete, Workers_Weekend_Work_Edit, Workers_Weekend_Work_Add, Workers_Weekend_Work_Time_Add, \
    Workers_Work_Planning_View

urlpatterns = [
    path('settings/workers/information_schedule/', Information_Schedule_View.as_view(), name='information_schedule'),
    path('settings/workers/information_schedule/add/', Information_Schedule_Add.as_view(),
         name='information_schedule_add'),
    path('settings/workers/information_schedule/update/<int:pk>', Information_Schedule_Edit.as_view(),
         name='information_schedule_update'),

    path('settings/workers/information_missing/', Information_Missing_View.as_view(), name='information_missing'),
    path('settings/workers/information_missing/add/', Information_Missing_Add.as_view(),
         name='information_missing_add'),
    path('settings/workers/information_missing/update/<slug:information_missing_slug>',
         Information_Missing_Edit.as_view(), name='information_missing_update'),

    path('workers/workers_missing/', Workers_Missing_View.as_view(), name='workers_missing'),
    path('workers/workers_missing/add/', Workers_Missing_Add.as_view(),
         name='workers_missing_add'),
    path('workers/workers_missing/update/<int:pk>', Workers_Missing_Edit.as_view(),
         name='workers_missing_update'),
    path('workers/workers_missing/delete/<int:pk>', Workers_Missing_Delete.as_view(),
         name='workers_missing_delete'),

    path('workers/workers_mission/', Workers_Mission_View.as_view(), name='workers_mission'),
    path('workers/workers_mission/add/', Workers_Mission_Add.as_view(),
         name='workers_mission_add'),
    path('workers/workers_mission/update/<int:pk>', Workers_Mission_Edit.as_view(),
         name='workers_mission_update'),
    path('workers/workers_mission/delete/<int:pk>', Workers_Mission_Delete.as_view(),
         name='workers_mission_delete'),

    path('workers/weekend_work/', Workers_Weekend_Work_View.as_view(), name='workers_weekend_work'),
    path('workers/weekend_work/add/', Workers_Weekend_Work_Add.as_view(),
         name='workers_weekend_work_add'),
    path('workers/weekend_work/update/<int:pk>', Workers_Weekend_Work_Edit.as_view(),
         name='workers_weekend_work_update'),
    path('workers/weekend_work/update/time/<int:pk>', Workers_Weekend_Work_Time_Add.as_view(),
         name='workers_weekend_work_update_time'),
    path('workers/weekend_work/delete/<int:pk>', Workers_Weekend_Work_Delete.as_view(),
         name='workers_weekend_work_delete'),

    path('workers/work_planning/', Workers_Work_Planning_View.as_view(),
         name='workers_work_planning'),

    path('workers/report_card/', Workers_Report_Card_View.as_view(), name='report_card'),

]
