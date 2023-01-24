from django.urls import path

from workers_certificates.views import Certificate_Workers, Certificate_Workers_Add_All, Certificate_Workers_Add, \
     Сertificates_View, Сertificates_Add, Сertificates_Update, Сertificates_Parts_View, Сertificates_Parts_Add, \
     Сertificates_Parts_Update

urlpatterns = [
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
]
