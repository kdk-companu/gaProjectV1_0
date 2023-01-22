from django.urls import path


from workers.views import Workers, info1, Workers_Views, Workers_Add, Workers_Image, Subdivision_Add, Subdivision_View, \
    Subdivision_Update, Department_Add, Department_View, Department_Update, Chief_Add, Chief_View, Chief_Update, \
    Workers_Change_Password, Workers_Update_Password, Workers_Change, Workers_Basic_Change, Workers_Closed_Change, \
    Workers_Passport, Workers_Signature, Workers_Snils, Workers_Inn, Workers_Archive, Certificate_Workers, \
    Certificate_Workers_Add, Workers_Edit_Сontacts, Сertificates_View, Сertificates_Add, Сertificates_Update, \
    Сertificates_Parts_View, Сertificates_Parts_Add, Сertificates_Parts_Update, Certificate_Workers_Add_All

urlpatterns = [
    path('settings/subdivision/add/', Subdivision_Add.as_view(), name='subdivision_add'),
    path('settings/subdivision/', Subdivision_View.as_view(), name='subdivision'),
    path('settings/subdivision/update/<slug:subdivision_slug>', Subdivision_Update.as_view(),
         name='subdivision_update'),
    path('settings/department/add/', Department_Add.as_view(), name='department_add'),
    path('settings/department/', Department_View.as_view(), name='department'),
    path('settings/department/update/<slug:department_slug>', Department_Update.as_view(),
         name='department_update'),
    path('settings/chief/add/', Chief_Add.as_view(), name='chief_add'),
    path('settings/chief/', Chief_View.as_view(), name='chief'),
    path('settings/chief/update/<slug:chief_slug>', Chief_Update.as_view(), name='chief_update'),

    path('workers/', Workers.as_view(), name='workers'),
    path('workers/views/<slug:workers_slug>', Workers_Views.as_view(), name='workers_views'),
    path('workers/views/image/<slug:workers_slug>', Workers_Image.as_view(), name='workers_image'),
    path('workers/add/', Workers_Add.as_view(), name='workers_add'),
    path('workers/password/change/', Workers_Change_Password.as_view(), name='workers_change_password'),
    path('workers/password/update/<slug:workers_slug>', Workers_Update_Password.as_view(),
         name='workers_update_password'),
    path('workers/update/<slug:workers_slug>', Workers_Change.as_view(), name='workers_update'),
    path('workers/basic/update/<slug:workers_slug>', Workers_Basic_Change.as_view(), name='workers_basic_update'),
    path('workers/closed/update/<slug:workers_slug>', Workers_Closed_Change.as_view(), name='workers_closed_update'),
    path('workers/passport/<slug:workers_slug>', Workers_Passport.as_view(), name='workers_passport'),
    path('workers/snils/<slug:workers_slug>', Workers_Snils.as_view(), name='workers_snils'),
    path('workers/inn/<slug:workers_slug>', Workers_Inn.as_view(), name='workers_inn'),
    path('workers/archive/<slug:workers_slug>', Workers_Archive.as_view(), name='workers_archive'),
    path('workers/signature/<slug:workers_slug>', Workers_Signature.as_view(), name='workers_signature'),
    path('workers/contacts/<slug:workers_slug>', Workers_Edit_Сontacts.as_view(), name='contacts_edit'),

    path('workers/certificates/', Certificate_Workers.as_view(), name='workers_certificates'),
    path('workers/certificates/add/', Certificate_Workers_Add_All.as_view(), name='workers_certificate_add_all'),
    path('workers/certificates/add/<slug:workers_slug>', Certificate_Workers_Add.as_view(), name='workers_certificate_add'),


    path('settings/certificates/', Сertificates_View.as_view(), name='certificates'),
    path('settings/certificates/add/', Сertificates_Add.as_view(), name='certificates_add'),
    path('settings/certificates/update/<slug:сertificates_slug>', Сertificates_Update.as_view(),
         name='certificates_update'),

    path('settings/certificates_parts/', Сertificates_Parts_View.as_view(), name='certificates_parts'),
    path('settings/certificates_parts/add/', Сertificates_Parts_Add.as_view(), name='certificates_parts_add'),
    path('settings/certificates_parts/update/<slug:сertificates_parts_slug>', Сertificates_Parts_Update.as_view(),
         name='certificates_parts_update'),

    path('', Workers.as_view(), name='base_page')

]
